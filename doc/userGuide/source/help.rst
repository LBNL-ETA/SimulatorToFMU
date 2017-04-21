Help
====

Running PyFMI with Python 3.4 on Windows 32 bit
-----------------------------------------------
:term:`PyFMI` is a python package which can be used to import and run a CYMDIST FMU. 
In :term:`PyFMI` version 2.3.1, a master algorithm was added to import and 
link multiple FMUs for co-simulation. At time of writing, there was no :term:`PyFMI` 
2.3.1 executable available for Python 3.4 for Windows 32bit (See `PyPyi <https://pypi.python.org/pypi/PyFMI>`_.).
The next steps describe requirements and steps to perform to compile :term:`PyFMI` version 2.3.1 from source.

.. note::
  
  To avoid having to recompile :term:`PyFMI` dependent libraries from source, 
  we recommend to use pre-compiled Windows binaries whenever available.

Requirements
++++++++++++

The next table shows the list of Python modules and softwares used to compile version 2.3.1 of PyFMI from source
so it can run with Python 3.4 on Windows 32 bit.

Install PyFMI dependencies with

   .. code-block:: none
   
      pip install -r dev/master/bin/pyfmi-dependencies.txt

Below is a table with dependencies which fail to install using pip. 
For those, we recommend to use the MS Windows installer directly.

+---------------+---------------------------------------------+-----------------------------------------------------------+
| Modules       | Version                                     | Link                                                      |
+===============+=============================================+===========================================================+
| FMI Library   | 2.0.2 (source)                              | http://www.jmodelica.org/FMILibrary                       |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| Scipy         | 0.16.1                                      | https://sourceforge.net/projects/scipy/files/scipy/0.16.1 |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| lxml          | 3.4.4                                       | https://pypi.python.org/pypi/lxml/3.4.4                   |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| Assimulo      | 2.7b1                                       | https://pypi.python.org/pypi/Assimulo/2.7b1               |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| PyFMI         | 2.3.1 (source)                              | https://pypi.python.org/pypi/PyFMI                        |
+---------------+---------------------------------------------+-----------------------------------------------------------+

.. note::

   :term:`PyFMI` needs a C-compiler to compile the source codes. We used the Microsoft Visual Studio 10 Professional.


Compilation
+++++++++++

To compile :term:`PyFMI` from source, run

.. code-block:: none

  python setup.py install --fmil-home=path_to_FMI_Library\

where ``path_to_FMI_Library\`` is the path to the FMI library.

To use :term:`PyFMI` as a master algorithm to couple a CYMDIST FMU with GridDyn FMU,
we refer to the documentation located in ``fmu/master/doc/userGuide``.


