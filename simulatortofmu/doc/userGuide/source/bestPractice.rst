.. highlight:: rest

.. _bestPractice:


Best Practice
=============

This section explains to users the best practice in configuring a Simulator XML input file,
and implementing the Python wrapper which will interface with the Simulator.


Configuring and Generating the Python Binaries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This option has been added starting from Python 3.8.
To export a Simulator that wraps a Python script as an FMU,
the user needs to configure files that are needed to
create binaries for the targeted Python version.

This can be done by editing the
``systemVariables-windows.properties`` (Windows) or ``systemVariables-linux.properties`` (Linux)
files. These files are located under ``parser/makLib`` folder.

First, The user is required to provide the path to the following folders:

- ``PYTHON_EXE_DIR``. This is the path to the Python executable directory (e.g. D:\\programs\\Anaconda3)

- ``CMD_TOOL``. This is the path to the build tools needed to compile the Python/C interface (e.g. C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\MSBuild\\Current\\Bin\\msbuild.exe)

Next, the user is required to run the ``createlib.py`` that is located in ``parser/makLib`` folder by
running the following command:

.. code-block:: none

  > python  parser/makLib/createlib.py -pv <python-version>

where ``python-version`` is the targeted Python version (e.g. ``38`` for Python 3.8).

This command will invoke the build tools that will create the Python binaries and copied them in the
appropriate Modelica library folder (``parser\libraries\modelica\SimulatorToFMU\Resources\Library``).
The created python binaries will be embedded in the FMU when the FMU will be created (see :doc:`build`).

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
  - give the unit of the variable (Currently only :term:`Modelica` units are supported) (Line 14)
  - give a start value for the input variable (This is optional) (Line 15)

To parametrize the ``ScalarVariable`` as an output variable, the user needs to

  - define the name of the variable (Line 18),
  - give a brief description of the variable (Line 19)
  - give the causality of the variable (``input`` for inputs, ``output`` for outputs) (Line 20)
  - define the type of variable (Currently only ``Real`` variables are supported) (Line 21)
  - give the unit of the variable (Currently only :term:`Modelica` units are supported) (Line 22)

.. note::

   If :term:`Modelica` units can't be used (Line 14 and Line 22), then remove the `unit` field from the input file
   when defining new ``ScalarVariable``.

Configuring the Python Wrapper Simulator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To export a Simulator as an FMU, the user needs to write the Python wrapper which will interface with the Simulator.
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
| ``write_results``                                  | A flag for writing the simulation results to a file located in    |
|                                                    | the working directory of the importing tool.                      |
+----------------------------------------------------+-------------------------------------------------------------------+
| ``memory``                                         | A variable that holds the memory of a Python object               |
|                                                    | This argument is required only if the simulator has               |
|                                                    | variables which have memory.                                      |
+----------------------------------------------------+-------------------------------------------------------------------+

If the simulator does not have memory, then the function ``simulator`` will be defined as

.. literalinclude:: ../../../parser/utilities/simulator_wrapper_no_memory.py
   :language: python
   :linenos:

.. note::

   - The function ``exchange`` must return a list of output values which matches the order of the output names.
   - If the simulator has memory, then the function ``exchange`` must also return the memory.
   - The function ``exchange`` can be used to invoke external programs/scripts which do not ship with the FMU.
     The external programs/scripts will have to be installed on the target machine where the
     FMU is run. See :doc:`build` for details on command line options.
   - Once ``simulator_wrapper.py`` is implemented, it must be saved under a name of the form ``"modelname"`` + ``"_wrapper.py"``,
     and its path used as required argument for ``SimulatorToFMU.py``.
