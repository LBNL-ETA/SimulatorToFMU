within SimulatorToFMU.Python35.Functions.Examples;
model Simulator "Test model for simulator functions"
  extends Modelica.Icons.Example;
  function replaceCharacters
    "Replace backward slashs with forward slashs"
    input String insStr "Input string";
    output String outStr "Output string";
  external"C" outStr = str_replace(
        insStr,
        "\\",
        "/") annotation (IncludeDirectory="modelica://SimulatorToFMU.Resources/C-Sources",
        Include="#include \"replaceCharacters.c\"");
  end replaceCharacters;

  function detectingOperatingSystem
    "Detect the operating system and return 0 for Windows 64, 
    1 for Windows 32, 2 for Linux 64, and 3 for Linux32"
    output Integer osFla "Return value";
  external"C" osFla = detectOperatingSystem() annotation (IncludeDirectory="modelica://SimulatorToFMU.Resources/C-Sources",
        Include="#include \"detectingOperatingSystem.c\"");
  end detectingOperatingSystem;

  Real yR1[1] "Real function value";
  Real yR2[2] "Real function value";
  // Parameters names can be empty.
  // Inputs and outputs cannot be empty.
  parameter String emptyDblParNam[0](each start="")
    "Empty list of parameters names";
  parameter Real emptyDblParVal[0]=zeros(0) "Empty vector of parameters values";
  parameter String pathToScript=Modelica.Utilities.Files.loadResource("modelica://SimulatorToFMU/Resources/Python-Sources/testSimulator.py");
  Boolean havePytPat "true if PYTHONPATH is already set by the user";
  String pytPatSimulatorToFMU "Path to the Python Simulator driver";
  String pytPat "Value of PYTHONPATH environment variable";
  String cleanPathScript "Path to script with backward  
    slashes replaced with forward slashes";
  Integer osFla=detectingOperatingSystem()
    "Flag for detecting operating system";

algorithm
  // Check the Operating system and change slashs characters
  if (osFla < 2) then
    cleanPathScript := replaceCharacters(pathToScript);
  else
    cleanPathScript := pathToScript;
  end if;
  (pytPatSimulatorToFMU,,):= Modelica.Utilities.Files.splitPathName(
    cleanPathScript);
  (pytPat,havePytPat):= Modelica.Utilities.System.getEnvironmentVariable("PYTHONPATH");
  if havePytPat then
    if (osFla < 2) then
      Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH",
        content=pytPatSimulatorToFMU + ";" + pytPat);
    else
      Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH",
        content=pytPatSimulatorToFMU + ":" + pytPat);
    end if;
  else
    Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH", content=
      pytPatSimulatorToFMU);
  end if;
  yR1 := SimulatorToFMU.Python35.Functions.simulator(
    moduleName="testSimulator",
    functionName="r1_r1",
    conFilNam="config.csv",
    modTim={time},
    nDblInp=1,
    dblInpNam={"u"},
    dblInpVal={15.0},
    nDblOut=1,
    dblOutNam={"y"},
    nDblPar=0,
    dblParNam=emptyDblParNam,
    dblParVal=emptyDblParVal,
    resWri={0});
  assert(abs(15 - yR1[1]) < 1e-5, "Error in function r1_r1");
  yR1 := SimulatorToFMU.Python35.Functions.simulator(
    moduleName="testSimulator",
    functionName="r2_r1",
    conFilNam="config.csv",
    modTim={time},
    nDblInp=2,
    dblInpNam={"u","u1"},
    dblInpVal={15.0,30.0},
    nDblOut=1,
    dblOutNam={"y"},
    nDblPar=0,
    dblParNam=emptyDblParNam,
    dblParVal=emptyDblParVal,
    resWri={0});
  assert(abs(45 - yR1[1]) < 1e-5, "Error in function r2_r1");
  yR1 := SimulatorToFMU.Python35.Functions.simulator(
    moduleName="testSimulator",
    functionName="par3_r1",
    conFilNam="config.csv",
    modTim={time},
    nDblInp=0,
    dblInpNam={""},
    dblInpVal={0},
    nDblOut=1,
    dblOutNam={"y"},
    nDblPar=3,
    dblParNam={"par1","par2","par3"},
    dblParVal={1.0,2.0,3.0},
    resWri={1});
  assert(abs(6 - yR1[1]) < 1e-5, "Error in function par3_r1");
  yR2 := SimulatorToFMU.Python35.Functions.simulator(
    moduleName="testSimulator",
    functionName="r1_r2",
    conFilNam="config.csv",
    modTim={time},
    nDblInp=1,
    dblInpNam={"u"},
    dblInpVal={30.0},
    nDblOut=2,
    dblOutNam={"y","y1"},
    nDblPar=0,
    dblParNam=emptyDblParNam,
    dblParVal=emptyDblParVal,
    resWri={0});
  assert(abs(yR2[1] - 30) + abs(yR2[2] - 60) < 1E-5, "Error in function r1_r2");
  yR2 := SimulatorToFMU.Python35.Functions.simulator(
    moduleName="testSimulator",
    functionName="r2p2_r2",
    conFilNam="config.csv",
    modTim={time},
    nDblInp=2,
    dblInpNam={"u","u1"},
    dblInpVal={1.0,2.0},
    nDblOut=2,
    dblOutNam={"y","y1"},
    nDblPar=2,
    dblParNam={"par1","par2"},
    dblParVal={1.0,10.0},
    resWri={1});
  assert(abs(yR2[1] - 1) + abs(yR2[2] - 20) < 1E-5, "Error in function r2p2_r2");
  // Change the PYTHONPATH back to what it was so that the function has no
  // side effects.
  if havePytPat then
    Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH", content=
      pytPat);
  else
    Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH", content="");
  end if;

  annotation (
    experiment(StopTime=1.0),
    __Dymola_Commands(file="modelica://SimulatorToFMU.Resources/Scripts/Dymola/Python35/Functions/Examples/Simulator.mos"
        "Simulate and plot"),
    Documentation(info="<html>
<p>
This example calls various functions in the Python module <code>testSimulator.py</code>.
It tests whether arguments and return values are passed correctly.
The functions in  <code>testSimulator.py</code> are very simple in order to test
whether they compute correctly, and whether the data conversion between Modelica and
Python is implemented correctly.
Each call to Python is followed by an <code>assert</code> statement which terminates
the simulation if the return value is different from the expected value.
</p>
</html>", revisions="<html>
<ul>
<li>
October 17, 2016, by Thierry S. Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
end Simulator;
