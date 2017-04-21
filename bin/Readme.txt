09/06/2016 by T. Nouidui 

To Run the FMUChecker

**Get the FMUChecker from the repository**

On Unix machine,

run getFmuChecker.sh + version of FMUChecker to use

  ./getFmuChecker.sh 2.0.1

This will download the FMUChecker from the fmi-standard.org repository and 
copy the files which are necessary to run the checker in the correct folder.

On a Windows machine, you will need to 
- manually download the files from the repository (https://svn.fmi-standard.org/fmi/branches/public/Test_FMUs/FMI_1.0/Compliance-Checker/)
- unzip the FMUChecker folder,
- copy the executable (e.g. fmuChecker.win32.exe) to the top level of the fmuChecker folder.
  
**Run the unit test with Python**

run runUnitTest.py which is in the bin folder with

  python runUnitTest.py

Please note that runUnitTest.py call fmuChecker with
default settings
