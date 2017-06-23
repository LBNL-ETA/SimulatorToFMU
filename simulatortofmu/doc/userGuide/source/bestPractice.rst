.. highlight:: rest

.. _bestPractice:


Best Practice
=============

This section explains to users the best practice in configuring a Simulator XML input file,
and implementing the Python wrapper which will interface with the Simulator.

Configuring the Simulator XML input file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To export a Simulator as an FMU, the user needs to write an XML file which contains the list 
of inputs, outputs and parameters of the FMU. The XML snippet below shows how a user has to write such an input file.
A template named ``SimulatorModeldescritpion.xml`` which shows such a file is provided in the ``parser/utilities`` installation folder of SimulatorToFMU. 
This template should be adapted to create new XML input file.

The following snippet shows an input file where the user defines 1 input and 1 output variable.

.. literalinclude:: ../../../parser/utilities/SimulatorModelDescription.xml
   :language: xml
   :linenos:

To create such an input file, the user needs to specify the name of the FMU (Line 5). 
This is the ``modelName`` which should be unique.
The user then needs to define the inputs and outputs of the FMUs. 
This is done by adding a ``ScalarVariable`` into the list of ``ModelVariables``.

To parametrize the ``ScalarVariable`` as an input variable, the user needs to

  - define the name of the variable (Line 10), 
  - give a brief description of the variable (Line 11)
  - give the causality of the variable (``input`` for inputs, ``output`` for outputs) (Line 12)
  - define the type of variable (Currently only ``Real`` variables are supported) (Line 13)
  - give the unit of the variable (Currently only valid :term:`Modelica` units are supported) (Line 14)
  - give a start value for the input variable (This is optional) (Line 15)

To parametrize the ``ScalarVariable`` as an output variable, the user needs to

  - define the name of the variable (Line 18), 
  - give a brief description of the variable (Line 19)
  - give the causality of the variable (``input`` for inputs, ``output`` for outputs) (Line 20)
  - define the type of variable (Currently only ``Real`` variables are supported) (Line 21)
  - give the unit of the variable (Currently only valid :term:`Modelica` units are supported) (Line 22)
   

Configuring the Python Wrapper Simulator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To export Simulator as an FMU, the user needs to write the Python wrapper which will interface with the Simulator.
The wrapper will be embedded in the FMU when the Simulator is exported and used at runtime on the target machine.

The user needs to extend the Python wrapper provided in ``parser/utilities/simulator_wrapper.py`` 
and implements the function ``exchange``.

The following snippet shows the Simulator function.

.. literalinclude:: ../../../parser/utilities/simulator_wrapper.py
   :language: python
   :linenos:

The arguments of the functions are in the next table

+----------------------------------------------------+-------------------------------------------------------------------+
| Arguments                                          | Description                                                       | 
+====================================================+===================================================================+
| ``configuration_file``                             | The Path to the Simulator model or configuration file             |
+----------------------------------------------------+-------------------------------------------------------------------+
| ``time``                                           | The current simulation model time                                 |   
+----------------------------------------------------+-------------------------------------------------------------------+
| ``input_names``                                    | The list of input names of the FMU                                |  
+----------------------------------------------------+-------------------------------------------------------------------+
| ``input_values``                                   | The list of input values of the FMU                               |   
+----------------------------------------------------+-------------------------------------------------------------------+
| ``output_names``                                   | The list of output names of the FMU                               | 
+----------------------------------------------------+-------------------------------------------------------------------+
| ``output_values``                                  | The list of output values of the FMU                              | 
+----------------------------------------------------+-------------------------------------------------------------------+
| ``write_results``                                  | A flag for writing results to a file                              | 
+----------------------------------------------------+-------------------------------------------------------------------+

.. note:: 

   - The function ``exchange`` must return a list of output values which matches the order of the output names. 
   - The function ``exchange`` can be used to invoke external programs/scripts which do not ship with the FMU. 
     The external programs/scripts will have to be installed on the target machine where the 
     FMU is run. See :doc:`build` for details on command line options. 
   - Once ``simulator_wrapper.py`` is implemented, it must be saved under the same name, and its path used as required argument for ``SimulatorToFMU.py``.

  
