SimulatorToFMU
--------------

Overview
^^^^^^^^

SimulatorToFMU is a software package written in Python which allows 
users to export a memoryless Python-driven simulation program or script 
as a Functional Mock-up Unit (FMU) for  
model exchange or co-simulation using the Functional Mock-up Interface (FMI) 
standard version 1.0 or 2.0 (https://www.fmi-standard.org).
This FMU can then be imported into a variety of simulation programs 
that support the import of Functional Mock-up Units.

A memoryless Python-driven simulation program/script 
is a simulation program which meets following requirements:
   
- The simulation program/script can be invoked through a Python script.
- The invocation of the simulation program/script is memoryless. That is, 
  the output of the simulation program at any invocation time ``t`` 
  depends only on the inputs at the time ``t``. 
- The inputs and the outputs of the simulation program/script must be ``real`` numbers.

Requirements
^^^^^^^^^^^^
- `jinja2 <https://pypi.python.org/pypi/Jinja2>`_
- `lxml <http://pypi.python.org/pypi/lxml>`_


Installation
^^^^^^^^^^^^
To install run

.. code:: text

   pip install simulatortofmu

For more information visit the development page at `https://github.com/LBNL-ETA/SimulatorToFMU <https://github.com/LBNL-ETA/SimulatorToFMU>`_

The license is at `LICENSE.txt <https://github.com/tsnouidui/SimulatorToFMU/blob/master/simulatortofmu/LICENSE.txt>`_





