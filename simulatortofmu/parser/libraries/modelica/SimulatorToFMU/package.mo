within ;
package SimulatorToFMU "Library with models for building energy and control systems"
  extends Modelica.Icons.Package;




annotation (
preferredView="info",
version="4.0.0",
versionDate="2016-03-29",
dateModified="2016-03-29",
uses(Modelica(version="3.2.2")),
conversion(
 from(version={"3.0.0", "4.0.0"},
      script="modelica://SimulatorToFMU.Resources/Scripts/Dymola/ConvertSimulatorToFMU.from_3.0_to_4.0.mos")),
revisionId="$Id$",
preferredView="info",
Documentation(info="<html>
<p>The <code>SimulatorToFMU</code> library contains 
models for exporting the distribution tool 
<a href=\"http://www.cyme.com\">SimulatorToFMU</a> 
as a Functional Mock-up Unit. </p>
</html>"));
end SimulatorToFMU;
