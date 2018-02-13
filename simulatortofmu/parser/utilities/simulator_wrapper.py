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


    def doTimeStep(self, input_values):
        """
        This function increments the input variables by 1
        """

        return input_values + 1

# Main Python function to be modified to interface with a simulator which has memory.
def exchange(configuration_file, time, input_names,
            input_values, output_names, write_results,
            memory):
    """
    Return  a list of output values from the Python-based Simulator.
    The order of the output values must match the order of the output names.

    :param configuration_file (String): Path to the Simulator model or configuration file
    :param time (Float): Simulation time
    :param input_names (Strings): Input names
    :param input_values (Floats): Input values (same length as input_names)
    :param output_names (Strings): Output names
    :param write_results (Integers): Store results to file (1 to store, 0 else)
    :param memory: Variable that stores the memory of a Python object

    """

    #######################################################################
    # EDIT AND INCLUDE CUSTOM CODE FOR TARGET SIMULATOR
    # Include body of the function used to compute the output values
    # based on the inputs received by the simulator function.
    # This will need to be adapted so it returns the correct output_values.
    # If the list of output names has only one name, then only a scalar
    # must be returned.
    # The snippet shows how a Python object should be held in the memory
    # This is done by getting the object from the exchange function, modifying it,
    # and returning it.
    ########################################################################
    # Since master algorithms need to some time call at the same time instant
    # an FMU multiple times for event iteration. It is for efficient reasons
    # good to catch the simulator input and outputs results, along with the current
    #  and past simulation times to determine when the Simulator needs to be reinvoked.
    if memory == None:
        # Initialize the Python object
        s = Simulator(configuration_file, time, input_names,
                        input_values, output_names, write_results)
        memory = {'inputsLast':input_values, 'memory':s,
                'tLast':time, 'outputs':None}
        if not (input_values is None):
            memory['inputsLast'] = input_values
            memory['outputs'] = s.doTimeStep(input_values)
        else:
            # Return default output
            memory['outputs'] = 1.0
        memory['s'] = s
    else:
        # Check if inputs values have changed
        if not (input_values is None):
            newInputs = sum([abs(m - n) for m, n in zip (input_values,
            memory['inputsLast'])])
        # Check if time has changed prior to updating the outputs
        if(abs(time - memory['tLast'])>1e-6 or newInputs > 0):
            # Updtate the outputs of the Simulator
            memory['outputs'] = memory['s'].doTimeStep(memory['outputs'])
            # Save last time
            memory['tLast'] = time
            # Save last input values
            memory['inputsLast'] = input_values
    # Handle errors
    if(memory['outputs'] < 0.0):
            raise("The memory['outpus'] cannot be null")
    # Save the output of the Simulator
    output_values = memory['outputs']
    #########################################################################
    return [output_values, memory]

if __name__ == "__main__":
    memory = None
    print(exchange("dummy.csv", 0.0, "v", None, "i", 0, memory))
