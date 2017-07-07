Notes:

The shared original Python shared library 
libpython2.7.so.1 is copied here and renamed to libpython27.so.
This is because of the Modelica model which includes python27 as a
library. This is to avoid having to provide two dependencies for 
Windows (python27) and Linux (libpython2.7). The solution is to
link to libpython27.so in the makefile but include and 
rename the original library in the Library folder.
