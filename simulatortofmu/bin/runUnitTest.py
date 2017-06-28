#######################################################
# Script with unit tests for SimulatorToFMU
#
# TSNouidui@lbl.gov                            2016-09-06
#######################################################
import unittest
import os
import sys
import platform
import subprocess
import shutil
from datetime import datetime

# Appending parser_path to the system path os required to be able
# to find the SimulatorToFMU model from this directory
script_path = os.path.dirname(os.path.realpath(__file__))
parser_path = os.path.abspath(os.path.join(script_path, '..', 'parser'))
sys.path.append(parser_path)

import SimulatorToFMU as simulator

XSD_SCHEMA = 'SimulatorModelDescription.xsd'
NEEDSEXECUTIONTOOL = 'needsExecutionTool'
MODELDESCRIPTION = 'modelDescription.xml'
SimulatorModelicaTemplate_MO = 'SimulatorModelicaTemplate.mo'
SimulatorModelicaTemplate_Dymola_MOS = 'SimulatorModelicaTemplate_Dymola.mos'
SimulatorModelicaTemplate_JModelica_MOS = 'SimulatorModelicaTemplate_JModelica.py'
SimulatorModelicaTemplate_OpenModelica_MOS = 'SimulatorModelicaTemplate_OpenModelica.mos'
XML_MODELDESCRIPTION = 'SimulatorModelDescription.xml'
# Get the path to the templates files
script_path = os.path.dirname(os.path.realpath(__file__))
utilities_path = os.path.join(script_path, '..', 'parser', 'utilities')
PYTHON_SCRIPT_PATH = os.path.join(utilities_path, 'simulator_wrapper.py')
MO_TEMPLATE_PATH = os.path.join(utilities_path, SimulatorModelicaTemplate_MO)
MOS_TEMPLATE_PATH_DYMOLA = os.path.join(
    utilities_path, SimulatorModelicaTemplate_Dymola_MOS)
MOS_TEMPLATE_PATH_JMODELICA = os.path.join(
    utilities_path, SimulatorModelicaTemplate_JModelica_MOS)
MOS_TEMPLATE_PATH_OPENMODELICA = os.path.join(
    utilities_path, SimulatorModelicaTemplate_OpenModelica_MOS)
XSD_FILE_PATH = os.path.join(utilities_path, XSD_SCHEMA)
XML_INPUT_FILE = os.path.join(utilities_path, XML_MODELDESCRIPTION)
SimulatorToFMU_LIB_PATH = os.path.join(
    script_path, '..', 'parser', 'libraries', 'modelica')
python_scripts_path = [PYTHON_SCRIPT_PATH]

if(platform.system().lower() == 'windows'):
    python_scripts_path = [item.replace('\\', '\\\\') for item in [
        PYTHON_SCRIPT_PATH]]

Simulator_T = simulator.SimulatorToFMU('con_path',
                                       XML_INPUT_FILE,
                                       SimulatorToFMU_LIB_PATH,
                                       MO_TEMPLATE_PATH,
                                       MOS_TEMPLATE_PATH_DYMOLA,
                                       XSD_FILE_PATH,
                                       '35',
                                       python_scripts_path,
                                       '2.0',
                                       'me',
                                       'dymola',
                                       None,
                                       None,
                                       'false')


