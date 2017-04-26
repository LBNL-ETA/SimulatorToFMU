.. highlight:: rest

.. _build:


Creating an FMU
===============

This chapter describes how to create a Functional Mockup Unit, starting from a Simulator XML input file.
It assumes you have followed the :doc:`installation` instructions, and that you have created the Simulator 
model description file  following the :doc:`bestPractice` guidelines.

Command-line use
^^^^^^^^^^^^^^^^

.. automodule:: parser.SimulatorToFMU


Outputs of SimulatorToFMU
^^^^^^^^^^^^^^^^^^^^^^^^^

The main output from running ``SimulatorToFMU.py`` consists of an FMU, named after the ``modelName`` specified in the input file.
The FMU is written to the current working directory, that is, in the directory from which you entered the command.

The FMU is complete and self-contained.

Any secondary output from running the SimulatorToFMU tools can be deleted safely.

Note that the FMU is a zip file.
This means you can open and inspect its contents.
To do so, it may help to change the "``.fmu``" extension to "``.zip``".

.. note:: 

   SimulatorToFMU detects the Python version used to export the FMU and 
   include binaries for Python 2.7 or Python 3.5. Hence it is important 
   to use the correct version of Python when invoking SimulatorToFMU.

Exporting a Simulator with Python 2.7
"""""""""""""""""""""""""""""""""""""

If SimulatorToFMU is run using Python 2.7, then 
SimulatorToFMU.py creates a  ``.zip`` file named
``Simulator.scripts.zip`` along with the FMU. 
The zip file contains the Python scripts needed to 
interface the Simulator. The unzipped folder must be added 
to the PYTHONPATH of the target machine where the FMU will be used.
This is because of an issue with Cython and the python interpreter 
which does not add the files on the path as expected. 
This step is not needed when using Python 3.5.x.

