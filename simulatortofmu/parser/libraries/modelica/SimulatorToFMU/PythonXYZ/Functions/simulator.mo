within SimulatorToFMU.PythonXYZ.Functions;
function simulator "Function that communicates with the SimulatorToFMU Python API"
  extends Modelica.Icons.Function;
  input String moduleName
  "Name of the python module that contains the function";
  input String functionName=moduleName "Name of the python function";
  input BaseClasses.PythonObject obj "Memory that holds the Python object";
  input Boolean passMemoryObject
    "Set to true if the Python function returns and receives an object, see User's Guide";
  input String  conFilNam "Name of the python function";
  input Real    modTim "Model time";
  input Real    dblParVal[nDblPar] "Parameter variables values to send to SimulatorToFMU";
  input Real    dblInpVal[max(1, nDblInp)] "Input variables values to be sent to SimulatorToFMU";
  input String  dblParNam[nDblPar] "Parameter variables names to send to SimulatorToFMU";
  input String  dblOutNam[max(1, nDblOut)] "Output variables names to be read from SimulatorToFMU";
  input String  dblInpNam[max(1, nDblInp)] "Input variables names to be sent to SimulatorToFMU";
  input Integer nDblInp(min=0) "Number of double inputs to send to SimulatorToFMU";
  input Integer nDblOut(min=0) "Number of double outputs to read from SimulatorToFMU";
  input Integer nDblPar(min=0) "Number of double parameters to send to SimulatorToFMU";
  input Boolean resWri  "Flag for enabling results writing. 1: write results, 0: else";
  output Real   dblOutVal[max(1, nDblOut)] "Double output values read from SimulatorToFMU";
algorithm
  // Call the.simulator function
dblOutVal := BaseClasses.simulator(
      moduleName=moduleName,
      functionName=functionName,
      conFilNam=conFilNam,
      modTim=modTim,
      nDblInp=nDblInp,
      dblInpNam=dblInpNam,
      dblInpVal=dblInpVal,
      nDblOut=nDblOut,
      dblOutNam=dblOutNam,
      nDblPar=nDblPar,
      dblParNam=dblParNam,
      dblParVal=dblParVal,
      resWri=resWri,
      obj=obj,
      passMemoryObject=passMemoryObject);
end simulator;
