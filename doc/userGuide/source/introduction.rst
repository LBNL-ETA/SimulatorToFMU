.. highlight:: rest

.. _introduction:

Introduction
============

This user manual explains how to install and use SimulatorToFMU.

SimulatorToFMU is a software package written in Python which allows 
users to export any memoryless Python-based simulation program which can be interfaced 
through a Python API  as a :term:`Functional Mock-up Unit` (FMU) for  
model Exchange or co-Simulation using the :term:`Functional Mock-up Interface` (FMI) 
standard `version 2.0 <https://svn.modelica.org/fmi/branches/public/specifications/v2.0/FMI_for_ModelExchange_and_CoSimulation_v2.0.pdf>`_.
This FMU can then be imported into a variety of simulation programs 
that support the import of the Functional Mock-up Interface.

.. note::  
   
   A memoryless Python-based simulation is a simulation program which meets following requirements:
   
   - The simulation program can be invoked through a Python script.
   - The invocation of the simulation program is memoryless. That is, 
     the output of the simulation program at any invocation time ``t`` 
     depends only on the inputs at the time ``t``. 


