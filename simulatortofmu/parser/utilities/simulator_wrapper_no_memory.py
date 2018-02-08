# Dummy Python-driven simulator
class Simulator():
    """
    Dummy simulator Python-driven simulator
    which increments in its doTimeSteo method the input values by 1.
    This class is for illustration purposes only.
    """
    def __init__(self, configuration_file, time, input_names, 
            input_values, output_names, write_results):
        self.configuration_file = configuration_file
        self.input_values = input_values

    
    def doTimeStep(self):
        """
        This function increments the input variables by 1
        """
        
        return self.input_values + 1

# Main Python function to be modified to interface with a simulator which has memory.
def exchange(configuration_file, time, input_names, 
            input_values, output_names, write_results):
    """
    Return  a list of output values from the Python-based Simulator.
    The order of the output values must match the order of the output names.    

    :param configuration_file (String): Path to the Simulator model or configuration file
    :param time (Float): Simulation time
    :param input_names (Strings): Input names 
    :param input_values (Floats): Input values (same length as input_names) 
    :param output_names (Strings): Output names
    :param write_results (Integers): Store results to file (1 to store, 0 else)
        
    """

    #######################################################################
    # EDIT AND INCLUDE CUSTOM CODE FOR TARGET SIMULATOR
    # Include body of the function used to compute the output values
    # based on the inputs received by the simulator function. 
    # This will need to be adapted so it returns the correct output_values.
    # If the list of output names has only one name, then only a scalar 
    # must be returned.
    s = Simulator(configuration_file, time, input_names,
                    input_values, output_names, write_results)

    output_values = s.doTimeStep()
    # Check if return values are correct
    # Store the new state of the simulator
    if(output_values < input_values):
        raise("...")
    #########################################################################
    return output_values
    
if __name__ == "__main__":
    memory = None
    print(exchange("test.csv", 1.0, "i1", 0.0, "y1", 1))
    print(exchange("test.csv", 2.0, "i1", 1.0, "y1", 1))