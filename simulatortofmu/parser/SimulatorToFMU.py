#!/usr/bin/env python

"""

___int_doc:
SimulatorToFMU is a software package written in Python which allows 
users to export a memoryless Python-driven simulation program or script 
as a :term:`Functional Mock-up Unit` (FMU) for  
model exchange or co-simulation using the :term:`Functional Mock-up Interface` (FMI) 
standard `version 1.0 or 2.0 <https://www.fmi-standard.org>`_.
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
   
.. note::

  SimulatorToFMU generates FMUs that use the Python 2.7/ C API for executing Python-driven simulation programs/scripts.
  
__author__ = "Thierry S. Nouidui"
__email__ = "TSNouidui@lbl.gov"
__license__ = "BSD"
__maintainer__ = "Thierry S Nouidui"
___int_doc::

To create an FMU,
open a command-line window (see :doc:`notation`).
The standard invocation of the SimulatorToFMU tool is:

.. code-block:: none

  > python  <scriptDir>SimulatorToFMU.py -s <python-scripts-path>

where ``scriptDir`` is the path to the scripts directory of SimulatorToFMU.
This is the ``parser`` subdirectory of the installation directory.
See :doc:`installation` for details.

An example of invoking ``SimulatorToFMU.py`` on Windows is

.. code-block:: none

  # Windows:
  > python parser\\SimulatorToFMU.py -s parser\\utilities\\simulator_wrapper.py,d:\\calc.py

Following requirements must be met when using SimulatorToFMU

- All file paths can be absolute or relative.
- If any file path contains spaces, then it must be surrounded with double quotes.


``SimulatorToFMU.py`` supports the following command-line switches:

+----------------------------------------------------+-------------------------------------------------------------------+
| Options                                            | Purpose                                                           |
+====================================================+===================================================================+
| -s                                                 | Paths to python scripts required to run the                       |
|                                                    | Simulator.                                                        |
|                                                    | The main Python script must be an extension                       |
|                                                    | of the ``simulator_wrapper.py`` script which is provided in       |
|                                                    | ``parser/utilities/simulator_wrapper.py``. The name of            |
|                                                    | the main Python script must be ``simulator_wrapper.py``.          |
+----------------------------------------------------+-------------------------------------------------------------------+
| -c                                                 | Path to the Simulator model or configuration file.                |
+----------------------------------------------------+-------------------------------------------------------------------+
| -i                                                 | Path to the XML input file with the inputs/outputs of the FMU.    |
|                                                    | Default is ``parser/utilities/SimulatorModelDescription.xml``     |
+----------------------------------------------------+-------------------------------------------------------------------+
| -v                                                 | FMI version. Options are ``1.0`` and ``2.0``. Default is ``2.0``  |
+----------------------------------------------------+-------------------------------------------------------------------+
| -a                                                 | FMI API version. Options are ``cs`` (co-simulation) and ``me``    |
|                                                    | (model exchange). Default is ``me``.                              |
+----------------------------------------------------+-------------------------------------------------------------------+
| -t                                                 | Modelica compiler. Options are ``dymola`` (Dymola), ``jmodelica`` |
|                                                    | (JModelica), and ``openmodelica`` (OpenModelica).                 |
|                                                    | Default is ``dymola``.                                            |
+----------------------------------------------------+-------------------------------------------------------------------+
| -pt                                                | Path to the Modelica executable compiler.                         |
+----------------------------------------------------+-------------------------------------------------------------------+

The main functions of SimulatorToFMU are

 - reading, validating, and parsing the Simulator XML input file.
   This includes removing and replacing invalid characters in variable names such as ``*+-`` with ``_``,
 - writing Modelica code with valid inputs and outputs names,
 - invoking a Modelica compiler to compile the :term:`Modelica` code as an FMU 
   for model exchange or co-simulation ``1.0`` or ``2.0``.

The next section discusses requirements of some of the arguments of SimulatorToFMU.

Simulation model or configuration file 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An FMU exported by SimulatorToFMU needs in certain cases a configuration file to run.
There are two ways of providing the configuration file to the FMU:

  1. The path to the configuration file is passed as the comamnd line argument ``"-c"`` 
     of SimulatorToFMU.py. In this situation, the configuration file is copied 
     in the resources folder of the FMU.
  2. The path to the configuration is set by the master algorithm before initializing the FMU.
     

.. note::

   The name of the configuration variable is ``_configurationFileName``. 
   This name is reserved and should not be used for FMU input and output names.
  
Depending on the tool used to export the FMU, following requirements/restrictions apply:


Dymola
******

- If the path to the configuration file is provided,  then
  Dymola copies the file to its resources folder and uses the configuration file at runtime.
  In this case, the path to the configuration file can't be set and changed by the master algorithm. 

- If the configuration file is not provided, then the path to the configuration file must 
  be set by the master algorithm prior to initializing the FMU.  

JModelica
*********

- If the path to the configuration file is provided,  then
  JModelica will not copy it to the resources folder of the FMU. 
  Instead, the path to the configuration is hard-coded in the FMU. 
  As a further restriction, the path to the configuration file can't be set and changed by the master algorithm. 
 
  These are known limitations in JModelica 2.0.
  The workaround is to make sure that the path of the configuration file is 
  the same on the machine where the FMU will be run.
  
- If the configuration file is not provided, then SimularToFMU will issue a warning. 


OpenModelica
************

- If the path to a configuration file is provided,  then
  OpenModelica will not copy it to the resources folder of the FMU. 
  Instead, the path to the configuration is hard-coded in the FMU. 
  However, the path to the configuration file can be set and changed by the master algorithm. 

  This is a known limitation in OpenModelica 1.11.0.
  The workaround is to either make sure that the path of the configuration file is 
  the same on the machine where the FMU will be run, or set the path of the configuration file
  when running the FMU.
  
- If the configuration file is not provided, then the path to the configuration file must 
  be set by master algorithm prior to initializing the FMU. 


Reserved variable names 
~~~~~~~~~~~~~~~~~~~~~~~

Following variables names are not allowed to be used as FMU input, output, or parameter names.

- ``_configurationFileName``: Variable name used to set the path to the Simulator model or configuration file.
- ``_saveToFile``: Variable used to set the flag for storing simulation results (1 for storing, 0 else).
- ``time``: Internal FMU simulation time.

If any of these variables is used for an FMU input, output, or parameter name, SimulatorToFMU will exit with an error.


"""

