.. highlight:: rest

.. _installation:

Installation and Configuration
==============================

This chapter describes how to install, configure, and uninstall SimulatorToFMU on Windows and Linux operating systems. SimulatorToFMU is currently not supported on Mac OS.


Software requirements
^^^^^^^^^^^^^^^^^^^^^

To export a Simulator as an FMU, SimulatorToFMU needs:

1. Python and following dependencies:

   - jinja2 
   - lxml 

2. Modelica parser

3. C-Compiler

SimulatorToFMU has been tested with:

- Python 2.7.12 (Linux) and 2.7.13 (Windows) 
- Three Modelica parsers

  - Dymola 2018 on Windows and Linux
  - JModelica 2.0 on Windows, and JModelica trunk version 9899 on Linux
  - OpenModelica 1.11.0 on Windows

- C-Compiler: Microsoft Visual Studio 10 Professional

.. _installation directory:

Installation
^^^^^^^^^^^^

To install SimulatorToFMU, proceed as follows:

1. Add following folders to your system path: 

 - Python installation folder (e.g. ``C:\Python27``)
 - Python scripts folder (e.g. ``C:\Python27\Scripts``), 
 - Dymola executable folder (e.g. ``C:\Program Files(x86)\Dymola2018\bin``)
 - JModelica installation folder (e.g. ``C:\JModelica.org-2.0``)
 - OpenModelica executable folder (e.g. ``C:\OpenModelica1.11.0-32bit\bin``)

   
 You can add folders to your system path by performing following steps on Windows 8 or 10:

 - In Search, search for and then select: System (Control Panel)
     
 - Click the Advanced system settings link.
     
 - Click Environment Variables. In the section System Variables, find the PATH environment variable and select it. Click Edit. 
     
 - In the Edit System Variable (or New System Variable) window, specify the value of the PATH environment variable (e.g. ``C:\Python27``, ``C:\Python27\Scripts``). Click OK. Close all remaining windows by clicking OK.
     
 - Reopen Command prompt window for your changes to be active.
    
 To check if the variables have been correctly added to the system path on Windows, type ``python``, ``dymola``, ``pylab``, or ``omc``
 into a command prompt to see if the right version of Python, Dymola, JModelica, or OpenModelica starts up.

 .. note:: 

    - To avoid adding Dymola, JModelica, or OpenModelica to the system path, provide the path to the executables to SimulatorToFMU.py. See :ref:`build_cmd` for the lists of arguments of SimulatorToFMU.

    - SimulatorToFMU sets the hidden Dymola 2018's flag ``Advanced.AllowStringParametersForFMU`` to ``true`` when exporting a simulation program/script as an FMU. The flag is not available in older versions of Dymola. The flag is required to allow a master algorithm to set the path to the configuration file of an FMU. See section :ref:`build_cmd` for more details.

2. Install SimulatorToFMU by running 

 .. code-block:: none

    > pip install --user SimulatorToFMU

 .. note::

   Use the ``--user`` command line option to install SimulatorToFMU so it can be installed in your Python 2.7 user installation directory and can write files to your disk. The Python 2.7 user installation directory is typically ``C:\Users\YourUserName\AppData\Roaming\Python\Python27\site-packages`` on Windows, and ``/home/YourUserName/.local/lib/python2.7/site-packages`` on Linux where ``YourUserName`` is your system login user name. 

 
The installation directory should contain the following subdirectories:

 - ``bin/``
   (Scripts for running unit tests)

 - ``doc/``
   (Documentation sources)

 - ``fmus/``
   (FMUs folder)

 - ``parser/``
   (Python scripts, Modelica templates and XML validator files)
   

UnitTests
^^^^^^^^^

To test your installation run from the installation ``bin`` folder

.. code-block:: none

    > python runUnitTest.py 
    

Uninstallation
^^^^^^^^^^^^^^

To uninstall SimulatorToFMU, run

.. code-block:: none

    > pip uninstall SimulatorToFMU
