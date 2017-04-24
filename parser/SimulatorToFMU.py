#!/usr/bin/env python

"""

SimulatorToFMU is a software package written in Python which allows 
users to export any memory less simulation program which can be interfaced 
through a Python API  as a :term:`Functional Mock-up Unit` (FMU) for  
model Exchange or co-Simulation using the :term:`Functional Mock-up Interface` (FMI) 
standard `version 2.0 <https://svn.modelica.org/fmi/branches/public/specifications/v2.0/FMI_for_ModelExchange_and_CoSimulation_v2.0.pdf>`_.
This FMU can then be imported into a variety of simulation programs 
that support the import of the Functional Mock-up Interface.

__author__ = "Thierry S. Nouidui"
__email__ = "TSNouidui@lbl.gov"
__license__ = "BSD"
__maintainer__ = "Thierry S Nouidui"

"""


from lxml import etree
from datetime import datetime
import xml.etree.ElementTree as ET
import jinja2 as jja2
import logging as log
import subprocess as sp
import os, shutil, sys, zipfile, re, platform

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
# SimulatorModelicaTemplate_MO: Template used to write Modelica model
# SimulatorModelicaTemplate_MOS: Template used to write mos script
# XML_MODELDESCRIPTION: Default XML input file if none is provided
XSD_SCHEMA = 'SimulatorModelDescription.xsd'
NEEDSEXECUTIONTOOL = 'needsExecutionTool'
MODELDESCRIPTION = 'modelDescription.xml'
SimulatorModelicaTemplate_MO = 'SimulatorModelicaTemplate.mo'
SimulatorModelicaTemplate_Dymola_MOS = 'SimulatorModelicaTemplate_Dymola.mos'
SimulatorModelicaTemplate_OpenModelica_MOS = 'SimulatorModelicaTemplate_OpenModelica.mos'
XML_MODELDESCRIPTION = 'SimulatorModelDescription.xml'
# Get the path to the templates files
script_path = os.path.dirname(os.path.realpath(__file__))
utilities_path = os.path.join(script_path, 'utilities')
MO_TEMPLATE_PATH_DYMOLA = os.path.join(utilities_path, SimulatorModelicaTemplate_MO)
MOS_TEMPLATE_PATH_DYMOLA = os.path.join(utilities_path, SimulatorModelicaTemplate_Dymola_MOS)
MOS_TEMPLATE_PATH_OPENMODELICA = os.path.join(utilities_path, SimulatorModelicaTemplate_OpenModelica_MOS)
XSD_FILE_PATH = os.path.join(utilities_path, XSD_SCHEMA)
XML_INPUT_FILE = os.path.join(utilities_path, XML_MODELDESCRIPTION)
SimulatorToFMU_LIB_PATH = os.path.join(script_path, 'libraries', 'modelica')