from lxml import etree
from datetime import datetime
import xml.etree.ElementTree as ET
import jinja2 as jja2
import logging as log
import subprocess as sp
import os
import sys
import shutil
import zipfile
import re
import platform
import random, string

log.basicConfig(filename='Simulator.log', filemode='w',
                level=log.DEBUG, format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')
stderrLogger = log.StreamHandler()
stderrLogger.setFormatter(log.Formatter(log.BASIC_FORMAT))
log.getLogger().addHandler(stderrLogger)

# These files are required by the utility to run.
# They must be at the top level of the current working
# directory.
# XSD_SCHEMA: Schema used to validate the XML input
# MO_TEMPLATE: Template used to write Modelica model
# SimulatorModelicaTemplate_MOS: Template used to write mos script
# XML_MODELDESCRIPTION: Default XML input file if none is provided

# Get the path to the templates files
script_path = os.path.dirname(os.path.realpath(__file__))
utilities_path = os.path.join(script_path, 'utilities')
XSD_SCHEMA = 'SimulatorModelDescription.xsd'
NEEDSEXECUTIONTOOL = 'needsExecutionTool'
MODELDESCRIPTION = 'modelDescription.xml'
MO_TEMPLATE = 'SimulatorModelicaTemplate.mo'
MOS_TEMPLATE_DYMOLA = 'SimulatorModelicaTemplate_Dymola.mos'
MOS_TEMPLATE_JMODELICA = 'SimulatorModelicaTemplate_JModelica.py'
MOS_TEMPLATE_OPENMODELICA = 'SimulatorModelicaTemplate_OpenModelica.mos'
XML_MODELDESCRIPTION = 'SimulatorModelDescription.xml'
MO_TEMPLATE_PATH = os.path.join(utilities_path, MO_TEMPLATE)
MOS_TEMPLATE_PATH_DYMOLA = os.path.join(utilities_path, MOS_TEMPLATE_DYMOLA)
MOS_TEMPLATE_PATH_JMODELICA = os.path.join(utilities_path, MOS_TEMPLATE_JMODELICA)
MOS_TEMPLATE_PATH_OPENMODELICA = os.path.join(
    utilities_path, MOS_TEMPLATE_OPENMODELICA)
XSD_FILE_PATH = os.path.join(utilities_path, XSD_SCHEMA)
XML_INPUT_FILE = os.path.join(utilities_path, XML_MODELDESCRIPTION)
SimulatorToFMU_LIB_PATH = os.path.join(script_path, 'libraries', 'modelica')


def main():
    """
    Main function to export a Simulator as an FMU.


    """
    import argparse

    # Configure the argument parser

    parser = argparse.ArgumentParser(
        description='Export Simulator as a Functional Mock-up Unit')
    simulator_group = parser.add_argument_group(
        "Arguments to export a Simulator as an FMU")

    simulator_group.add_argument(
        '-s',
        '--python-scripts-path',
        required=True,
        help='Path to the Python scripts ' +
        ' used to interface with simulator',
        type=(
            lambda s: [
                item for item in s.split(',')]))

    simulator_group.add_argument('-c', '--con-fil-path',
                                 help='Path to the configuration file')
    simulator_group.add_argument('-i', '--io-file-path',
                                 help='Path to the XML input file')
    simulator_group.add_argument('-v', '--fmi-version',
                                 help='FMI version. Valid options are <1.0>'
                                 + ' and <2.0>). Default is <2.0>')
    simulator_group.add_argument('-a', "--fmi-api",
                                 help='FMI API version. Valid options'
                                 + ' are <cs> for co-simulation'
                                 + ' and <me> for model exchange.'
                                 + ' Default is <me>')
    simulator_group.add_argument("-t", "--export-tool",
                                 help='Modelica compiler. Valid options are '
                                 + '<dymola> for Dymola, <jmodelica> '
                                 + 'for JModelica, and <openmodelica> for OpenModelica'
                                 + ' Default is <dymola>')
    simulator_group.add_argument("-pt", "--export-tool-path",
                                 help='Path to the Modelica executable compiler.')
#     simulator_group.add_argument("-n", "--needs-tool",
#                                  help='Flag to indicate if FMU needs an '
#                                  + 'external execution tool to run. '
#                                  + 'Valid options are '
#                                  + '<true> and <false>.'
#                                  + 'Default is <false>')

    # Parse the arguments
    args = parser.parse_args()

    # Set the Python version
    # Here we set the Python version. We keep this in case
    # we want to include different versions of Python in the
    # Modelica model and use the correct one by detecting the version
    # of Python used to run the script.
    python_vers = '27'

    # Check command line options
    if not(platform.system().lower() in ['windows', 'linux']):
        log.info('SimulatorToFMU is only supported on Linux and Windows')
        return

    # Check export tool
    export_tool = args.export_tool
    if (platform.system().lower() == 'linux' and export_tool == 'openmodelica'):
        log.info(
            'SimulatorToFMU is only supported on Windows when using OpenModelica as the Modelica compiler.')
        return
    
    # Get export tool Path
    export_tool_path = args.export_tool_path
    if export_tool_path is None:
        s = 'Path to the installation folder of tool={!s} was not specified.'\
        ' Make sure that the tool is on the system path otherwise compilation will fail.'.format(export_tool)
        log.warning(s)
    else:   
        export_tool_path = fix_path_delimiters(export_tool_path)
      
    # Get the FMI version
    fmi_version = args.fmi_version

    # Check if fmi version is none
    if(fmi_version is None):
        log.info('FMI version not specified. Version 2.0 will be used.')
        fmi_version = '2.0'

    # Check if fmi version is valid
    if not (fmi_version in ['1.0', '2.0', '1', '2']):
        s = 'This version only supports FMI version 1.0 and 2.0.'
        log.error(s)
        raise ValueError(s)

    # Get the FMI API version
    fmi_api = args.fmi_api

    # Check if fmi api is none
    if(fmi_api is None):
        log.info('FMI API not specified. Model exchange (me) API will be used.')
        fmi_api = 'me'

    # Check if the fmi api is valid
    if not (fmi_api.lower() in ['me', 'cs']):
        s = 'This version only supports FMI model exchange(me) or co-simulation (cs) API.'
        log.error(s)
        raise ValueError(s)

    if(export_tool is None):
        log.info('No export tool was specified. dymola the default will be used.')
        export_tool = 'dymola'

    # Check if export tool is valid
    if not (export_tool.lower() in ['dymola', 'jmodelica', 'openmodelica']):
        s = 'Supported export tools are Dymola (dymola), Jmodelica (jmodelica) and OpenModelica(openmodelica).'
        log.error(s)
        raise ValueError(s)

    # Define templates variables
    if(export_tool.lower() == 'dymola'):
        mos_template_path = MOS_TEMPLATE_PATH_DYMOLA
        # Convert the FMI version to int for Dymola
        if fmi_version in ['1.0', '2.0']:
            fmi_version = str(int(float(fmi_version)))
        modelica_path = 'MODELICAPATH'
    elif(export_tool.lower() == 'jmodelica'):
        mos_template_path = MOS_TEMPLATE_PATH_JMODELICA
        if fmi_version in ['1', '2']:
            fmi_version = str(float(fmi_version)*1.0)
        modelica_path = None
    elif(export_tool.lower() == 'openmodelica'):
        if fmi_version in ['1', '2']:
            fmi_version = str(float(fmi_version)*1.0)
        mos_template_path = MOS_TEMPLATE_PATH_OPENMODELICA
        modelica_path = 'OPENMODELICALIBRARY'

        

    # Check if user is trying to export a 1.0 co-simulation FMU with
    # OpenModelica
    if (export_tool == 'openmodelica' and fmi_version ==
            '1.0' and fmi_api.lower() == 'cs'):
        log.info(
            'Export of FMU type cs for version 1 is not supported for openmodelica.' +
            ' Supported combinations are me (model exchange) for versions 1.0 & 2.0,' +
            ' cs (co-simulation) & me_cs (model exchange & co-simulation) for version 2.0.')
        return

    # Get the Python script path
    python_scripts_path = args.python_scripts_path
    # Make sure we have correct path delimiters
    python_scripts_path = [os.path.abspath(item)
                           for item in python_scripts_path]
    if(platform.system().lower() == 'windows'):
        python_scripts_path = [item.replace('\\', '\\\\')
                               for item in python_scripts_path]

    python_scripts_base = [os.path.basename(item)
                           for item in python_scripts_path]
    # Check if simulator_wrapper.py is in the list of functions
    if not('simulator_wrapper.py' in python_scripts_base):
        s = ('simulator_wrapper.py no found in the list of Python scripts={!s}').format(
            python_scripts_path)
        log.error(s)
        raise ValueError(s)

    # Check if the path exists
    for python_script_path in python_scripts_path:
        if(not os.path.exists(python_script_path)):
            s = ('The Path to the Python script={!s} provided does not exist.').format(
                python_script_path)
            log.error(s)
            raise ValueError(s)

    # Check if it is a Python file
    for python_script_path in python_scripts_path:
        ext = os.path.splitext(python_script_path)[-1].lower()
        if (ext != '.py'):
            s = ('The Python script={!s} provided does not have a valid extension.').format(
                python_script_path)
            log.error(s)
            raise ValueError(s)
    
    print('============Exporting scripts={!s} as Functional Mock-up Unit. API={!s}, Version={!s}, Export Tool={!s}'.format(python_scripts_path, 
                                    fmi_api, fmi_version, export_tool))
           
    # Get the xml files
    io_file_path = args.io_file_path
    if io_file_path is None:
        s = ('No XML input file was provided. The default XML file which is at {!s} will be used.').format(
            XML_INPUT_FILE)
        log.info(s)
        io_file_path = XML_INPUT_FILE

    # Set the default configuration file
    con_path = args.con_fil_path
    # Make sure we have correct path delimiters
    if not (con_path is None):        
        con_path = fix_path_delimiters(con_path)
    
    # Check configuration file for JModelica
    if con_path is None and export_tool=='jmodelica':
        s = ('No configuration file was provided.'+\
             ' JModelica does not allow to set the path'+
             ' to a configuration file at runtime.' +\
             ' Hence if the exported simulation program/script'+\
             ' needs a configuration file to run, then the path'+\
             ' to the configuration file must be provided'+\
             ' when creating the FMU. Otherwise the FMU'+\
             ' will fail to run.')
        log.warning(s)
        con_path = ''
    elif (con_path is None):
        con_path = ''
        
    # Get the need execution
    #needs_tool = args.needs_tool
    # Leave this to eventually avoid having
    # to add "model_name".scripts to the python path
    # Currently adding an import statement in the Python
    # main script will cause the module to fail 
    needs_tool = 'True'
    # Check if fmi api is none
    if(needs_tool is None):
        log.info(
            'Flag to specify whether an execution is needed is not specified. Default (false) will be used.')
        needs_tool = 'true'

    if not (needs_tool.lower() in ['true', 'false']):
        log.info(
            'Flag to specify whether an execution is needed is not specified. Default (false) will be used.')
        needs_tool = 'true'

    # Export the tool as an FMU
    Simulator = SimulatorToFMU(con_path,
                               io_file_path,
                               SimulatorToFMU_LIB_PATH,
                               MO_TEMPLATE_PATH,
                               mos_template_path,
                               XSD_FILE_PATH,
                               python_vers,
                               python_scripts_path,
                               fmi_version,
                               fmi_api,
                               export_tool,
                               export_tool_path,
                               modelica_path,
                               needs_tool.lower())

    start = datetime.now()
    ret_val = Simulator.print_mo()
    if(ret_val != 0):
        s = 'Could not print the Simulator Modelica model. Error in print_mo().'
        parser.print_help()
        log.error(s)
        raise ValueError(s)    
    
    ret_val = -1
    ret_val = Simulator.generate_fmu()
    if(ret_val != 0):
        s = 'Could not generate the Simulator FMU. Error in generate_fmu().'
        parser.print_help()
        log.error(s)
        raise ValueError(s)
    
    ret_val = -1
    ret_val = Simulator.create_scripts_folder()
    if(ret_val != 0):
        s = 'Could not create the Python scripts folder. Error in create_scripts_folder().'
        parser.print_help()
        log.error(s)
        raise ValueError(s)
    
    ret_val = -1
    ret_val = Simulator.create_binaries_folder()
    if(ret_val != 0):
        s = 'Could not create the binaries folder. Error in create_binaries_folder().'
        parser.print_help()
        log.error(s)
        raise ValueError(s)
    
    ret_val = -1
    ret_val = Simulator.clean_temporary()
    if(ret_val != 0):
        s = 'Could not clean temporary files. Error in clean_temporary().'
        parser.print_help()
        log.error(s)
        raise ValueError(s)

    # Rewrite FMUs for FMUs with version higher than 1.0
    ret_val = -1
    ret_val = Simulator.rewrite_fmu()
    if(ret_val != 0):
        s = 'Could not rewrite Simulator FMU. Error in rewrite_fmu().'
        parser.print_help()
        log.error(s)
        raise ValueError(s)
    end = datetime.now()

    log.info('Export Simulator as an FMU in {!s} seconds.'.format(
        (end - start).total_seconds()))


def check_duplicates(arr):
    """
    Check duplicates in a list of variables.

    This function checks duplicates in a list
    and breaks if duplicates are found. Duplicates
    names are not allowed in the list of inputs, outputs,
    and parameters.

    :param arr(str): list of string variables.

    """

    dup = set([x for x in arr if arr.count(x) > 1])
    lst_dup = list(dup)
    len_lst = len(lst_dup)
    if (len_lst > 0):
        log.error('There are duplicates names in the list {!s}.'.format(arr))
        log.error('This is invalid. Check your XML input file.')
        for i in lst_dup:
            log.error('Variable {!s} has duplicates in the list {!s}.'.format(
                i, arr))
        # Assert if version is different from FMI 2.0
        assert(len_lst <= 0), 'Duplicates found in the list.'


# Invalid symbols
g_rexBadIdChars = re.compile(r'[^a-zA-Z0-9_]')


def sanitize_name(name):
    """
    Make a Modelica valid name.

    In Modelica, a variable name:
    Can contain any of the characters {a-z,A-Z,0-9,_}.
    Cannot start with a number.

    :param name(str): Variable name to be sanitized.
    :return: Sanitized variable name.

    """

    # Check if variable has a length > 0
    if(len(name) <= 0):
        log.error('Require a non-null variable name.')
        assert(len(name) > 0), 'Require a non-null variable name.'
    #
    # Check if variable starts with a number.
    if(name[0].isdigit()):
        log.warning('Variable Name {!s} starts with 0.'.format(name))
        log.warning('This is invalid.')
        log.warning('The name will be changed to start with f_.')
        name = 'f_' + name
    #
    # Replace all illegal characters with an underscore.
    name = g_rexBadIdChars.sub('_', name)
    #
    return(name)


def fix_path_delimiters(name):
    
    """
    Make a valid path.

    :param name(str): Path name to be sanitized.
    :return: Sanitized path name.

    """
    
    if not (name is None):
        name = os.path.abspath(name)
    if(platform.system().lower() == 'windows'):
        name = name.replace('\\', '\\\\')
    return name

def zip_fmu(dirPath=None, zipFilePath=None, includeDirInZip=True):
    """
    Create a zip archive from a directory.

    Note that this function is designed to put files in the zip archive with
    either no parent directory or just one parent directory, so it will trim any
    leading directories in the filesystem paths and not include them inside the
    zip archive paths. This is generally the case when you want to just take a
    directory and make it into a zip file that can be extracted in different
    locations.

    :param dirPath(str): String path to the directory to archive. This is the only
            required argument. It can be absolute or relative, but only one or zero
            leading directories will be included in the zip archive.

    :param zipFilePath(str): String path to the output zip file. This can be an absolute
            or relative path. If the zip file already exists, it will be updated. If
            not, it will be created. If you want to replace it from scratch, delete it
            prior to calling this function. (default is computed as dirPath + ".zip")

    :param includeDirInZip(bool): Boolean indicating whether the top level directory
            should be included in the archive or omitted. (default True)

    Author: http://peterlyons.com/problog/2009/04/zip-dir-python

    """
    if not zipFilePath:
        zipFilePath = dirPath + '.zip'
    if not os.path.isdir(dirPath):
        raise OSError('dirPath argument must point to a directory. '
                      "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)
    # Little nested function to prepare the proper archive path

    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        # return os.path.normcase(archivePath)
        return archivePath

    outFile = zipfile.ZipFile(zipFilePath, "w",
                              compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        # Make sure we get empty directories as well
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            outFile.writestr(zipInfo, "")
    outFile.close()


class SimulatorToFMU(object):

    """
    Simulator FMU writer.

    This class contains various methods to
    read and XML file, validate it against
    a pre-defined XML schema, extracting the
    variables attributes, writing a Modelica
    model of a Simulator model and exporting
    the model as an FMU for model exchange or
    co-simulation.

    """

    def __init__(self, con_path,
                 xml_path,
                 simulatortofmu_path,
                 moT_path,
                 mosT_path,
                 xsd_path,
                 python_vers,
                 python_scripts_path,
                 fmi_version,
                 fmi_api,
                 export_tool,
                 export_tool_path,
                 modelica_path,
                 needs_tool):
        
        """
        Initialize the class.

        :param con_path (str): The path to the configuration file.
        :param xml_path (str): The path to the XML file.
            simulatortofmu_path (str): The path to the folder
            which contains the Buildings library excluding
            the ending FILE SEPARATOR.
        :param moT_path (str): Modelica model template.
        :param mosT_path (str): Modelica script template.
        :param xsd_path (str): The path to the XML schema.
        :param python_vers (str): The python version.
        :param python_scripts_path (str): The path to the Python
            scripts needed to interface the simulator.
        :param fmi_version (str): The FMI version.
        :param fmi_api (str): The FMI API.
        :param export_tool (str): The Modelica compiler.
        :param export_tool_path (str): The path to the Modelica compiler.
        :param modelica_path (str): The path to the libraries to be added 
               to the MODELICAPATH.
        :param needs_tool (str): Needs execution tool on target machine.

        """

        self.con_path = con_path
        self.xml_path = xml_path
        self.simulatortofmu_path = \
            simulatortofmu_path + os.sep
        self.moT_path = moT_path
        self.mosT_path = mosT_path
        self.xsd_path = xsd_path
        self.python_vers = python_vers
        self.python_scripts_path = python_scripts_path
        self.fmi_version = fmi_version
        self.fmi_api = fmi_api
        self.export_tool = export_tool
        self.export_tool_path = export_tool_path
        self.modelica_path = modelica_path
        self.needs_tool = needs_tool

    def xml_validator(self):
        """
        Validate the XML file.

        This function validates the XML file
        against SimulatorModelDescription.xsd.

        """

        try:
            # Get the XML schema to validate against
            xml_schema = etree.XMLSchema(file=self.xsd_path)
            # Parse string of XML
            xml_doc = etree.parse(self.xml_path)
            # Validate parsed XML against schema
            xml_schema.assertValid(xml_doc)
            # Validate parsed XML against schema returning
            # boolean value indicating success/failure
            result = xml_schema.validate(xml_doc)
            if result:
                log.info(self.xml_path + ' is a valid XML document.')
            return result
        except etree.XMLSchemaParseError as xspe:
            # Something wrong with the schema (getting from URL/parsing)
            print('XMLSchemaParseError occurred!')
            print(xspe)
        except etree.XMLSyntaxError as xse:
            # XML not well formed
            print('XMLSyntaxError occurred!')
            print(xse)
        except etree.DocumentInvalid:
            # XML failed to validate against schema
            print('DocumentInvalid occurred!')
            error = xml_schema.error_log.last_error
            if error:
                # All the error properties (from libxml2) describing what went
                # wrong
                print('domain_name: ' + error.domain_name)
                print('domain: ' + str(error.domain))
                print('filename: ' + error.filename)
                print('level: ' + str(error.level))
                print('level_name: ' + error.level_name)  # an integer
                # a unicode string that identifies the line where the error
                # occurred.
                print('line: ' + str(error.line))
                # a unicode string that lists the message.
                print('message: ' + error.message)
                print('type: ' + str(error.type))  # an integer
                print('type_name: ' + error.type_name)

    def xml_parser(self):
        """
        Parse the XML file.

        This function parses the XML file which contains
        the input, output,  and parameters of a Simulator
        model. It extracts the variables attributes
        needed to write the Simulator Modelica model.

        :return: List of scalar variables, input names, output names,
                parameter values, Modelica input names, Modelica output names,
                Modelica output parameter names.

        """

        # Get the XML file
        tree = ET.parse(self.xml_path)
        # Get the root of the tree
        root = tree.getroot()

        # Get the model name to write the .mo file
        self.model_name = root.attrib.get('modelName')

        # Remove Invalid characters from the model name as this is used
        # by the Modelica model and the FMU
        s = ('Invalid characters will be removed from the model name={!s}.').format(
            self.model_name)
        log.info(s)
        self.model_name = sanitize_name(self.model_name)
        s = ('The new model name is {!s}.').format(self.model_name)
        log.info(s)

        # Iterate through the XML file and get the ModelVariables.
        input_variable_names = []
        modelica_input_variable_names = []
        # modelicaInputVariableNames = []
        output_variable_names = []
        modelica_output_variable_names = []
        parameter_variable_values = []
        parameter_variable_names = []
        modelica_parameter_variable_names = []
        # Parameters used to write annotations.
        inpY1 = 88
        inpY2 = 110
        outY1 = 88
        outY2 = 108
        indel = 20
        outdel = 18
        # Get variables
        scalar_variables = []
        for child in root.iter('ModelVariables'):
            for element in child:
                scalar_variable = {}
                # Iterate through ScalarVariables and get attributes
                (name, description, causality) = element.attrib.get('name'), \
                    element.attrib.get('description'), \
                    element.attrib.get('causality').lower()
                # Iterate through children of ScalarVariables and get
                # attributes
                if (causality == 'input'):
                    input_variable_names.append(name)
                    log.info('Invalid characters will be removed from the '
                             'input variable name {!s}.'.format(name))
                    new_name = sanitize_name(name)
                    log.info(
                        'The new input variable name is {!s}.'.format(new_name))
                    modelica_input_variable_names.append(new_name)
                    scalar_variable['name'] = new_name

                    inpY1 = inpY1 - indel
                    inpY2 = inpY2 - indel
                    scalar_variable['annotation'] = (' annotation'
                                                     '(Placement'
                                                     '(transformation'
                                                     '(extent={{-122,'
                                                     + str(inpY1) + '},'
                                                     '{-100,' + str(inpY2)
                                                     + '}})))')

                if (causality == 'output'):
                    output_variable_names.append(name)
                    log.info('Invalid characters will be removed from the '
                             'output variable name {!s}.'.format(name))
                    new_name = sanitize_name(name)
                    log.info(
                        'The new output variable name is {!s}.'.format(new_name))
                    modelica_output_variable_names.append(new_name)
                    scalar_variable['name'] = new_name

                    outY1 = outY1 - outdel
                    outY2 = outY2 - outdel
                    scalar_variable['annotation'] = (' annotation'
                                                     '(Placement'
                                                     '(transformation'
                                                     '(extent={{100,'
                                                     + str(outY1) + '},'
                                                     '{120,' + str(outY2)
                                                     + '}})))')

                if (causality == 'parameter'):
                    parameter_variable_names.append(name)
                    s = ('Invalid characters will be removed from the '
                         'parameter variable name={!s}.').format(name)
                    log.info(s)
                    new_name = sanitize_name(name)
                    s = ('The new parameter variable name is {!s}.').format(
                        new_name)
                    log.info(s)
                    modelica_parameter_variable_names.append(new_name)
                    scalar_variable['name'] = new_name

                for subelement in element:
                    vartype = subelement.tag
                    vartype_low = vartype.lower()
                    # Modelica types are case sensitive.
                    # This code makes sure that we get correct
                    # Modelica types if the user mistypes them.
                    if (vartype_low == 'real'):
                        # Make sure that we have
                        # a valid Modelica type.
                        vartype = 'Real'
                        unit = subelement.attrib.get('unit')
                        start = subelement.attrib.get('start')

                    if ((start is None) and ((causality == 'input')
                                             or causality == 'parameter')):
                        # Set the start value of input and parameter to zero.
                        s = (
                            'Start value of variable {!s} with causality {!s} is not defined.' +
                            'The start value will be set to 0.0 by default.').format(
                            name,
                            causality)
                        log.warning(s)
                        start = 0.0
                    elif not(start is None):
                        start = float(start)
                    # Create a dictionary
                    # scalar_variable['name'] = name
                    if not (description is None):
                        scalar_variable['description'] = description
                    # If there is no description set this to
                    # be an empty string.
                    else:
                        scalar_variable['description'] = ''
                    scalar_variable['causality'] = causality

                scalar_variable['vartype'] = vartype
                # Check if unit is defined
                if(unit is None):
                    unit = "1"
                scalar_variable['unit'] = unit
                # Check if start is defined
                if not (start is None):
                    scalar_variable['start'] = start
                scalar_variables.append(scalar_variable)
            # perform some checks on variables to avoid name clash
            # before returning the variables to Modelica
            log.info(
                'Check for duplicates in input, output and parameter variable names.')
            for i in [modelica_input_variable_names,
                      modelica_output_variable_names,
                      modelica_parameter_variable_names]:
                check_duplicates(i)
                
            for elm in ['_configurationFileName', '_saveToFile', 'time']:
                for nam in [modelica_input_variable_names,
                      modelica_output_variable_names,
                      modelica_parameter_variable_names]:
                    if elm in nam:
                        s = 'Reserved name={!s} is in the list '\
                            'of input/output/parameters variables={!s}. '\
                            'Check the XML input file={!s} and correct the variable name.'.format(elm, nam, self.xml_path)
                        log.error(s)
                        raise ValueError(s)
                        
            if(len(modelica_input_variable_names) < 1):
                s = 'The XML input file={!s} does not contain any input variable. '\
                'At least, one input variable needs to be defined'.format(self.xml_path)
                log.error(s)
                raise ValueError(s)
            
            if(len(modelica_output_variable_names) < 1):
                s = 'The XML input file={!s} does not contain any output variable. '\
                'At least, one output variable needs to be defined'.format(self.xml_path)
                log.error(s)
                raise ValueError(s)
            
            s = 'Parsing of {!s} was successfull.'.format(self.xml_path)
            log.info(s)
            return scalar_variables, input_variable_names, \
                output_variable_names, parameter_variable_names, \
                parameter_variable_values, modelica_input_variable_names, \
                modelica_output_variable_names, \
                modelica_parameter_variable_names

    def print_mo(self):
        """
        Print the Modelica model of a Simulator XML file.

        This function parses a Simulator XML file and extracts
        the variables attributes needed to write the Simulator
        Modelica model. It then writes the Modelica model.
        The name of the Modelica model is the model_name in the
        model description file. This is used to avoid
        name conflicts when generating multiple Simulator models.

        :return: 0 if success.

        """

        self.xml_validator()
        scalar_variables, input_variable_names, \
            output_variable_names, \
            parameter_variable_names, \
            parameter_variable_values, \
            modelica_input_variable_names, \
            modelica_output_variable_names, \
            modelica_parameter_variable_names \
            = self.xml_parser()

        loader = jja2.FileSystemLoader(self.moT_path)
        env = jja2.Environment(loader=loader)
        template = env.get_template('')

        # Call template with parameters
        output_res = template.render(
            model_name=self.model_name,
            scalar_variables=scalar_variables,
            input_variable_names=input_variable_names,
            output_variable_names=output_variable_names,
            parameter_variable_names=parameter_variable_names,
            parameter_variable_values=parameter_variable_values,
            modelica_input_variable_names=modelica_input_variable_names,
            modelica_output_variable_names=modelica_output_variable_names,
            modelica_parameter_variable_names=modelica_parameter_variable_names,
            con_path=self.con_path,
            python_vers=self.python_vers)
        # Write results in mo file which has the same name as the class name
        output_file = self.model_name + '.mo'
        if os.path.isfile(output_file):
            s = 'The output file {!s} exists and will be overwritten.'.format(
                output_file)
            log.warning(s)
        with open(output_file, 'w') as fh:
            fh.write(output_res)
        fh.close()

        # Write success.
        s = ('The Modelica model {!s} of {!s} is successfully created.').format(
            output_file, self.model_name)
        log.info(s)
        s = ('The Modelica model {!s} of {!s} is in {!s}.').format(
            output_file, self.model_name, os.getcwd())
        log.info(s)
        return 0

    def generate_fmu(self):
        """
        Generate the Simulator FMU.

        This function writes the mos file which is used to create the
        Simulator FMU. The function requires the path to the Buildings
        library which will be set to the MODELICAPATH.
        The function calls Dymola to run the mos file and
        writes a Simulator FMU. The Simulator FMU cannot be used yet
        as Dymola does not support the export of FMUs which
        has the needsExecutionTool set to true.

        :return: 0 if success.

        """


        # Check if library path is none
        if not(self.export_tool == 'jmodelica'):
            # Set the Modelica path to point to the Simulator Library
            current_library_path = os.environ.get(self.modelica_path)
            if (current_library_path is None):
                os.environ[self.modelica_path] = self.simulatortofmu_path
            else:
                os.environ[self.modelica_path] = self.simulatortofmu_path \
                    + os.pathsep + current_library_path

        loader = jja2.FileSystemLoader(self.mosT_path)
        env = jja2.Environment(loader=loader)
        template = env.get_template('')
        
        # Convert path to the correct format for PYTHON
        sim_lib_path_jm = os.path.abspath(self.simulatortofmu_path)
        sim_lib_path_jm = fix_path_delimiters(sim_lib_path_jm)

        output_res = template.render(model_name=self.model_name,
                                     fmi_version=self.fmi_version,
                                     fmi_api=self.fmi_api,
                                     sim_lib_path = sim_lib_path_jm)
                
        # Write results in mo file which has the same name as the class name
        
        rand_name = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(6))
        
        
        if (self.export_tool == 'jmodelica'):
            output_file = rand_name + '_' + self.model_name + '.py'
        elif (self.export_tool == 'dymola' or self.export_tool == 'openmodelica'):
            output_file = rand_name + '_' + self.model_name + '.mos'
        if os.path.isfile(output_file):
            s = ('The output file {!s} exists and will be overwritten.').format(
                output_file)
            log.warning(s)
        with open(output_file, 'w') as fh:
            fh.write(str(output_res))
        fh.close()
        
        # Create different commands for different tools
        # Create command for Dymola
        if (self.export_tool == 'dymola'):
            if (not (self.export_tool_path is None)):
                command = os.path.join(self.export_tool_path, 'dymola')
            else:
                command = 'dymola' 
            
        # Create command for JModelica     
        if(self.export_tool == 'jmodelica'):
            if(platform.system().lower()=='linux'):
                if (not (self.export_tool_path is None)):
                    command = os.path.join(self.export_tool_path, 'jm_python.sh')
                else:
                    command = os.path.join('jm_python.sh')
            elif(platform.system().lower()=='windows'):
                if (not (self.export_tool_path is None)):
                    
                    command = os.path.join(self.export_tool_path, 'setenv.bat')
                else:
                    command = 'setenv.bat'
        # Create command for OpenModelica
        if (self.export_tool == 'openmodelica'):
            if (not (self.export_tool_path is None)):
                command = os.path.join(self.export_tool_path, 'openmodelica')
            else:
                command = 'omc'
                
        # Compile the FMU using Dymola      
        if (self.export_tool == 'dymola'):
            retStr=sp.check_output([command, output_file])

        # Compile the FMU using JModelica
        if (self.export_tool == 'jmodelica'):
            if(platform.system().lower()=='linux'):
                retStr = sp.check_output([command, output_file])
            else:
                # 
                output_cmd = 'python ' + str(output_file)
                print ("command is {!s}".format(command + "&&" + output_cmd))
                # Run multiple commands in the same shell
                retStr = sp.check_output(command + "&&" + output_cmd, shell=True)

        # Compile the FMU using OpenModelica 
        if (self.export_tool == 'openmodelica'):
            retStr = sp.check_output([command, output_file, 'SimulatorToFMU'])
        
        # Check if there is any error message in the output
        if not (retStr is None):
            retStr=retStr.lower()
            if sys.version_info.major > 2:
                retStr = str(retStr, 'utf-8')
            if(retStr.find('error')>=0):
                s='{!s} failed to export {!s} as an FMU with error={!s}'.format(self.export_tool,
                                                                        self.model_name,
                                                                        retStr)
                raise ValueError(s)
        # Reset the library path to the default
        if not(self.export_tool == 'jmodelica'):
            if not(current_library_path is None):
                os.environ[self.modelica_path] = current_library_path
        
        # removd the output file
        os.remove(output_file)

        # Renamed the FMU to indicate target Python simulator
        fmu_name = self.model_name + '.fmu'
        # os.rename(self.model_name+'.fmu', fmu_name)
        
        # Write scuccess.
        s = 'The FMU {!s} is successfully created.'.format(fmu_name)
        log.info(s)
        s = 'The FMU {!s} is in {!s}.'.format(fmu_name, os.getcwd())
        log.info(s)

        return 0
    
    def create_scripts_folder(self):
        
        """
        Create folder which contains the scripts to be 
        added to the PYTHONPATH of the target machine where 
        the FMU will be run.

        :return: 0 if success.

        """
        
        # Copy all resources file in a directory
        dir_name = self.model_name +'.scripts'
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        log.info('Create the folder Simulator.scripts with scripts to be added to the PYTHONPATH.')
        os.makedirs(dir_name)
        for python_script_path in self.python_scripts_path:
            shutil.copy2(python_script_path, dir_name)
        fnam = os.path.join(dir_name, "README.txt")
        fh = open(fnam, "w")
        readme = 'IMPORTANT:\n\n' + \
                 'The files contains in this folder must be added to the PYTHONPATH.\n' + \
                 'This can be done by adding the unzipped folder ' + dir_name + ' to the PYTHONPATH.\n\n'
        fh.write(readme)
        fh.close()
        dir_name_zip = dir_name + '.zip'
        if os.path.exists(dir_name_zip):
            os.remove(dir_name_zip)
        zip_fmu(dir_name, includeDirInZip=False)
        # Delete the folder created
        shutil.rmtree(dir_name)   
        
        return 0
    
    
    def create_binaries_folder(self):
        
        """
        Create folder which contains the binaries to be 
        added to the system PATH of the target machine where 
        the FMU will be run.

        :return: 0 if success.

        """
        
        # Copy all resources file in a directory
        dir_name = self.model_name +'.binaries'
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        log.info('Create the folder Simulator.binaries with binaries to be added to the system PATH.')
        
        # Path to the libraries
        fil_path = os.path.join(
                        self.simulatortofmu_path,
                        'SimulatorToFMU',
                        'Resources',
                        'Library')
        
        if(platform.system().lower() == 'windows'):
            for arch in ['win32', 'win64']:
                zip_path = os.path.join(dir_name, arch)
                os.makedirs(zip_path)
                for libr in ['SimulatorToFMUPython27.dll', 'python27.dll']:
                    lib_path = os.path.join(fil_path, arch, libr)
                    if (os.path.isfile(lib_path)):
                        s = '{!s} will be copied to the binaries folder {!s}.' \
                        .format(lib_path, zip_path)
                        log.info(s)
                        shutil.copy2(lib_path, zip_path)
                    else:
                        s = '{!s} does not exist and will need to be compiled.'.format(fil_path)
                        raise ValueError(s)

        if(platform.system().lower() == 'linux'):       
            for arch in ['linux32', 'linux64']:
                zip_path = os.path.join(dir_name, arch)
                os.makedirs(zip_path)
                for libr in ['libSimulatorToFMUPython27.so', 'libpython27.so']:
                    lib_path = os.path.join(fil_path, arch, libr)
                    if (os.path.isfile(lib_path)):
                        s = '{!s} will be copied to the binaries folder {!s}.' \
                        .format(lib_path, zip_path)
                        log.info(s)
                        shutil.copy2(lib_path, zip_path)
                    else:
                        s = '{!s} does not exist and will need to be compiled.'.format(fil_path)
                        raise ValueError(s)

        fnam = os.path.join(dir_name, "README.txt")
        fh = open(fnam, "w")
        readme = 'IMPORTANT:\n\n' + \
                 'The files contains in this folder must be added to the system PATH.\n' + \
                 'This can be done by adding subdirectories of the unzipped folder '+ \
                 dir_name + ' to the system PATH.\n\n'
        fh.write(readme)
        fh.close()
        dir_name_zip = dir_name + '.zip'
        if os.path.exists(dir_name_zip):
            os.remove(dir_name_zip)
        zip_fmu(dir_name, includeDirInZip=False)
        # Delete the folder created
        shutil.rmtree(dir_name)   
        
        return 0

    def clean_temporary(self):
        """
        Clean temporary generated files.

        :return: 0 if success.

        """
        temporary = ['buildlog.txt', 'dsin.txt', 'dslog.txt', 'dymosim',
                     'request.', 'status.', 'dsmodel.c', 'dsfinal.txt',
                     'dsmodel_fmuconf.h', 'fmiModelIdentifier.h']
        for fil in temporary:
            if os.path.isfile(fil):
                os.remove(fil)
        # FMU folders generated by Dymola.
        DymFMU_tmp = ['~FMUOutput', '.FMUOutput',
                      'DymosimDll32', 'DymosimDll64']
        for fol in DymFMU_tmp:
            if os.path.isdir(fol):
                shutil.rmtree(fol)

        # Delete any files with extension in the list
        import glob
        for ext in ['*.c', '*.h', '*.o', '*.dll',
                    '*.makefile', '*.libs', '*.json',
                    '*.exe', '*.exp', '*.lib']:
            filelist = glob.glob(ext)
            for f in filelist:
                os.remove(f)
        return 0

    def rewrite_fmu(self):
        """
        Add needsExecutionTool and missing libraries to the Simulator FMU.

        This function unzips the FMU generated with generate_fmu(),
        reads the xml file, and add needsExecutionTool to the FMU capabilities.
        The function also includes binaries which are not included by OpenModelica
        and Dymola on Linux machines so the FMU can run on the deloyed paltforms.
        The function completes the process by re-zipping the FMU.
        The new FMU contains the modified XML file as well as the binaries.

        :return: 0 if success.


        """

        fmi_version = float(self.fmi_version)
        if (self.export_tool == 'openmodelica' or platform.system().lower() == 'linux'
                or (float(fmi_version) > 1.0 and self.needs_tool == 'true')):

            fmutmp = self.model_name + '.tmp'
            zipdir = fmutmp + '.zip'
            fmu_name = self.model_name + '.fmu'

            if os.path.exists(fmutmp):
                shutil.rmtree(fmutmp)

            if not os.path.exists(fmutmp):
                os.makedirs(fmutmp)

            # Copy file to temporary folder
            shutil.copy2(fmu_name, fmutmp)

            # Get the current working directory
            cwd = os.getcwd()

            # Change to the temporary directory
            os.chdir(fmutmp)

            # Path to the temporary directory
            fmutmp_path = os.path.join(cwd, fmutmp)

            # Unzip folder which contains he FMU
            zip_ref = zipfile.ZipFile(fmu_name, 'r')
            zip_ref.extractall('.')
            zip_ref.close()

            # Delete the FMU which is no longer used
            if os.path.isfile(fmu_name):
                os.remove(fmu_name)

            if (float(fmi_version) > 1.0 and self.needs_tool == 'true'):
                s = ('The model description file will be rewritten' +
                     ' to include the attribute {!s} set to true.').format(
                    NEEDSEXECUTIONTOOL)
                log.info(s)
                tree = ET.parse(MODELDESCRIPTION)
                # Get the root of the tree
                root = tree.getroot()
                # Add the needsExecution tool attribute
                root.attrib[NEEDSEXECUTIONTOOL] = 'true'
                tree.write(MODELDESCRIPTION, xml_declaration=True)

            # Switch back to the current working directory
            os.chdir(cwd)
            # Pass the directory which will be zipped
            # and call the zipper function.
            zip_fmu(fmutmp, includeDirInZip=False)

            if (os.path.exists(fmutmp)):
                shutil.rmtree(fmutmp)

            if os.path.isfile(fmu_name):
                os.remove(fmu_name)

            # Renamed file
            os.rename(zipdir, fmu_name)

            # Write scuccess.
            s = 'The FMU {!s} is successfully re-created.'.format(fmu_name)
            log.info(s)
            s = 'The FMU {!s} is in {!s}.'.format(fmu_name, os.getcwd())
            log.info(s)

            return 0
        return 0


if __name__ == '__main__':
    # Run main program!
    main()
