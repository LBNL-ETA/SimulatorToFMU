# Main Python function to be modified to integrate the main simulator.

def exchange(configuration_file, time, input_values, 
            input_names, output_names, write_results):
    """
    Return  a list of output values from the Python-based Simulator.
    The order of the output values must match the order of the output names.    

    :param configuration_file (String): filename for the model configurations
    :param time (Float): Current simulation time
    :param input_values (Floats): Input values 
    :param input_names (Strings): Input names (same length as input_values)

    :param output_names (Strings): Output names
    :param write_results (Float): save results to a file (1.0 for saving, 0.0 else)
        
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
    # Assign the vector of output values with dummy values.
    output_values = [0]*len(output_names)
    #########################################################################

    return output_values
    
