.. highlight:: rest

.. _bestPractice:


Best Practice
=============

This section explains to users the best practice in configuring a CYMDIST XML input file 
for an FMU. 

To export CYMDIST as an FMU, the user needs to write an XML file which contains the list 
of inputs, outputs and parameters of the FMU. The XML snippet below shows how a user has to write such an input file.
A template named ``CYMDISTModeldescritpion.xml`` which shows such a file is provided in the ``parser\utilities`` installation folder of CYMDISTToFMU. 
This template should be adapted to create new XML input file.

The following snippet shows an input file where the user defines 6 inputs and 6 output variables.

.. literalinclude:: ../../../parser/utilities/CYMDISTModelDescription.xml
   :language: xml
   :linenos:

To create such an input file, the user needs to specify the name of the FMU (Line 5). 
This is the ``modelName`` which should be unique.
The user then needs to define the inputs and outputs of the FMUs. 
This is done by adding ``ScalarVariable`` into the list of ``ModelVariables``.

To parametrize the ``ScalarVariable`` as an input variable, the user needs to

  - define the name of the variable (Line 10), 
  - give a brief description of the variable (Line 11)
  - give the causality of the variable (``input`` for inputs, ``output`` for outputs) (Line 12)
  - define the type of variable (Currently only ``Real`` variables are supported) (Line 13)
  - give the unit of the variable (Currently only valid Modelica units are supported) (Line 14)
  - give a start value for the input variable (This is optional) (Line 15)

To parametrize the ``ScalarVariable`` as an output variable, the user needs to

  - define the name of the variable (Line 58), 
  - give a brief description of the variable (Line 59)
  - give the causality of the variable (``input`` for inputs, ``output`` for outputs) (Line 60)
  - define the type of variable (Currently only ``Real`` variables are supported) (Line 61)
  - give the unit of the variable (Currently only valid Modelica units are supported) (Line 62)
   
 
