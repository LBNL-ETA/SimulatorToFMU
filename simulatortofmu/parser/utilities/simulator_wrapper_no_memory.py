# Dummy Python-driven simulator
class Simulator():
    """
    Dummy simulator Python-driven simulator
    which increments in its doTimeStep method the input values by 1.
    This class is for illustration purposes only.
    """
    def __init__(self, configuration_file, time, input_names,
            input_values, output_names, write_results):
        self.configuration_file = configuration_file
        self.input_values = input_values


    def doTimeStep(self, input_values):
        """
        This function increments the input variables by 1
        """

        return input_values + 1

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
    ########################################################################

    # # Initialize the Simulator object
    s = Simulator(configuration_file, time, input_names,
                        input_values, output_names, write_results)
    # check if we have input values. If yes, update the outputs.
    if not (input_values is None):
        output_values=s.doTimeStep(input_values)
    else:
        # Return default output value
        output_values = 1.0

    # Save the output of the Simulator
    #########################################################################
    return output_values
