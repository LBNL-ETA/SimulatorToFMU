This directory contains the source files
that are used to build the Python API
for the SimulatorToFMU library.
To compile the files on Linux Ubuntu,

The makefile generates libraries for the respective
operating system, and copies the library to
SimulatorToFMU.Resources/Library/"operatingSystem".

Pleas note that for Windows, %ERRORLEVEL% == 0 detects the 
operating system. To force compilation for a different platfrm,
set the flag to 1.
