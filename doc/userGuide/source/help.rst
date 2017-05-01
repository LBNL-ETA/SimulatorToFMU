.. highlight:: rest

.. _help:

Help
====

This chapter lists potential issues encountered when using SimulatorToFMU.


Simulation failed with Dymola FMUs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If an FMU exported using Dymola fails to run, check if the version of Dymola which exported the FMU had the ``Binary Model Export`` license.
The ``Binary Model Export`` license is required to export FMUs which can be run without requiring a Dymola runtime license.
You can also inspect the model description of the FMU to see if a Dymola runtime license is required to run the FMU.

Compilation failed with OpenModelica
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the compilation of Modelica models fails with OpenModelica, check if the ``OPENMODELICALIBRARY`` is defined in the Windows ``Environment Variables``.

``OPENMODELICALIBRARY`` is the path to the libraries which are required by OpenModelica to compile Modelica models.


