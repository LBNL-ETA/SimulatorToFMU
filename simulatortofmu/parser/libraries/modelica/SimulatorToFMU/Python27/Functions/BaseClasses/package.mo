within SimulatorToFMU.Python27.Functions;
package BaseClasses "Package with functions that call Python"
  extends Modelica.Icons.BasesPackage;

  class PythonObject
  "class used to create the external object: PythonObject"
    extends
        ExternalObject;
    function constructor
      "Construct an external object that can be used to store a Python object"
      input String patPytScri "Path to the Python main script";
      output PythonObject pytObj;
    external "C" pytObj = initPythonMemory(patPytScri)
        annotation (Library={"SimulatorToFMUPython27",  "python27"},
          LibraryDirectory={"modelica://SimulatorToFMU/Resources/Library"});
    annotation(Documentation(info="<html>
<p>
The function <code>constructor</code> is a C function that is called by a Modelica simulator
exactly once during the initialization.
The function returns the object <code>PythonObject</code> that
will be used to store a Python object and pass it from one invocation to another 
in the function
<a href=\"modelica://Buildings.Utilities.IO.Python27.Functions.BaseClasses.exchange\">
Buildings.Utilities.IO.Python27.Functions.BaseClasses.exchange</a>.
</p>
</html>", revisions="<html>
<ul>
<li>
January 31, 2018, by Michael Wetter and Thierry Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
    end constructor;

  function destructor "Release memory"
    input PythonObject pytObj;
    external "C" freePythonMemory(pytObj)
      annotation (Library={"SimulatorToFMUPython27",  "python27"},
        LibraryDirectory={"modelica://SimulatorToFMU/Resources/Library"});
  annotation(Documentation(info="<html>
<p>
Destructor that frees the memory of the object
<code>PythonObject</code>.
</p>
</html>", revisions="<html>
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

</html>",   revisions=
          "<html>
<ul>
<li>
January 31, 2018, by Michael Wetter and Thierry Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
  end PythonObject;

annotation (preferredView="info", Documentation(info="<html>
<p>
This package contains functions that call Python.
</p>
</html>"));
end BaseClasses;