class Tester(unittest.TestCase):
    '''
    Class that runs all regression tests.

    '''

    def test_check_duplicates(self):
        '''
        Test the function check_duplicates().

        '''

        # Array does not contain duplicates variables.
        simulator.check_duplicates(['x1', 'x2', 'x3', 'x4'])

        # Array contain duplicates variables.
        with self.assertRaises(AssertionError):
            simulator.check_duplicates(['x1', 'x1', 'x3', 'x4'])

    def test_sanitize_name(self):
        '''
        Test the function sanitize_name().

        '''

        # Testing name conversions.
        name = simulator.sanitize_name('test+name')
        self.assertEqual(name, 'test_name', 'Names are not matching.')

        name = simulator.sanitize_name('0test+*.name')
        self.assertEqual(name, 'f_0test___name', 'Names are not matching.')

    def test_xml_validator(self):
        '''
        Test the function xml_validator().

        '''

        # Testing validation of xml file
        Simulator_T.xml_validator()

    def test_xml_parser(self):
        '''
        Test the function xml_validator().

        '''

        # Testing validation of xml file
        Simulator_T.xml_parser()

    def test_print_mo(self):
        '''
        Test the function print_mo().

        '''

        # Testing function to print Modelica model.
        Simulator_T.print_mo()

    #@unittest.skip("Export Simulator using multiple options.")
    def test_simulator_to_fmu(self):
        '''
        Test the export of an FMU with various options.

        '''

        for tool in ['dymola', 'jmodelica', 'omc']:
            if (platform.system().lower() == 'linux' and tool == 'omc'):
                print ('tool={!s} is not supported on Linux.'.format(tool))
                continue
            if tool == 'omc':
                modPat = 'OPENMODELICALIBRARY'
                mosT = MOS_TEMPLATE_PATH_OPENMODELICA
            elif tool == 'dymola':
                modPat = 'MODELICAPATH'
                mosT = MOS_TEMPLATE_PATH_DYMOLA
            elif tool == 'jmodelica':
                os.environ['MODELICAPATH']=''
                modPat = None
                mosT = MOS_TEMPLATE_PATH_JMODELICA
            for version in ['1', '2']:
                if (tool == 'omc' or tool == 'jmodelica'):
                    version = str(float(version))
                for api in ['me', 'cs']:
                    if (tool == 'omc' and version == '1.0' and api == 'cs'):
                        print (
                            'tool={!s} with FMI version={!s} and FMI API={!s} is not supported.'.format(
                                tool, version, api))
                        continue
                    for cs_xml in ['true']:
                        if (version == '1'):
                            continue
                        Simulator_Test = simulator.SimulatorToFMU(
                            'con_path',
                            XML_INPUT_FILE,
                            SimulatorToFMU_LIB_PATH,
                            MO_TEMPLATE_PATH,
                            mosT,
                            XSD_FILE_PATH,
                            '35',
                            python_scripts_path,
                            version,
                            api,
                            tool,
                            None,
                            modPat,
                            cs_xml)

                        print (
                            'Export the simulator with tool={!s}, FMI version={!s}, FMI API={!s}'.format(
                                tool, version, api))
                        start = datetime.now()
                        Simulator_Test.print_mo()
                        Simulator_Test.generate_fmu()
                        Simulator_Test.clean_temporary()
                        Simulator_Test.rewrite_fmu()
                        end = datetime.now()
                        print(
                            'Export Simulator as an FMU in {!s} seconds.'.format(
                                (end - start).total_seconds()))
                        
    #@unittest.skip("Export Simulator using multiple options.")
    def test_updates_fmu(self):
        '''
        Test the export and updates of FMUs.

        '''

        for tool in ['dymola', 'jmodelica', 'omc']:
            if (platform.system().lower() == 'linux' and tool == 'omc'):
                print ('tool={!s} is not supported on Linux.'.format(tool))
                continue
            if tool == 'omc':
                modPat = 'OPENMODELICALIBRARY'
                mosT = MOS_TEMPLATE_PATH_OPENMODELICA
            elif tool == 'dymola':
                modPat = 'MODELICAPATH'
                mosT = MOS_TEMPLATE_PATH_DYMOLA
            elif tool == 'jmodelica':
                os.environ['MODELICAPATH']=''
                modPat = None
                mosT = MOS_TEMPLATE_PATH_JMODELICA
            for version in ['2']:
                if (tool == 'omc' or tool == 'jmodelica'):
                    version = str(float(version))
                for api in ['me']:
                    if (tool == 'omc' and version == '1.0' and api == 'cs'):
                        print (
                            'tool={!s} with FMI version={!s} and FMI API={!s} is not supported.'.format(
                                tool, version, api))
                        continue
                    for cs_xml in ['true']:
                        if (version == '1'):
                            continue
                        Simulator_Test = simulator.SimulatorToFMU(
                            'con_path',
                            XML_INPUT_FILE,
                            SimulatorToFMU_LIB_PATH,
                            MO_TEMPLATE_PATH,
                            mosT,
                            XSD_FILE_PATH,
                            '35',
                            python_scripts_path,
                            version,
                            api,
                            tool,
                            None,
                            modPat,
                            cs_xml)

                        print (
                            'Export the simulator with tool={!s}, FMI version={!s}, FMI API={!s}'.format(
                                tool, version, api))
                        start = datetime.now()
                        Simulator_Test.print_mo()
                        Simulator_Test.generate_fmu()
                        Simulator_Test.clean_temporary()
                        Simulator_Test.rewrite_fmu()
                        end = datetime.now()
                        print(
                            'Export Simulator as an FMU in {!s} seconds.'.format(
                                (end - start).total_seconds()))
                        
                        if(tool=='dymola'):
                            tool_folder='Dymola'
                        elif(tool=='jmodelica'):
                            tool_folder='JModelica'
                        elif(tool=='omc'):
                            tool_folder='OpenModelica'
                        fmu_path = os.path.join(
                        script_path, '..', 'fmus', tool_folder, platform.system().lower())
                        print(
                            'Copy Simulator.fmu to {!s}.'.format(fmu_path))
                        shutil.copy2('Simulator.fmu', fmu_path)

    #@unittest.skip("Run the FMU using PyFMI")
    def test_run_simulator_fmu(self):
        '''
        Test the execution of one Simulator FMU.

        '''
        
        try:
            from pyfmi import load_fmu
        except BaseException:
            print ('PyFMI not installed. Test will not be be run.')
            return
        
        # Run the cases
        if platform.system().lower() == 'windows':
            # Export FMUs which are needed to run the cases.
            for tool in ['dymola', 'jmodelica', 'omc']:
                if tool == 'omc':
                    modPat = 'OPENMODELICALIBRARY'
                    mosT = MOS_TEMPLATE_PATH_OPENMODELICA
                elif tool == 'dymola':
                    modPat = 'MODELICAPATH'
                    mosT = MOS_TEMPLATE_PATH_DYMOLA
                elif tool == 'jmodelica':
                    os.environ['MODELICAPATH']=''
                    modPat = None
                    mosT = MOS_TEMPLATE_PATH_JMODELICA
                for version in ['2']:
                    if (tool == 'omc' or tool == 'jmodelica'):
                        version = str(float(version))
                    for api in ['me']:
                        if (tool == 'omc' and version == '1.0' and api == 'cs'):
                            print (
                                'tool={!s} with FMI version={!s} and FMI API={!s} is not supported.'.format(
                                    tool, version, api))
                            continue
                        for cs_xml in ['true']:
                            if (version == '1'):
                                continue
                            Simulator_Test = simulator.SimulatorToFMU(
                                'con_path',
                                XML_INPUT_FILE,
                                SimulatorToFMU_LIB_PATH,
                                MO_TEMPLATE_PATH,
                                mosT,
                                XSD_FILE_PATH,
                                '35',
                                python_scripts_path,
                                version,
                                api,
                                tool,
                                None,
                                modPat,
                                cs_xml)
    
                            print (
                                'Export the simulator with tool={!s}, FMI version={!s}, FMI API={!s}'.format(
                                    tool, version, api))
                            start = datetime.now()
                            Simulator_Test.print_mo()
                            Simulator_Test.generate_fmu()
                            Simulator_Test.clean_temporary()
                            Simulator_Test.rewrite_fmu()
                            end = datetime.now()
                            print(
                                'Export Simulator as an FMU in {!s} seconds.'.format(
                                    (end - start).total_seconds()))
                            
                            if(tool=='dymola'):
                                tool_folder='Dymola'
                            elif(tool=='jmodelica'):
                                tool_folder='JModelica'
                            elif(tool=='omc'):
                                tool_folder='OpenModelica'
                            fmu_path = os.path.join(
                            script_path, '..', 'fmus', tool_folder, platform.system().lower())
                            print(
                                'Copy Simulator.fmu to {!s}.'.format(fmu_path))
                            shutil.copy2('Simulator.fmu', fmu_path)
        
    
            # OMC needs to be run first otherwise PyFMI will segfault.
            # It seems like either Dymola or JModelica is not releasing
            # resources hence causing OpenModelica to fail.
            for tool in ['OpenModelica', 'Dymola', 'JModelica']:
                fmu_path = os.path.join(
                        script_path, '..', 'fmus', tool, 'windows', 'Simulator.fmu')
                # Parameters which will be arguments of the function
                start_time = 0.0
                stop_time = 5.0
    
                print ('Starting the simulation with {!s}'.format(tool))
                start = datetime.now()
                # Path to configuration file
                simulator_con_val_str = os.path.abspath('config.json')
                if sys.version_info.major > 2:
                    simulator_con_val_str = bytes(simulator_con_val_str, 'utf-8')
    
                simulator_input_valref = []
                simulator_output_valref = []
    
                sim_mod = load_fmu(fmu_path, log_level=7)
                sim_mod.setup_experiment(
                    start_time=start_time, stop_time=stop_time)
    
                # Define the inputs
                simulator_input_names = ['v']
                simulator_input_values = [220.0]
                simulator_output_names = ['i']
    
                # Get the value references of simulator inputs
                for elem in simulator_input_names:
                    simulator_input_valref.append(
                        sim_mod.get_variable_valueref(elem))
    
                # Get the value references of simulator outputs
                for elem in simulator_output_names:
                    simulator_output_valref.append(
                        sim_mod.get_variable_valueref(elem))
    
                # Set the flag to save the results
                sim_mod.set('_saveToFile', 0)
                # Get value reference of the configuration file
                simulator_con_val_ref = sim_mod.get_variable_valueref(
                    '_configurationFileName')
    
                # Set the configuration file
                # Setting strings failed in JModelica. This seems to be a bug
                # since JModelica sets the variability of models which contain
                # a string parameter to constant. Consequently the FMU cannot
                # be modified at runtime. The workaround will be to pass the
                # path to the configuration file when invoking SimulatorToFMU so
                # it has the configuration file in its resource folders.
                if not (tool=='JModelica'):
                    sim_mod.set_string(
                        [simulator_con_val_ref],
                        [simulator_con_val_str])
    
                # Initialize the FMUs
                sim_mod.initialize()
    
                # Call event update prior to entering continuous mode.
                sim_mod.event_update()
    
                # Enter continuous time mode
                sim_mod.enter_continuous_time_mode()
    
                sim_mod.set_real(simulator_input_valref, simulator_input_values)
                
                end = datetime.now()
    
                print(
                    'Ran a single Simulator simulation with {!s} FMU={!s} in {!s} seconds.'.format(
                        tool, fmu_path, (end - start).total_seconds()))
                if not (tool=='OpenModelica'):
                    # PyFMI fails to get the output of an OpenModelica FMU 
                    self.assertEqual(
                        sim_mod.get_real(
                            sim_mod.get_variable_valueref('i')),
                        1.0,
                        'Values are not matching.')
                    
                # Terminate FMUs
                sim_mod.terminate()
        else:
            print('The unit tests for simulating FMUs only run on Windows')
                                            

if __name__ == "__main__":
    unittest.main()
