SimulatorToFMU
--------------

|Running Tests for SimulatorToFMU|

.. |Running Tests for SimulatorToFMU| image:: https://github.com/LBNL-ETA/SimulatorToFMU/actions/workflows/unitTest.yml/badge.svg
   :target: https://github.com/LBNL-ETA/SimulatorToFMU/actions/workflows/unitTest.yml


Overview
^^^^^^^^

SimulatorToFMU is a software package written in Python which allows 
users to export a Python-driven simulation program or a Python script 
as a Functional Mock-up Unit (FMU) for  
model-exchange or co-simulation using the Functional Mock-up Interface (FMI) 
standard version 1.0 or 2.0 (https://www.fmi-standard.org).
This FMU can then be imported into a variety of simulation programs 
that support the import of Functional Mock-up Units.

.. note::

  SimulatorToFMU generates FMUs that use the Python/C API for interfacing 
  with Python-driven simulation programs and Python scripts.

Requirements
^^^^^^^^^^^^
- `jinja2 <https://pypi.python.org/pypi/Jinja2>`_
- `lxml <http://pypi.python.org/pypi/lxml>`_


Installation
^^^^^^^^^^^^
To install SimulatorToFMU, clone the master branch of the development repository locally or run

.. code:: text

   pip install --user git+https://github.com/LBNL-ETA/SimulatorToFMU.git

For more information visit the development page at `https://github.com/LBNL-ETA/SimulatorToFMU <https://github.com/LBNL-ETA/SimulatorToFMU>`_

The license is at `LICENSE.txt <https://github.com/LBNL-ETA/SimulatorToFMU/blob/master/simulatortofmu/LICENSE.txt>`_

Help
^^^^

- For support questions use the `SimulatorToFMU Forum <https://groups.google.com/forum/#!forum/simulatortofmu>`_
- For bug reports use the `SimulatorToFMU GitHub Issues <https://github.com/LBNL-ETA/SimulatorToFMU/issues>`_





