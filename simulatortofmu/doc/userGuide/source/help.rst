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

.. note::

  ``OPENMODELICALIBRARY`` is the path to the libraries which are required by OpenModelica to compile Modelica models.

Simulation failed when running ``Simulator.fmu``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the simulation failed with the exported FMU, check if 
the unzipped ``"modelname"`` + ``".scripts.zip"``, and  the subdirectories of ``"modelname"`` + ``".binaries.zip"``
were added to the ``PYTHONPATH``, and the system ``PATH`` respectively as described in :ref:`build_output`. 

.. note::

  Any software which is required to run the exported FMU will need to 
  be installed on the target machine where the FMU is run.

Simulation failed with Dymola FMUs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If an FMU exported using Dymola fails to run, check if the version of Dymola which exported the FMU had the ``Binary Model Export`` license.
The ``Binary Model Export`` license is required to export FMUs which can be run without requiring a Dymola runtime license.
You can also inspect the model description of the FMU to see if a Dymola runtime license is required to run the FMU.




