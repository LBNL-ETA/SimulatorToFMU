within SimulatorToFMU.Python37.Functions.BaseClasses;
class PythonObject
"class used to create the external object: PythonObject"
  extends ExternalObject;
  function constructor
    "Construct an external object that can be used to store a Python object"
    input String patResScri "Path to the Python main script";
    output PythonObject obj;
  external "C" obj = initPythonMemory(patResScri)
      annotation (Library={"SimulatorToFMUPython37",  "python37"},
        LibraryDirectory="modelica://SimulatorToFMU/Resources/Library");

  annotation(Documentation(info="<html>
<p>
The function <code>constructor</code> is a C function that is called by a Modelica simulator
exactly once during the initialization.
The function returns the object <code>PythonObject</code> that
will be used to store a Python object and pass it from one invocation to another 
in the function
<a href=\"modelica://SimulatorToFMU.Python37.Functions.BaseClasses.simulator\">
SimulatorToFMU.Python37.Functions.BaseClasses.simulator</a>.
</p>
</html>",
        revisions="<html>
<ul>
<li>
January 31, 2018, by Michael Wetter and Thierry Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
  end constructor;

function destructor "Release memory"
  input PythonObject obj;
  external "C" freePythonMemory(obj)
    annotation (Library={"SimulatorToFMUPython37",  "python37"},
      LibraryDirectory="modelica://SimulatorToFMU/Resources/Library");
annotation(Documentation(info="<html>
<p>
Destructor that frees the memory of the object
<code>PythonObject</code>.
</p>
</html>",
        revisions="<html>
<ul>
<li>
January 31, 2018, by Michael Wetter and Thierry Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
end destructor;
  annotation (Documentation(info=
                            "<html>
<p>
Class derived from <code>ExternalObject</code> having two local external functions
named <code>destructor</code> and <code>constructor</code>.
<p>
These functions create and release an external object that allows the storage
of a Python object.

</html>", revisions=
        "<html>
<ul>
<li>
January 31, 2018, by Michael Wetter and Thierry Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
end PythonObject;
