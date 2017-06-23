.. highlight:: rest

.. _introduction:

Introduction
============

This user manual explains how to install and use SimulatorToFMU.

SimulatorToFMU is a software package written in Python which allows 
users to export a memoryless Python-driven simulation program or script 
as a :term:`Functional Mock-up Unit` (FMU) for  
model exchange or co-simulation using the :term:`Functional Mock-up Interface` (FMI) 
standard `version 1.0 or 2.0 <https://www.fmi-standard.org>`_.
This FMU can then be imported into a variety of simulation programs 
that support the import of Functional Mock-up Units.

A memoryless Python-driven simulation program/script 
is a simulation program which meets following requirements:
   
  - The simulation program/script can be invoked through a Python script.
  - The invocation of the simulation program/script is memoryless. That is, 
    the output of the simulation program at any invocation time ``t`` 
    depends only on the inputs at the time ``t``. 
  - The inputs and the outputs of the simulation program/script must be ``real`` numbers.
    
   

