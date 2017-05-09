.. highlight:: rest

.. _installation:

Installation and Configuration
==============================

This chapter describes how to install, configure, and uninstall SimulatorToFMU.


Software requirements
^^^^^^^^^^^^^^^^^^^^^

To export a Simulator as an FMU, SimulatorToFMU needs:

1. Python and following dependencies:

   - jinja2 

   - lxml 

2. Modelica parser

3. C-Compiler

SimulatorToFMU has been tested with:

  - Python 2.7.13
  - Python 3.5.0 
  - Dymola 2017 FD01 (Modelica parser, Windows and Linux)
  - OpenModelica 1.11.0 (Modelica parser, Windows)
  - Microsoft Visual Studio 10 Professional (C-Compiler) 

.. note:: 

   SimulatorToFMU can use OpenModelica and Dymola to export a Simulator as an FMU. 
   However OpenModelica 1.11.0 (on Windows) and Dymola 2017 FD01 (on Linux) do not copy all required libraries dependencies to the FMU.
   As a workaround, SimulatorToFMU checks if there are missing libraries dependencies and copies the dependencies to the FMU.

.. _installation directory:

Installation
^^^^^^^^^^^^

To install SimulatorToFMU, proceed as follows:

1. Add following folders to your system path: 

 - Python installation folder (e.g. ``C:\Python35``)
 - Python scripts folder (e.g. ``C:\Python35\Scripts``), 
 - Dymola executable folder (e.g. ``C:\Program Files(x86)\Dymola2017 FD01\bin``)
 - OpenModelica executable folder (e.g. ``C:\OpenModelica1.11.0-32bit\``)

   
 You can add folders to your system path by performing following steps on Windows 8 or 10:

 - In Search, search for and then select: System (Control Panel)
     
 - Click the Advanced system settings link.
     
 - Click Environment Variables. In the section System Variables, find the PATH environment variable and select it. Click Edit. 
     
 - In the Edit System Variable (or New System Variable) window, specify the value of the PATH environment variable (e.g. ``C:\Python35``, ``C:\Python35\Scripts``). Click OK. Close all remaining windows by clicking OK.
     
 - Reopen Command prompt window for your changes to be active.
    
 To check if the variables have been correctly added to the system path, type ``python``, ``dymola``, or ``omc``
 into a command prompt to see if the right version of Python, Dymola or OpenModelica starts up.


2. To install SimulatorToFMU, run 

  .. code-block:: none

    > pip install SimulatorToFMU
 
  The installation directory should contain the following subdirectories:

    - ``bin/``
      (Python scripts for running unit tests)

    - ``doc/``
      (Documentation)

    - ``fmus/``
      (FMUs folder)

    - ``parser/``
      (Python scripts, Modelica templates and XML validator files)


Uninstallation
^^^^^^^^^^^^^^

To uninstall SimulatorToFMU, run

.. code-block:: none

    > pip uninstall SimulatorToFMU
