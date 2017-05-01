.. highlight:: rest

.. _installation:

Installation and Configuration
==============================

This chapter describes how to install, configure and uninstall SimulatorToFMU.


Software requirements
^^^^^^^^^^^^^^^^^^^^^

To export a Simulator as an FMU, SimulatorToFMU needs:

1. Python 

2. jinja2

3. lxml

4. Modelica compiler

SimulatorToFMU has been tested with:

  - Python 2.7.13
  - Python 3.5.0 
  - Dymola 2017 FD01 (Windows and Linux)
  - OpenModelica 1.11.0 (Windows) 

.. note:: 

   SimulatorToFMU can use OpenModelica and Dymola to export a Simulator as an FMU. 
   
   However OpenModelica (on sWindows) and Dymola (on Linux) do not copy all required libraries dependencies to the FMU.

   As a workaround, SimulatorToFMU checks if there are missing libraries dependencies and copies the dependencies to the FMU.

.. _installation directory:

Installation
^^^^^^^^^^^^

To install SimulatorToFMU, proceed as follows:

1. Download the installation file from the :doc:`download` page.

2. Unzip the installation file into any subdirectory (hereafter referred to as the "installation directory").
 

The installation directory should contain the following subdirectories:

  - ``bin/``
    (Python scripts for running unit tests)

  - ``doc/``
    (Documentation)

  - ``fmus/``
    (FMUs folder)

  - ``parser/``
    (Python scripts, Modelica templates and XML validator files)
    

3. Add following folders to your system path: 

 - Python installation folder (e.g. ``C:\Python35``)
 - Python scripts folder (e.g. ``C:\Python35\Scripts``), 
 - Dymola executable folder (e.g. ``C:\Program Files(x86)\Dymola2017 FD01\bin64``)
 - OpenModelica executable folder (e.g. ``C:\OpenModelica1.11.0-32bit\``)

   .. note:: 

     You can add folders to your system path by performing following steps on Windows 8 or 10:

     In Search, search for and then select: System (Control Panel)
     
     Click the Advanced system settings link.
     
     Click Environment Variables. In the section System Variables, find the PATH environment variable and select it. Click Edit. 
     
     In the Edit System Variable (or New System Variable) window, specify the value of the PATH environment variable (e.g. ``C:\Python35``, ``C:\Python35\Scripts``). Click OK. Close all remaining windows by clicking OK.
     
     Reopen Command prompt window for your changes to be active.
    
   To check if the variables have been correctly added to the system path, type ``python``, ``dymola``, or ``omc``
   into a command prompt to see if the right version of Python, Dymola or OpenModelica starts up.


4. Install Python dependencies by running

   .. code-block:: none
   
      pip install -r bin/simulatortofmu-requirements.txt



Uninstallation
^^^^^^^^^^^^^^

To uninstall SimulatorToFMU, delete the `installation directory`_.
