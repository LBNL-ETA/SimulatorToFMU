.. highlight:: rest

.. _introduction:

Introduction
============

This user manual explains how to install and use SimulatorToFMU.

SimulatorToFMU is a software package written in Python which allows
users to export a Python-driven simulation program or script
as a :term:`Functional Mock-up Unit` (FMU) for
model.simulator or co-simulation using the :term:`Functional Mock-up Interface` (FMI)
standard `version 1.0 or 2.0 <https://www.fmi-standard.org>`_.
This FMU can then be imported into a variety of simulation programs
that support the import of Functional Mock-up Units.
In the remainder of this document, we define a Python-driven simulation program,
and a Python script as a Simulator.

.. note::

  SimulatorToFMU generates FMUs that use the Python/C API for interfacing with the simulators.
