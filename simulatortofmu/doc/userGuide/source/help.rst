.. highlight:: rest

.. _help:

Help
====

This chapter lists potential issues encountered when using SimulatorToFMU.

Compilation failed with Dymola
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the export of the Simulator failed when compiling the model with Dymola, comment out ``"exit()"`` in 
``parser/utilities/SimulatorModelica_Template_Dymola.mos`` with ``"//exit()"``, and re-run ``SimulatorToFMU.py`` 
to see why the complation has failed.

Compilation failed with OpenModelica
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the export of the Simulator failed when compiling the model with OpenModelica, 
check if the variable ``OPENMODELICALIBRARY`` is defined in the Windows ``Environment Variables``.

``OPENMODELICALIBRARY`` is the path to the libraries which are required by OpenModelica to compile Modelica models.

Simulation failed in OpenModelica and Dymola FMUs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the simulation failed with the exported FMU, check if the ``"modelname"`` + ``".scripts.zip"``
was added to the ``PYTHONPATH`` as described in :ref:`build_output`. Please note that any software
which is required to run the exported FMU will need to be installed on the target machine where the FMU is run.

Simulation failed with Dymola FMUs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If an FMU exported using Dymola fails to run, check if the version of Dymola which exported the FMU had the ``Binary Model Export`` license.
The ``Binary Model Export`` license is required to export FMUs which can be run without requiring a Dymola runtime license.
You can also inspect the model description of the FMU to see if a Dymola runtime license is required to run the FMU.




