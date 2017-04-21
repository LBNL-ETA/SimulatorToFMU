.. highlight:: rest

.. _usage:

Usage of CYMDIST as an FMU
=============================

The following requirements must be met to import and run a CYMDIST FMU:

1. Python 3.4 must be installed. This is needed by the master algorithm :term:`PyFMI`.

2. CYME version 7.2 must be installed. CYME can be downloaded from `www.cyme.com <https://www.cyme.com>`_.

3. The ``fmu_code`` functions directory must be added to the ``PYTHONPATH``.  
   This directory contains functions needed at runtime by the CYMDIST FMU.
   The ``fmu_code`` functions folder can be found at the top level of
   the distribution folder of CyDER. It is in ``web\docker_django\worker\simulation``. 

   To add the ``fmu_code`` functions folder to the ``PYTHONPATH``:

   - In Search, search for and then select: System (Control Panel).
     
   - Click the Advanced system settings link.
     
   - Click Environment Variables. In the section System Variables, 
     find a variable named ``PYTHONPATH`` environment variable and select it. 
	 If the variable does not exist, create it. Click Edit. 
     
   - In the Edit System Variable (or New System Variable) window, 
     specify the value of the PYTHONPATH environment variable 
     which should be in our case the full path to
     ``web\docker_django\worker\simulation\fmu_code``. 

4. The CYMDIST Python API directory must be added to the ``PYTHONPATH``. 
   This directory contains scripts needed at runtime by the CYMDIST FMU. 

   The CYMDIST Python API directory is in the installation folder of CYME. 
   It can typically be found in ``path_to_CYME\CYME\cympy``, where ``path_to_CYME`` 
   is the path to the installation folder of CYME 7.2.

 To add the CYMDIST Python API scripts folder to the ``PYTHONPATH``, 
 add ``path_to_CYME\CYME`` to the ``PYTHONPATH``.
 Note that ``cympy`` is not included in the name of the variable.   

5. The CYMDIST installation directory must be added to the system ``PATH``. 
   This directory contains runtime DLLS (``mkl_core.dll``, ``mkl_def.dll``) 
   that are needed at runtime by the CYMDIST FMU. 

   The CYMDIST installation directory is typically found in ``path_to_CYME\CYME\`, 
   where ``path_to_CYME`` is the path to the installation folder of CYME 7.2.

6. Upon request, the simulation results are saved in a result file which 
   is created in the current working directory. 
   The name of the result file is ``xxx_result_.pickle``, where xxx 
   is the FMU model name as defined in the XML input file.






