# create a temporary folder
# copy the template file for makefile
# write the template makefile
# call the compiler to run and create the libraries
# copy the libraries to the correct folder and then export the FMU
# For Windows Compilation using Visual Studio 2019, you need to
# and Modify the Visual Studio 2017 installation. Otherwise an error message
 # will indicate that the stddef.h library can't be found.
import subprocess as sp
import jinja2 as jja2
import os
import struct
import shutil
import glob
import xml.etree.ElementTree as et
import logging as log
log.basicConfig(filename='simulator.log', filemode='w',
                level=log.DEBUG, format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')
stderrLogger = log.StreamHandler()
stderrLogger.setFormatter(log.Formatter(log.BASIC_FORMAT))
log.getLogger().addHandler(stderrLogger)

file_path=os.path.dirname(os.path.realpath(__file__))
script_path = os.path.join(file_path, "..")
utilities_path = os.path.join(script_path, 'utilities')
MAKEFILE_TEMPLATE_WINDOWS = 'SimulatorToFMUPythonTemplate.vcxproj'
MAKEFILE_TEMPLATE_WINDOWS_PATH = os.path.join(utilities_path, MAKEFILE_TEMPLATE_WINDOWS)
PYTHON_C_SRC_DIR = os.path.join(script_path, 'libraries', 'modelica',
'SimulatorToFMU', 'Resources', 'src', 'python')
PYTHON_DLL_DIR = os.path.join(script_path, 'libraries', 'modelica',
'SimulatorToFMU', 'Resources', 'Library')
MODELICA_FOLDER_TEMPLATE=os.path.join(script_path, 'libraries', 'modelica', 'SimulatorToFMU', 'PythonXYZ')

# Pasing of the properties variables file
tree = et.ElementTree(file='systemVariables-windows.properties')
root = tree.getroot()
directories=[]
children = iter(root)
for child in children:
    directory={}
    pairs = iter(child)
    for pair in pairs:
        directory[pair.tag]=pair.text
        directories.append(directory)
print (directories)

PY_VERS="38"
#DLL_ROOT_NAME
DLL_ROOT_NAME="SimulatorToFMUPython"+PY_VERS

# Check existense of first directory
PYTHON_EXE_DIR=root[0][0].attrib['name']
if (PYTHON_EXE_DIR.lower()=='PYTHON_EXE_DIR'.lower()):
    PYTHON_EXE_DIR_PATH=directories[0]['entry']
    log.info('The PYTHON_EXE_DIR key is present in the configuration file.')
    if (os.path.isdir(PYTHON_EXE_DIR_PATH)):
        s = 'The PYTHON_EXE_DIR key path exists.'\
        ' The path found in the configuration file is '\
        + PYTHON_EXE_DIR_PATH
        log.info(s)
    else:
        s = 'The PYTHON_EXE_DIR key path does not exist.'\
        ' The path found in the configuration file is ' \
        + directories[0]['entry']
        log.error(s)
        raise ValueError(s)

# Check if the Python include directory exists
PYTHON_C_INC_DIR=os.path.join(PYTHON_EXE_DIR_PATH, 'include')
if(os.path.isdir(PYTHON_C_INC_DIR)):
    s = 'The Python include directory exists and is located at '\
    + PYTHON_C_INC_DIR
    log.info(s)
else:
    s = 'The Python include directory which should be located at '\
    + PYTHON_C_INC_DIR + ' does not exists.'
    log.error(s)
    raise ValueError(s)

# Check if the Python libraries (libs) directory exists
PYTHON_C_LIB=os.path.join(PYTHON_EXE_DIR_PATH, 'libs', "python"+PY_VERS+".lib")
if(os.path.exists(PYTHON_C_LIB)):
    s = 'The Python library exists and is located at '\
    + PYTHON_C_LIB
    log.info(s)
else:
    s = 'The Python library which should be located at '\
    + PYTHON_C_LIB + ' does not exists.'
    log.error(s)
    raise ValueError(s)
# Check existense of second directory
CMD_TOOL=root[1][0].attrib['name']
if (CMD_TOOL.lower()=='CMD_TOOL'.lower()):
    CMD_TOOL_PATH=directories[1]['entry']
    log.info('The CMD_TOOL key is present in the configuration file.')
    if (os.path.exists(CMD_TOOL_PATH)):
        s = 'The CMD Tool key path exists.'\
        ' The path found in the configuration file is '\
        + CMD_TOOL_PATH
        log.info(s)
    else:
        s = 'The CMD_TOOL key path does not exist.'\
        ' The path found in the configuration file is '\
        + directories[1]['entry']
        log.error(s)
        raise ValueError(s)

loader = jja2.FileSystemLoader(MAKEFILE_TEMPLATE_WINDOWS_PATH)
env = jja2.Environment(loader=loader)
template = env.get_template('')

output_res=template.render(
    #python_vers=38,
    #python_exe_dir=PYTHON_EXE_DIR_PATH,
    python_c_src_dir=PYTHON_C_SRC_DIR,
    dll_root_name=DLL_ROOT_NAME,
    python_c_inc_dir=PYTHON_C_INC_DIR,
    python_c_lib=PYTHON_C_LIB)
    #cmd_tool_path=CMD_TOOL_PATH)

output_file = DLL_ROOT_NAME+'.vcxproj'
if os.path.isfile(output_file):
    s = 'The output file {!s} exists and will be overwritten.'.format(
        output_file)
    log.warning(s)
with open(output_file, 'w') as fh:
    fh.write(output_res)
fh.close()

# Create a folder which will contain the libraries
tmpFolder='Python'+ PY_VERS
# Make the full path to the folder
tmpFolderPath=os.path.join(script_path, 'libraries', 'modelica', 'SimulatorToFMU', tmpFolder)
if(os.path.isdir(tmpFolderPath)):
    s = 'A folder with path named ' + tmpFolderPath + \
    ' exists. The folder will be deleted and recreated.'
    shutil.rmtree (tmpFolderPath)
    log.warning(s)
# Copy the template folder to the specific Python folder
shutil.copytree(MODELICA_FOLDER_TEMPLATE, tmpFolderPath)
# Get the working directory
workDir=os.getcwd()
# Switch to the folder which will be used to create the librariers
os.chdir(tmpFolderPath)

# Rename all the mo files which contain XYZ by the specific Python version
for filepath in glob.iglob('./**/*.mo'):
    with open(filepath) as file:
        s = file.read()
    s = s.replace('XYZ', PY_VERS)
    with open(filepath, "w") as file:
        file.write(s)

# Move one folder up to rewrite the package.order
os.chdir('..')
# Check if the python package was already updated
with open("package.order") as file:
    contents = file.read()
    search_word = tmpFolder
    if search_word in contents:
        wf=True
    else:
        wf=False
# If the package order was not updated, update t now
if (not wf):
    with open("package.order", "a") as myfile:
        myfile.write(tmpFolder)
# Copy all the files from the templates folder to the
# Python folder which will be used for the export.

# Switch back to the working directory
os.chdir(workDir)

# Export the FMU
# Check the system architecture
nbits=8 * struct.calcsize("P")
if(nbits==64):
    plf="x64"
    PYTHON_DLL_SIM = os.path.join(PYTHON_DLL_DIR, 'win64')
    if( not os.path.isdir(PYTHON_DLL_SIM)):
        s='The folder {!s} does not exist.'.format(PYTHON_DLL_SIM)
        raise ValueError(s)
else:
    s='This is currently only working for 64 bits architecture'
    log.error(s)
    raise ValueError(s)
    #plf="Win32"
# Execute the command to create the DLL
cmd = "\""+CMD_TOOL_PATH +"\"" + ' ' + output_file + " /p:configuration=release " + "/p:platform="+plf
os.system(cmd)

# Check that all the required files have been created.
DLL_Simulator=os.path.join(file_path, 'x64','release',DLL_ROOT_NAME+'.dll')
if (not os.path.isfile(DLL_Simulator)):
    s = 'The SimulatorToFMU DLL {!s} does not exists'.format(DLL_Simulator)
    log.error(s)
    raise ValueError(s)
LIB_Simulator=os.path.join(file_path, 'x64','release',DLL_ROOT_NAME+'.lib')
if (not os.path.isfile(LIB_Simulator)):
    s = 'The SimulatorToFMU LIB {!s} does not exists'.format(LIB_Simulator)
    log.error(s)
    raise ValueError(s)
DLL_Py=os.path.join(PYTHON_EXE_DIR_PATH, 'python'+PY_VERS+'.dll')
if (not os.path.isfile(DLL_Py)):
    s = 'The Python DLL {!s} does not exists'.format(DLL_Py)
    log.error(s)
    raise ValueError(s)

# Copy all the required files in the winxx folders
files = [DLL_Simulator, LIB_Simulator, DLL_Py]
for i in files:
    log.info('Copying {!s} in {!s}'.format(i, PYTHON_DLL_SIM))
    shutil.copy(i, PYTHON_DLL_SIM)
# Remove all temporary folders.
tmp = ['x64', DLL_ROOT_NAME+'.vcxproj']
for i in tmp:
    log.info('Deleting {!s}'.format(i))
    if(os.path.isdir(i)):
        shutil.rmtree(i)
    if(os.path.isfile(i)):
        os.remove(i)

# Manually copy the SimulatorToFMUPythonXYZ.dll, SimulatorToFMUPythonXYZ.lib
# as well the pythonXYZ dll to the libraries folder win64.
