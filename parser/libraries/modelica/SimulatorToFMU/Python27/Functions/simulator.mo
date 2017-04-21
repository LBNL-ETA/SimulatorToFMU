within SimulatorToFMU.Python27.Functions;
function simulator "Function that communicates with the SimulatorToFMU Python API"
  extends Modelica.Icons.Function;
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
  //   input Integer strLenRea(min=0)
  //     "Maximum length of each string that is read. If exceeded, the simulation stops with an error";
  output Real dblOutVal[max(1, nDblOut)] "Double output values read from SimulatorToFMU";
//   String pytPat "Value of PYTHONPATH environment variable";
//   String pytPatSimulatorToFMU "PYTHONPATH of SimulatorToFMU library";
//   Boolean havePytPat "true if PYTHONPATH is already set by the user";
  //--  String filNam = "file://Utilities/IO/Python27/UsersGuide/package.mo"
  //--    "Name to a file of the SimulatorToFMU library";
algorithm
//   // Get the directory to SimulatorToFMU/Resources/Python-Sources
//   //-- The lines below do not work in Dymola 2014 due to an issue with the loadResource
//   //-- (ticket #15168). This will be fixed in future versions.
//   //-- pytPatSimulatorToFMU := SimulatorToFMU.BoundaryConditions.WeatherData.BaseClasses.getAbsolutePath(uri=filNam);
//   //-- pytPatSimulatorToFMU := Modelica.Utilities.Strings.replace(
//   //--   string=pytPatSimulatorToFMU,
//   //--   searchString=filNam,
//   //--   replaceString="Resources/Python-Sources");
//   // The next line is a temporary fix for the above problem
//   pytPatSimulatorToFMU := "Resources/Python-Sources";
//   // Update the PYTHONPATH variable
//   (
// pytPat,havePytPat) := Modelica.Utilities.System.getEnvironmentVariable("PYTHONPATH");
//   if havePytPat then
//     Modelica.Utilities.Streams.print("Path is " + pytPat);
//  Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH",
//     content=pytPat + ":" + pytPatSimulatorToFMU);
//
//   else
//  Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH",
//     content=pytPatSimulatorToFMU);
//         Modelica.Utilities.Streams.print("Simulator is " + pytPatSimulatorToFMU);
//   end if;
  // Call the exchange function
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
      resWri=resWri);
  // Change the PYTHONPATH back to what it was so that the function has no
  // side effects.
//   if havePytPat then
//  Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH",
//     content=pytPat);
//   else
//  Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH",
//     content="");
//   end if;
annotation (Documentation(info="<html>
<p>
This function is a wrapper for 
<a href=\"modelica://SimulatorToFMU.Python27.Functions.BaseClasses.simulator\">
SimulatorToFMU.Python27.Functions.BaseClasses.simulator</a>.
It adds the directory <code>modelica://SimulatorToFMU/Resources/Python-Sources</code>
to the environment variable <code>PYTHONPATH</code>
prior to calling the function that exchanges data with Python.
After the function call, the <code>PYTHONPATH</code> is set back to what
it used to be when entering this function.
See 
<a href=\"modelica://SimulatorToFMU.Python27.UsersGuide\">
SimulatorToFMU.Python27.UsersGuide</a>
for instructions, and 
<a href=\"modelica://SimulatorToFMU.Python27.Functions.Examples\">
SimulatorToFMU.Python27.Functions.Examples</a>
for examples.
</p>
</html>",
        revisions="<html>
<ul>
<li>
October 17, 2016, by Thierry S. Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
end simulator;
