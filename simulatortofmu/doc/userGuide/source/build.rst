.. highlight:: rest

.. _build:


Creating an FMU
===============

This chapter describes how to create a Functional Mockup Unit.
It assumes you have followed the :doc:`installation` instructions, and that you have created the Simulator 
model description file as well as the Python script required to interface the Simulator following the :doc:`bestPractice` guidelines.

.. _build_cmd:

Command-line use
^^^^^^^^^^^^^^^^

.. automodule:: parser.SimulatorToFMU

.. _build_output:

Outputs of SimulatorToFMU
^^^^^^^^^^^^^^^^^^^^^^^^^

The main output from running ``SimulatorToFMU.py`` consists of an FMU named 
after the ``modelName`` specified in the input file, and a zip 
file called ``"modelname"`` + ``".scripts.zip"``. That is, if the ``modelName``
is called ``Simulator``, then the outputs of ``SimulatorToFMU``
will be ``Simulator.fmu`` and ``Simulator.scripts.zip``.

The FMU and the zip file are written to the current 
working directory, that is, in the directory from which you entered the command.

``"modelname"`` + ``".scripts.zip"`` contains the Python scripts that are needed to 
interface with the Simulator. The unzipped folder must be added 
to the ``PYTHONPATH`` of the target machine where the FMU will be used.

Any secondary output from running the SimulatorToFMU tools can be deleted safely.

Note that the FMU itself is a zip file.
This means you can open and inspect its contents.
To do so, it may help to change the "``.fmu``" extension to "``.zip``".

.. note::

  - FMUs exported using OpenModelica 1.11.0 needs significantly 
    longer compilation/simulation time compared to the tested versions 
    of Dymola and JModelica.

  - FMUs exported using Dymola 2017 FD01 needs a Dymola runtime license to run.
    A Dymola runtime license is not be needed if the FMU is exported with 
    a version of Dymola which has the ``Binary Model Export`` license.