def main():
    
    """
    Main function to export a Simulator as an FMU.


    """
    import argparse
    
    # Configure the argument parser
    
    parser = argparse.ArgumentParser(description='Export Simulator as a Functional Mock-up Unit')
    simulator_group = parser.add_argument_group("Arguments to export CYMDIST as an FMU")
    
    simulator_group.add_argument('-s', '--python-scripts-path',
                                required=True,
                                help='Path to the Python scripts '
                                + ' used to interface with simulator',
                                type=(lambda s: [item for item in s.split(',')]))

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
                        help='Export tool. Valid options are '
                        + '<dymola> for Dymola and'
                        + ' <omc> for OpenModelica')
    # Parse the arguments
    args = parser.parse_args()
    
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
    # Check if Simulator.py is in the list of functions
    if not('Simulator.py' in python_scripts_base):
        s = 'Simulator.py no found in the list of Python scripts ' + \
            str(python_scripts_path) 
        log.error(s)
        raise ValueError(s)

    # Check if the path exists
    for python_script_path in python_scripts_path:
        if(not os.path.exists(python_script_path)):
            s = 'The Path to the Python script ' + python_script_path + \
                ' provided does not exist.'
            log.error(s)
            raise ValueError(s)
                        
    # Check if it is a Python file
    for python_script_path in python_scripts_path:
        ext = os.path.splitext(python_script_path)[-1].lower()
        if (ext != '.py'):
            s = 'The Python script ' + python_script_path + \
                ' provided does not have a valid extension.'
            log.error(s)
            raise ValueError(s)

    # Get the xml files
    io_file_path = args.io_file_path
    if io_file_path is None :
        log.info('No XML input file was provided. '
                 + ' The default XML file which is at ' 
                 + XML_INPUT_FILE + " will be used.")
        io_file_path = XML_INPUT_FILE
        
    # Set the default configuration file
    con_path = ''
                
    # Get the input/output XML file definition
    io_file_path = args.io_file_path
    
    # Check if io file is empty
    if io_file_path is None :
        log.info('No XML input file was provided. The default XML file which is at ' 
                 + XML_INPUT_FILE + ' will be used.')
        io_file_path = XML_INPUT_FILE
    
    # Detect the version of Python and set it
    log.info ('This script generates FMUs for Python 2.7 and 3.5 target simulators only.')
    if (sys.version_info[0] < 3):
        log.info ('Set the Python version of the target simulator to be 2.7.')
        python_vers = '27'
        # Copy all resources file in a directory
        dir_name = 'Simulator.scripts'
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        log.info('Create the folder Simulator.scripts with scripts to be added to the PYTHONPATH')
        os.makedirs(dir_name)
        for python_script_path in python_scripts_path:
            shutil.copy2(python_script_path, dir_name)
        fnam = os.path.join(dir_name, "README.txt")
        fh = open(fnam, "w")
        readme = 'IMPORTANT:\n\n' + \
                'The files contains in this folder must be added to the PYTHONPATH.\n' + \
                'This can be done by adding the folder ' + dir_name + ' to the PYTHONPATH.\n\n' + \
                'This is needed because of CYTHON which is not adding the PYTHONPATH in the \n' + \
                'pythonInterpreter.c code.' + \
                'Failing to add the files to the PYTHONPATH will cause the FMU to fail to run.\n' + \
                'This issue can be reproduced with Python 2.7.\n' + \
                'Python 3.5 does not exhibit this behavior and hence can be used without the folder\n' + \
                'addition.'
        fh.write(readme)
        fh.close()
        dir_name_zip = dir_name + '.zip'
        if os.path.exists(dir_name_zip):
            os.remove(dir_name_zip)
        zip_fmu(dir_name, includeDirInZip=False)
        # Delete the folder created
        shutil.rmtree(dir_name)      
    else:
        log.info ('Set the Python version of the target simulator to be 3.5.')
        python_vers = '35'

    # Get the FMI version
    fmi_version = args.fmi_version
    
    # Check if fmi version is none
    if(fmi_version is None):
        log.info('FMI version not specified. Version 2.0 will be used.')
        fmi_version = '2.0'
    
    # Check if fmi version is valid
    if not (fmi_version in ['1.0', '2.0']):
        s = 'This version only supports FMI version 1.0 and 2.0.'
        log.error (s)
        raise ValueError(s)
    # Get the FMI API version
    fmi_api = args.fmi_api
    
    # Check if fmi api is none
    if(fmi_api is None):
        log.info('FMI API not specified. Model exchange (me) API will be used.')
        fmi_api = 'me'
    
    # Check if the fmi api is valid
    if not (fmi_api in ['me', 'cs']):
        s = 'This version only supports FMI model exchange(me) or co-simulation (cs) API.'
        log.error (s)
        raise ValueError(s)

    # Get the FMI API version
    export_tool = args.export_tool    
    if(export_tool is None):
        log.info('No export tool was specified. dymola the default will be used.')
        export_tool = 'dymola'
    
    # Check if export tool is valid
    if not (export_tool in ['dymola', 'omc']):
        s = 'Export tool specified is neither Dymola (dymola) nor OpenModelica(omc).'
        log.error (s)
        raise ValueError(s)
    
    # Define templates variables
    if(export_tool == 'dymola'):
        mos_template_path = MOS_TEMPLATE_PATH_DYMOLA
        # Convert the FMI version to int for Dymola
        fmi_version = int(float(fmi_version))
        modelica_path = 'MODELICAPATH'
    elif(export_tool == 'omc'):
        mos_template_path = MOS_TEMPLATE_PATH_OPENMODELICA 
        modelica_path = 'OPENMODELICALIBRARY'
    
    # Export the tool as an FMU
    Simulator = SimulatorToFMU(con_path,
                            io_file_path,
                            SimulatorToFMU_LIB_PATH,
                            MO_TEMPLATE_PATH_DYMOLA,
                            mos_template_path,
                            XSD_FILE_PATH,
                            python_vers,
                            python_scripts_path,
                            fmi_version,
                            fmi_api,
                            export_tool,
                            modelica_path)
    
    start = datetime.now()
    ret_val = Simulator.print_mo()
    if(ret_val != 0):
        s = 'Could not print the Simulator Modelica model. Error in print_mo().'
        parser.print_help()
        log.error (s)
        raise ValueError(s)
    ret_val = -1
    ret_val = Simulator.generate_fmu()
    if(ret_val != 0):
        s = 'Could not generate the Simulator FMU. Error in generate_fmu().'
        parser.print_help()
        log.error (s)
        raise ValueError(s)
    ret_val = -1
    ret_val = Simulator.clean_temporary()
    if(ret_val != 0):
        s = 'Could not clean temporary files. Error in clean_temporary().'
        parser.print_help()
        log.error (s)
        raise ValueError(s)
    # Rewrite FMUs for FMUs with version higher than 1.0
    if(float(fmi_version) > 1.0): 
        ret_val = -1
        ret_val = Simulator.rewrite_fmu()
        if(ret_val != 0):
            s = 'Could not rewrite Simulator FMU. Error in rewrite_fmu().'
            parser.print_help()
            log.error (s)
            raise ValueError(s)
    end = datetime.now()
     
    log.info('Export Simulator as an FMU in ' + 
          str((end - start).total_seconds()) + ' seconds.')

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
        log.error('There are duplicates names in the list '
                  + str(arr) + '.')
        log.error('This is invalid. Check your XML input file.')
        for i in lst_dup:
            log.error('Variable ' + i + ' has duplicates'
                      ' in the list ' + str(arr) + '.')
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
        log.warning('Variable Name ' + name + ' starts with 0.')
        log.warning('This is invalid.')
        log.warning('The name will be changed to start with f_.')
        name = 'f_' + name
    #
    # Replace all illegal characters with an underscore.
    name = g_rexBadIdChars.sub('_', name)
    #
    return(name)


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
                 modelica_path):
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
        :param export_tool (str): The export tool.

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
        self.modelica_path = modelica_path

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
        log.info('Invalid characters will be removed from the '
                 'model name  ' + self.model_name + '.')
        self.model_name = sanitize_name(self.model_name)
        log.info('The new model name is ' + self.model_name + '.')

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
                     'input variable name ' + name + '.')
                    new_name = sanitize_name(name)
                    log.info('The new input variable name is ' \
                             + new_name + '.')
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
                     'output variable name ' + name + '.')
                    new_name = sanitize_name(name)
                    log.info('The new output variable name is ' \
                             + new_name + '.')
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
                    log.info('Invalid characters will be removed from the '
                     'parameter variable name ' + name + '.')
                    new_name = sanitize_name(name)
                    log.info('The new parameter variable name is ' \
                             + new_name + '.')
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
                        log.warning('Start value of variable '
                                    + name + ' with causality '
                                    + causality + ' is not defined.'
                                    + 'The start value will be set to 0.0 by default.')
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
                scalar_variable['unit'] = unit
                if not (start is None):
                    scalar_variable['start'] = start
                scalar_variables.append(scalar_variable)
            # perform some checks on variables to avoid name clashes
            # before returning the variables to Modelica            
            log.info('Check for duplicates in input, output and parameter variable names')
            for i in [modelica_input_variable_names,
                      modelica_output_variable_names,
                      modelica_parameter_variable_names]:
                check_duplicates(i)
                
            log.info('Parsing of ' + self.xml_path + ' was successfull.')
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
        output_res = template.render(model_name=self.model_name,
                                     scalar_variables=scalar_variables,
                                     python_scripts_path=self.python_scripts_path,
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
            log.warning('The output file ' + output_file
                        + ' exists and will be overwritten.')
        with open(output_file, 'w') as fh:
            fh.write(output_res)
        fh.close()

        # Write success.
        log.info('The Modelica model ' + output_file + 
                 ' of ' + self.model_name + ' is successfully created.')
        log.info('The Modelica model ' + output_file + 
                 ' of ' + self.model_name + ' is in ' + os.getcwd() + '.')
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
        
        # Set the Modelica path to point to the Simulator Library
        current_library_path = os.environ.get(self.modelica_path)
        
        # Check if library path is none
        if (current_library_path is None):
            os.environ[self.modelica_path] = self.simulatortofmu_path
        else:
            os.environ[self.modelica_path] = self.simulatortofmu_path \
            + os.pathsep + current_library_path

        loader = jja2.FileSystemLoader(self.mosT_path)
        env = jja2.Environment(loader=loader)
        template = env.get_template('')

        output_res = template.render(model_name=self.model_name,
                                     fmi_version=self.fmi_version,
                                     fmi_api=self.fmi_api)
        # Write results in mo file which has the same name as the class name
        output_file = self.model_name + '.mos'
        if os.path.isfile(output_file):
            log.warning('The output file ' + output_file
                        + ' exists and will be overwritten.')
        with open(output_file, 'w') as fh:
            fh.write(str(output_res))
        fh.close()

        if (self.export_tool == 'dymola'):
            sp.call([self.export_tool, output_file])
        
        if (self.export_tool == 'omc'):
            sp.call([self.export_tool, output_file, 'SimulatorToFMU'])
        
        # Reset the library path to the default
        if not(current_library_path is None):
            os.environ[self.modelica_path] = current_library_path

        # Renamed the FMU to indicate target Python simulator
        fmu_name = self.model_name + '.fmu'
        # os.rename(self.model_name+'.fmu', fmu_name)

        # Write scuccess.
        log.info('The FMU ' + fmu_name + ' is successfully created.')
        log.info('The FMU ' + fmu_name + ' is in ' + os.getcwd() + '.')

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
            filelist = glob.glob (ext)
            for f in filelist:
                os.remove(f)
        return 0

    def rewrite_fmu(self):
        """
        Add needsExecutionTool to the Simulator FMU.

        This function unzips the FMU generated with generate_fmu(),
        reads the xml file, and add needsExecutionTool to the FMU capabilities.
        The function completes the process by re-zipping the FMU.
        The new FMU contains the modified XML file as well as the binaries.

        :return: 0 if success.
        
        
        """

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

        # Unzip folder which contains he FMU
        zip_ref = zipfile.ZipFile(fmu_name, 'r')
        zip_ref.extractall('.')
        zip_ref.close()

        log.info('The model description file will be rewritten' + 
                 ' to include the attribute ' + NEEDSEXECUTIONTOOL + 
                 ' set to true.')
        tree = ET.parse(MODELDESCRIPTION)
        # Get the root of the tree
        root = tree.getroot()
        # Add the needsExecution tool attribute
        root.attrib[NEEDSEXECUTIONTOOL] = 'true'
        tree.write(MODELDESCRIPTION, xml_declaration=True)
        if os.path.isfile(fmu_name):
            os.remove(fmu_name)

        # Switch back to the current working directory
        os.chdir(cwd)
        
        # sys.exit()
        # Pass the directory which will be zipped
        # and call the zipper function.
        zip_fmu(fmutmp, includeDirInZip=False)

        # Check if fmu_name exists in current directory
        # If that is the case, delete it or rename to tmp?
        fmu_name_original = fmu_name + '.original'
        if os.path.isfile(fmu_name):
            log.info('The original Simulator FMU ' + fmu_name + 
                     ' will be renamed to ' + fmu_name + '.original.')
            log.info('A modified version of the original will be created.')
            log.info('The difference between the original and the new FMU lies'
                     ' in the model description file of the new FMU which has'
                     ' the attribute ' + NEEDSEXECUTIONTOOL + ' set to true.')
            if os.path.isfile(fmu_name_original):
                os.remove(fmu_name_original)
            os.rename(fmu_name, fmu_name_original)

        # Rename the FMU name to be the name of the FMU
        # which will be used for the simulation. This FMU
        # contains the needsExecutionTool flag.
        os.rename(zipdir, fmu_name)

        # Delete temporary folder
        shutil.rmtree(fmutmp)

        # Write scuccess.
        log.info('The FMU ' + fmu_name + ' is successfully re-created.')
        log.info('The FMU ' + fmu_name + ' is in ' + os.getcwd() + '.')

        return 0

if __name__ == '__main__':
    # Try running this module!
    # Set defaults for command-line options.
    main()
