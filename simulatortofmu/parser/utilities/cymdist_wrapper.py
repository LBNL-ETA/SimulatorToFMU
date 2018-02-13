# import numpy
# def cymdist(configuration_filename, time, input_voltage_names,
            # input_voltage_values, output_names, input_save_to_file):
			# #print("This is the configuration={!s}".format(configuration_filename))
			# return [0,1,2,3,4,5]
import json
try:
    import cympy
except:
    # Only installed on the Cymdist server
    pass


def exchange(configuration_filename, time, input_voltage_names,
            input_voltage_values, output_names, input_save_to_file):

    """Communicate with the FMU to launch a Cymdist simulation

    Args:
        configuration_filename (String): filename for the model configurations
        time (Float): Simulation time
        input_voltage_names (Strings): voltage vector names
        input_voltage_values (Floats): voltage vector values (same length as voltage_names)
        output_names (Strings): vector of name matching CymDIST nomenclature
        input_save_to_file (1 or 0): save all nodes results to a file

    Example:
        >>> time = 0
        >>> input_save_to_file = 0
        >>> input_voltage_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
        >>> input_voltage_values = [2520, 2520, 2520, 0, -120, 120]
        >>> configuration_filename = 'config.json'
        >>> output_names = ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC']

        >>> cymdist(configuration_filename, time, input_voltage_names,
                input_voltage_values, output_names, input_save_to_file)
    Note:
        config.json file format:
        {times: [0]
         interpolation_method: 'closest_time',
         models: [{
            filename: 'my_model.sxst',
            new_loads: [{
                section_id: '',
                active_power: '',
            }],
            new_pvs: [{
                section_id: '',
                generation: '',
            }],
            set_pvs: [{
                device_number: '',
                generation: '',
            }],
            set_loads: [{
                device_number: '',
                active_power: [{
                    active_power: '',
                    phase_index: '',
                    phase: c,
                }],
            }],
         }]
        }
        (time vector must have a 1:1 relationship with the model vector)

        output_names can be: ['KWA', 'KWB', 'KWC', 'KVARA', 'KVARB', 'KVARC',
        'IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC', 'PFA', 'PFB', 'PFC']
        for a greater list see CymDIST > customize > keywords > powerflow
        (output unit is directly given by output name)
    """

    def _input_voltages(input_voltage_names, input_voltage_values):
        """Create a dictionary from the input values and input names for voltages"""
        voltages = {}
        for name, value in zip(input_voltage_names, input_voltage_values):
            voltages[name] = value
        return voltages

    def _read_configuration_file(configuration_filename, current_time):
        """This function open the configuration file and pick the right model given
        a simulation time.
        """
        def _closest_time(current_time, times):
            """Find the closest time, return model index"""
            distances = [abs(value - current_time) for value in times]
            min_value, min_index = min((value, index) for index, value in enumerate(distances))
            return min_index

        # Open the configuration file and read the configurations
        with open(configuration_filename, 'r') as configuration_file:
            configuration = json.load(configuration_file)

        # Select the appropriate model
        model = configuration['models'][_closest_time(current_time, configuration['times'])]
        return model

    def _set_voltages(voltages, networks):
        """Set the voltage at the source node"""
        # Set up the right voltage in kV (input must be V)
        cympy.study.SetValueTopo(voltages['VMAG_A'] / 1000,
            "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage1", networks[0])
        cympy.study.SetValueTopo(voltages['VMAG_B'] / 1000,
            "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage2", networks[0])
        cympy.study.SetValueTopo(voltages['VMAG_C'] / 1000,
            "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage3", networks[0])
        return True

    def _add_loads(loads):
        for index, load in enumerate(loads):
            # Add load and overwrite (load demand need to be sum of previous load and new)
            temp_load_model = cympy.study.AddDevice(
                "MY_LOAD_" + str(index), 14, load['section_id'], 'DEFAULT',
                cympy.enums.Location.FirstAvailable , True)

            # Set power demand
            phases = list(cympy.study.QueryInfoDevice("Phase", "MY_LOAD_" + str(index), 14))
            power = load['active_power'] / len(phases)
            for phase in range(0, len(phases)):
                cympy.study.SetValueDevice(
                    power,
                    'CustomerLoads[0].CustomerLoadModels[0].CustomerLoadValues[' + str(phase) + '].LoadValue.KW',
                    "MY_LOAD_" + str(index), 14)
            # Note: customer is still 0 as well as energy values, does it matters?
        return True

    def _set_loads(loads):
        for index, load in enumerate(loads):
            for phase in load['active_power']:
                cympy.study.SetValueDevice(phase['active_power'],
                    'CustomerLoads[0].CustomerLoadModels[0].CustomerLoadValues[' + str(phase['phase_index']) + '].LoadValue.KW',
                    load['device_number'], 14)
        return True

    def _add_pvs(pvs):
        """Add new pvs on the grid"""
        for index, pv in enumerate(pvs):
            # Add PVs
            device = cympy.study.AddDevice("my_pv_" + str(index), cympy.enums.DeviceType.Photovoltaic, pv['section_id'])

            # Set PV size (add + 30 to make sure rated power is above generated power)
            device.SetValue(int((pv['generation'] + 30) / (23 * 0.08)), "Np")  # (ns=23 * np * 0.08 to find kW) --> kw / (23 * 0.08)
            device.SetValue(pv['generation'], 'GenerationModels[0].ActiveGeneration')

            # Set inverter size
            device.SetValue(pv['generation'], "Inverter.ConverterRating")
            device.SetValue(pv['generation'], "Inverter.ActivePowerRating")
            device.SetValue(pv['generation'], "Inverter.ReactivePowerRating")
        return True

    def _set_pvs(pvs):
        for index, pv in enumerate(pvs):
            cympy.study.SetValueDevice(int((pv['generation'] + 30) / (23 * 0.08)), 'Np',
                pv['device_number'], 39)
            cympy.study.SetValueDevice(pv['generation'], 'GenerationModels[0].ActiveGeneration',
                pv['device_number'], 39)
            cympy.study.SetValueDevice(pv['generation'], 'Inverter.ConverterRating',
                pv['device_number'], 39)
            cympy.study.SetValueDevice(pv['generation'], 'Inverter.ActivePowerRating',
                pv['device_number'], 39)
            cympy.study.SetValueDevice(pv['generation'], 'Inverter.ReactivePowerRating',
                pv['device_number'], 39)
        return True

    def _write_results(input_model_filename):
        """Write result to the file system"""
        # nodes = functions.list_nodes()
        # nodes = functions.get_voltage(nodes, is_node=True)
        # nodes.to_csv(input_model_filename + '_result.csv')
        return True

    def _output_values(source_node_id, output_names):
        """Query the right output name at the source node"""
        output = []
        for category in output_names:
            temp = cympy.study.QueryInfoNode(category, source_node_id)
            output.append(float(temp) * 1.0)
        return output

    # Process input and check for validity
    voltages = _input_voltages(input_voltage_names, input_voltage_values)
    if input_save_to_file in [1, 1.0, '1']:
        input_save_to_file = True
    else:
        input_save_to_file = False

    model = _read_configuration_file(configuration_filename, time)
    # Open the model
	#raise(model['filename'])
    cympy.study.Open(model['filename'])
    print("Could open model")

    # Set voltages
    networks = cympy.study.ListNetworks()
    _set_voltages(voltages, networks)

    # Set loads
    if model['set_loads']:
        _set_loads(model['set_loads'])

    # Add loads
    if model['new_loads']:
        _add_loads(model['new_loads'])

    # Set loads
    if model['set_pvs']:
        _set_pvs(model['set_pvs'])

    # Add PV
    if model['new_pvs']:
        _add_pvs(model['new_pvs'])

    # Run the power flow
    lf = cympy.sim.LoadFlow()
    lf.Run()

    # Write full results?
    if input_save_to_file:
        _write_results(model['filename'])

    # Return the right values
    source_node_id = cympy.study.GetValueTopo("Sources[0].SourceNodeID", networks[0])
    output = _output_values(source_node_id, output_names)
    return [output, memory]
    #return [0, 1,2,3,4,5]

# time = 0
# input_save_to_file = 0
# input_voltage_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
# input_voltage_values = [2520, 2520, 2520, 0, -120, 120]
# configuration_filename = 'config.json'
# output_names = ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC']
#
# print(cymdist(configuration_filename, time, input_voltage_names,
#                 input_voltage_values, output_names, input_save_to_file))
