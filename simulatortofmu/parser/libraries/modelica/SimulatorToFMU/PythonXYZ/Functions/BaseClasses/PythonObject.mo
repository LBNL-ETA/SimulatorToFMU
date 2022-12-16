within SimulatorToFMU.PythonXYZ.Functions.BaseClasses;
class PythonObject
"class used to create the external object: PythonObject"
  extends ExternalObject;
  function constructor
    "Construct an external object that can be used to store a Python object"
    input String patResScri "Path to the Python main script";
    output PythonObject obj;
  external "C" obj = initPythonMemory(patResScri)
      annotation (Library={"SimulatorToFMUPythonXYZ",  "pythonXYZ"},
        LibraryDirectory="modelica://SimulatorToFMU/Resources/Library");
  end constructor;

function destructor "Release memory"
  input PythonObject obj;
  external "C" freePythonMemory(obj)
    annotation (Library={"SimulatorToFMUPythonXYZ",  "pythonXYZ"},
      LibraryDirectory="modelica://SimulatorToFMU/Resources/Library");
end destructor;
end PythonObject;
