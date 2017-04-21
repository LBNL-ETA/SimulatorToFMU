# Main Python function to be modified to integrate the main simulator.


def exchange(configuration_file, time, input_values, 
            input_names, output_names, write_results):
    """
        Args:
        configuration_file (String): filename for the model configurations
        time (Float): Simulation time
        input_names (Strings): voltage vector names
        input_values (Floats): voltage vector values (same length as voltage_names)
        output_names (Strings): vector of name matching CymDIST nomenclature
        write_results (1 or 0): save all nodes results to a file
        
    Example:
        >>> configuration_file = 'config.json'
        >>> time = 0
        >>> input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
        >>> input_values = [2520, 2520, 2520, 0, -120, 120]
        >>> output_names = ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC']
        >>> write_results = 0
        >>> output_values = simulator(configuration_file, time, input_names,
                        input_values, output_names)
    """
    
    #######################################################################
    # EDIT AND INCLUDE CUSTOM CODE FOR TARGET SIMULATOR
    # ***Include body of the function used to compute the output values***
    # based on the inputs received by the simulator function
    # This function currently returns the input values. 
    # This will need to be adapted so it return the output_values instead.
    
    #########################################################################

    return input_values
    
