within SimulatorToFMU.Python27.Functions;
package Examples "Collection of models that illustrate model use and test models"
  extends Modelica.Icons.ExamplesPackage;

  model SimulatorWithpassMemoryObject
    "Test model for simulator functions with memory"
    extends Modelica.Icons.Example;
    parameter Boolean passMemoryObject = true
      "Set to true if the Python function returns and receives an object, see User's Guide";
    // Parameters names can be empty.
    // Inputs and outputs cannot be empty.
    parameter String emptyDblParNam[0](each start="")
      "Empty list of parameters names";
    parameter Real emptyDblParVal[0]=zeros(0) "Empty vector of parameters values";
    parameter String patResScri=Modelica.Utilities.Files.loadResource(
      "modelica://SimulatorToFMU/Resources/Python-Sources/testSimulator.py")
      "Path to the main Python script";
    SimulatorToFMU.Python27.Functions.BaseClasses.PythonObject obj=
      SimulatorToFMU.Python27.Functions.BaseClasses.PythonObject(patResScri=patResScri);
    Real yR1[1] "Real function value";
  algorithm
    yR1 := SimulatorToFMU.Python27.Functions.simulator(
      moduleName="testSimulator",
      functionName="r1_r1PassMemoryObject",
      conFilNam="config.csv",
      modTim=time,
      nDblInp=1,
      dblInpNam={"u"},
      dblInpVal={15.0},
      nDblOut=1,
      dblOutNam={"y"},
      nDblPar=0,
      dblParNam=emptyDblParNam,
      dblParVal=emptyDblParVal,
      resWri=false,
      obj=obj,
      passMemoryObject=passMemoryObject);
      //assert(abs(28 - yR1[1]) < 1e-5, "Error in function r1_r1passMemoryObject");
    annotation (
      experiment(StopTime=1.0),
      __Dymola_Commands(file="modelica://SimulatorToFMU.Resources/Scripts/Dymola/Python27/Functions/Examples/SimulatorWithpassMemoryObject.mos"
          "Simulate and plot"),
      Documentation(info="<html>
<p>
This example calls a function in the Python module <code>testSimulator.py</code>.
It tests whether arguments and return values are passed correctly.
The functions in  <code>testSimulator.py</code> are very simple in order to test
whether they compute correctly, and whether the data conversion between Modelica and
Python is implemented correctly.
Each call to Python is followed by an <code>assert</code> statement which terminates
the simulation if the return value is different from the expected value.
</p>
</html>",   revisions="<html>
<ul>
<li>
February 05, 2018, by Thierry S. Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
  end SimulatorWithpassMemoryObject;

annotation (preferredView="info", Documentation(info="<html>
<p>
This package contains examples for the use of models that can be found in
<a href=\"modelica://SimulatorToFMU.Python27.Functions\">
SimulatorToFMU.Python.Functions</a>.
</p>
<p>
The examples demonstrate how to call Python functions from Modelica.
</p>
</html>"));
end Examples;
