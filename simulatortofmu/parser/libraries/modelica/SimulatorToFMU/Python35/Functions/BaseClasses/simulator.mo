within SimulatorToFMU.Python35.Functions.BaseClasses;
function simulator "Function that communicates with the SimulatorToFMU Python API"
  input String moduleName
    "Name of the python module that contains the function";
  input String functionName=moduleName "Name of the python function";
  input String  conFilNam "Name of the python function";
  input Real    modTim[1] "Model time";
  input Real    dblParVal[nDblPar] "Parameter variables values to send to SimulatorToFMU";
  input Real    dblInpVal[max(1, nDblInp)] "Input variables values to be sent to SimulatorToFMU";
  input String  dblParNam[nDblPar] "Parameter variables names to send to SimulatorToFMU";
  input String  dblOutNam[max(1, nDblOut)] "Output variables names to be read from SimulatorToFMU";
  input String  dblInpNam[max(1, nDblInp)] "Input variables names to be sent to SimulatorToFMU";
  input Integer nDblInp(min=0) "Number of double inputs to send to SimulatorToFMU";
  input Integer nDblOut(min=0) "Number of double outputs to read from SimulatorToFMU";
  input Integer nDblPar(min=0) "Number of double parameters to send to SimulatorToFMU";
  input Real    resWri[1]  "Flag for enabling results writing. 1: write results, 0: else";
  output Real    dblOutVal[max(1, nDblOut)] "Double output values read from SimulatorToFMU";
  external "C" modelicaToSimulator(moduleName,
                                    functionName,
                                    conFilNam,
                                    modTim,
                                    nDblInp,
                                    dblInpNam,
                                    dblInpVal,
                                    nDblOut,
                                    dblOutNam,
                                    dblOutVal,
                                    nDblPar,
                                    dblParNam,
                                    dblParVal,
                                    resWri)
    annotation (Library={"SimulatorToFMUPython35", "python35"},
      LibraryDirectory={"modelica://SimulatorToFMU/Resources/Library"},
      IncludeDirectory="modelica://SimulatorToFMU/Resources/C-Sources",
      Include="#include \"pythonWrapper.c\"");
  annotation (Documentation(info="<html>
<p>
This function exchanges data with a Simulator through its Python API.
See 
<a href=\"modelica://SimulatorToFMU.Python35.UsersGuide\">
SimulatorToFMU.Python35.UsersGuide</a>
for instructions, and 
<a href=\"modelica://SimulatorToFMU.Python35.Functions.Examples\">
SimulatorToFMU.Python35.Functions.Examples</a>
for examples.
</p>
</html>", revisions="<html>
<ul>
<li>
October 17, 2016, by Thierry S. Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
end simulator;
