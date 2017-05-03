# Main Python function to be modified to interface with the Simulator.

def exchange(configuration_file, time, input_values, 
            input_names, output_names, write_results):
    """
    Return  a list of output values from the Python-based Simulator.
    The order of the output values must match the order of the output names.    

    :param configuration_file (String): Model configuration name
    :param time (Float): Current Simulation time
    :param input_values (Floats): Input values 
    :param input_names (Strings): Input names (same length as input_values)
    :param output_names (Strings): Output names
    :param write_results (Float): Save results to a file (1 to store, 0 else)
        
    Example:
        >>> configuration_file = 'config.json'
        >>> time = 0
        >>> input_names = ['v']
        >>> input_values = [220.0]
        >>> output_names = ['i']
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
    # If the list of output names has only one name, then only a scalar 
    # must be returned.
    if (len(output_names) > 1):
        output_values = [1.0] * len(output_names)
    else:
        output_values = 1.0
    #########################################################################
    return output_values
    
