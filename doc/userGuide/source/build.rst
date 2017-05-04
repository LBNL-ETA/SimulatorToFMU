.. highlight:: rest

.. _build:


Creating an FMU
===============

This chapter describes how to create a Functional Mockup Unit.
It assumes you have followed the :doc:`installation` instructions, and that you have created the Simulator 
model description file as well as the Python script required to interface the Simulator following the :doc:`bestPractice` guidelines.

Command-line use
^^^^^^^^^^^^^^^^

.. automodule:: parser.SimulatorToFMU


Outputs of SimulatorToFMU
^^^^^^^^^^^^^^^^^^^^^^^^^

The main output from running ``SimulatorToFMU.py`` consists of an FMU, named after the ``modelName`` specified in the input file.
The FMU is written to the current working directory, that is, in the directory from which you entered the command.

Any secondary output from running the SimulatorToFMU tools can be deleted safely.

Note that the FMU is a zip file.
This means you can open and inspect its contents.
To do so, it may help to change the "``.fmu``" extension to "``.zip``".

.. note::

  FMUs exported using the tested version OpenModelica tested needs 
  almost 10 times more compilation/simulation time compared to Dymola.

  FMUs exported using Dymola needs a Dymola runtime license to run.
  A Dymola runtime license is not be needed if the FMU is exported with 
  a version of Dymola which has the ``Binary Model Export`` license.



