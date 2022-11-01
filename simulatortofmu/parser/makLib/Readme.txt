# README TO CREATE DLL FOR NEWEST VERSION OF PYTHON

These steps should be followed prior to invoking the SimulatorToFMU.py script
This script has been included starting in the version 3.8 of Python

1. Edit systemVariables-windows.properties to include the path of
Python (executable). The Python executable folder also includes the Python DLL (e.g. python38.dll).
2. Edit the path to msbuild. msbuild will be used to compile the FMU C-code
using visual studio express.
3. Run Python createlib.py. This script will create a configuration file which
then be run using msbuild to create the DLLs that will later be included in the FMU
