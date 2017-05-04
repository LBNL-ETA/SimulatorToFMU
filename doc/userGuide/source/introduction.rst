.. highlight:: rest

.. _introduction:

Introduction
============

This user manual explains how to install and use SimulatorToFMU.

SimulatorToFMU is a software package written in Python which allows 
users to export a memoryless Python-driven simulation program or script 
as a :term:`Functional Mock-up Unit` (FMU) for  
model exchange or co-simulation using the :term:`Functional Mock-up Interface` (FMI) 
standard `version 2.0 <https://svn.modelica.org/fmi/branches/public/specifications/v2.0/FMI_for_ModelExchange_and_CoSimulation_v2.0.pdf>`_.
This FMU can then be imported into a variety of simulation programs 
that support the import of the Functional Mock-up Interface.

A memoryless Python-driven simulation program/script 
is a simulation program which meets following requirements:
   
  - The simulation program/script can be invoked through a Python script.
  - The invocation of the simulation program/script is memoryless. That is, 
    the output of the simulation program at any invocation time ``t`` 
    depends only on the inputs at the time ``t``. 
  - The inputs and the outputs of the simulation program/script must be of type ``Float``.

