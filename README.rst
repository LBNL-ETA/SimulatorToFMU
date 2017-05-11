SimulatorToFMU
--------------

Overview
^^^^^^^^

SimulatorToFMU is a software package written in Python which allows 
users to export a memoryless Python-driven simulation program or script 
as a Functional Mock-up Unit (FMU) for  
model exchange or co-simulation using the Functional Mock-up Interface (FMI) 
standard version 1.0 or 2.0 (https://www.fmi-standard.org).
This FMU can then be imported into a variety of simulation programs 
that support the import of Functional Mock-up Units.

A memoryless Python-driven simulation program/script 
is a simulation program which meets following requirements:
   
  - The simulation program/script can be invoked through a Python script.
  - The invocation of the simulation program/script is memoryless. That is, 
    the output of the simulation program at any invocation time ``t`` 
    depends only on the inputs at the time ``t``. 
  - The inputs and the outputs of the simulation program/script must be ``real`` numbers.

.. note::

   The Python-driven script could invoke 
   scripts written in languages such as 
   MATLAB using the ``subprocess`` or ``os.system()``
   module of Python or specifically for MATLAB 
   using the MATLAB engine API for Python. 

The license is at simulatortofmu/LICENSE.txt

Download
^^^^^^^^

Files can be downloaded individually, or as a whole repository.

See the _Clone_ button on the top right for instructions and for programs that use a graphical user interfaces.

To download, edit and add files from a command line, install first a `git` program.

To download all files, run

    git clone https://github.com/LBNL-ETA/SimulatorToFMU.git

The edit a file, such as `README.md`, first edit the file, then enter

    git commit -m "Revised README file" README.md
    git push

To add new files, enter something like

    git add filename.xyz
    git commit -m "Added the file xxxx" filename.xyz
    git push
    
To use the git command on `Windows`

1. download and install a `git` client such as [github desktop](https://desktop.github.com/)[^install] 

2. open the Git Shell

3. From the Git Shell command prompt, 

    create a folder which should contain the files on the CyDER repository by typing

        mkdir simulatortofmu

4. change to the created folder by typing

        cd simulatortofmu

From the Github Shell command prompt, you can execute any `git` command.

To download, edit, and add new files see the commands listed in the section above.

[^install]: In the installation process, you might be asked to log into your repository, just skip this section.
