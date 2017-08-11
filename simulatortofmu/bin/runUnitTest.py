#######################################################
# Script with unit tests for SimulatorToFMU
#
# TSNouidui@lbl.gov                          2016-09-06
#######################################################
import unittest
import os
import sys
import platform
import subprocess
import shutil
from datetime import datetime

# Appending parser_path to the system path os required to be able
# to find the SimulatorToFMU model from this directory
script_path = os.path.dirname(os.path.realpath(__file__))
parser_path = os.path.abspath(os.path.join(script_path, '..', 'parser'))
sys.path.append(parser_path)

import SimulatorToFMU as simulator

XSD_SCHEMA = 'SimulatorModelDescription.xsd'
NEEDSEXECUTIONTOOL = 'needsExecutionTool'
MODELDESCRIPTION = 'modelDescription.xml'
SimulatorModelicaTemplate_MO = 'SimulatorModelicaTemplate.mo'
SimulatorModelicaTemplate_Dymola_MOS = 'SimulatorModelicaTemplate_Dymola.mos'
SimulatorModelicaTemplate_JModelica_MOS = 'SimulatorModelicaTemplate_JModelica.py'
SimulatorModelicaTemplate_OpenModelica_MOS = 'SimulatorModelicaTemplate_OpenModelica.mos'
XML_MODELDESCRIPTION = 'SimulatorModelDescription.xml'
# Get the path to the templates files
script_path = os.path.dirname(os.path.realpath(__file__))
utilities_path = os.path.join(script_path, '..', 'parser', 'utilities')
PYTHON_SCRIPT_PATH = os.path.join(utilities_path, 'simulator_wrapper.py')
MO_TEMPLATE_PATH = os.path.join(utilities_path, SimulatorModelicaTemplate_MO)
MOS_TEMPLATE_PATH_DYMOLA = os.path.join(
    utilities_path, SimulatorModelicaTemplate_Dymola_MOS)
MOS_TEMPLATE_PATH_JMODELICA = os.path.join(
    utilities_path, SimulatorModelicaTemplate_JModelica_MOS)
MOS_TEMPLATE_PATH_OPENMODELICA = os.path.join(
    utilities_path, SimulatorModelicaTemplate_OpenModelica_MOS)
XSD_FILE_PATH = os.path.join(utilities_path, XSD_SCHEMA)
XML_INPUT_FILE = os.path.join(utilities_path, XML_MODELDESCRIPTION)
SimulatorToFMU_LIB_PATH = os.path.join(
    script_path, '..', 'parser', 'libraries', 'modelica')
python_scripts_path = [PYTHON_SCRIPT_PATH]

if(platform.system().lower() == 'windows'):
    python_scripts_path = [item.replace('\\', '\\\\') for item in [
        PYTHON_SCRIPT_PATH]]

Simulator_T = simulator.SimulatorToFMU('con_path',
                                       XML_INPUT_FILE,
                                       SimulatorToFMU_LIB_PATH,
                                       MO_TEMPLATE_PATH,
                                       MOS_TEMPLATE_PATH_DYMOLA,
                                       XSD_FILE_PATH,
                                       '27',
                                       python_scripts_path,
                                       '2.0',
                                       'me',
                                       'dymola',
                                       None,
                                       None,
                                       'false')





class Tester(unittest.TestCase):
    '''
    Class that runs all regression tests.

    '''
    
    def find_executable(self, tool):
        
        '''
        Function for checking if Dymola, JModelica, or OpenModelica is installed.

        '''
        
        if tool == 'jmodelica' and platform.system().lower() == "windows":
            tool = 'pylab'
        if tool == 'jmodelica' and platform.system().lower() == "linux":
            tool = 'jm_python.sh'
            
        if tool == 'openmodelica' and platform.system().lower() == "windows":
            tool = 'omc'
            
        cmd = "where" if platform.system() == "Windows" else "which"
        try: 
            return subprocess.call([cmd, tool])
        except: 
            print ("No executable for tool={!s}".format(tool))
            return 1

    def run_simulator (self, tool):
        
        '''
        Function for running FMUs exported from Dymola, JModelica, and OpenModelica with PyFMI.

        '''
        
        try:
            from pyfmi import load_fmu
        except BaseException:
            print ('PyFMI not installed. Test will not be be run.')
            return
        if (tool=='openmodelica' and platform.system().lower() == 'linux'):
                print ('tool={!s} is not supported on Linux'.format(tool))
                return
            
        else:
        # Export FMUs which are needed to run the cases.
            if tool == 'openmodelica':
                modPat = 'OPENMODELICALIBRARY'
                mosT = MOS_TEMPLATE_PATH_OPENMODELICA
            elif tool == 'dymola':
                modPat = 'MODELICAPATH'
                mosT = MOS_TEMPLATE_PATH_DYMOLA
            elif tool == 'jmodelica':
                # Unset environment variable
                if (os.environ.get('MODELICAPATH') is not None):
                    del os.environ['MODELICAPATH']
                modPat = None
                mosT = MOS_TEMPLATE_PATH_JMODELICA
            for version in ['2']:
                if (tool == 'openmodelica' or tool == 'jmodelica'):
                    version = str(float(version))
                for api in ['me']:
                    if (tool == 'openmodelica' and version == '1.0' and api == 'cs'):
                        print (
                            'tool={!s} with FMI version={!s} and FMI API={!s} is not supported.'.format(
                                tool, version, api))
                        continue
                    for cs_xml in ['true']:
                        if (version == '1'):
                            continue
                        Simulator_Test = simulator.SimulatorToFMU(
                            'con_path',
                            XML_INPUT_FILE,
                            SimulatorToFMU_LIB_PATH,
                            MO_TEMPLATE_PATH,
                            mosT,
                            XSD_FILE_PATH,
                            '27',
                            python_scripts_path,
                            version,
                            api,
                            tool,
                            None,
                            modPat,
                            cs_xml)

                        print (
                            'Export the simulator with tool={!s}, FMI version={!s}, FMI API={!s}'.format(
                                tool, version, api))
                        start = datetime.now()
                        Simulator_Test.print_mo()
                        Simulator_Test.generate_fmu()
                        Simulator_Test.clean_temporary()
                        Simulator_Test.rewrite_fmu()
                        end = datetime.now()
                        print(
                            'Export Simulator as an FMU in {!s} seconds.'.format(
                                (end - start).total_seconds()))
                        
                        fmu_path = os.path.join(
                        script_path, '..', 'fmus', tool, platform.system().lower())
                        print(
                            'Copy Simulator.fmu to {!s}.'.format(fmu_path))
                        shutil.copy2('Simulator.fmu', fmu_path)
    
        fmu_path = os.path.join(
                script_path, '..', 'fmus', tool, platform.system().lower(), 'Simulator.fmu')
        # Parameters which will be arguments of the function
        start_time = 0.0
        stop_time = 5.0

        print ('Starting the simulation with {!s}'.format(tool))
        start = datetime.now()

        simulator_input_valref = []
        simulator_output_valref = []

        sim_mod = load_fmu(fmu_path, log_level=7)
        sim_mod.setup_experiment(
            start_time=start_time, stop_time=stop_time)

        # Define the inputs
        simulator_input_names = ['v']
        simulator_input_values = [220.0]
        simulator_output_names = ['i']

        # Get the value references of simulator inputs
        for elem in simulator_input_names:
            simulator_input_valref.append(
                sim_mod.get_variable_valueref(elem))

        # Get the value references of simulator outputs
        for elem in simulator_output_names:
            simulator_output_valref.append(
                sim_mod.get_variable_valueref(elem))

        # Set the flag to save the results
        sim_mod.set('_saveToFile', 0)

        # Initialize the FMUs
        sim_mod.initialize()

        # Call event update prior to entering continuous mode.
        sim_mod.event_update()

        # Enter continuous time mode
        sim_mod.enter_continuous_time_mode()

        sim_mod.set_real(simulator_input_valref, simulator_input_values)
        
        end = datetime.now()

        print(
            'Ran a single Simulator simulation with {!s} FMU={!s} in {!s} seconds.'.format(
                tool, fmu_path, (end - start).total_seconds()))
        if not (tool=='openmodelica'):
            # PyFMI fails to get the output of an OpenModelica FMU 
            self.assertEqual(
                sim_mod.get_real(
                    sim_mod.get_variable_valueref('i')),
                1.0,
                'Values are not matching.')
            
        # Terminate FMUs
        sim_mod.terminate()

    def test_check_duplicates(self):
        '''
        Test the function check_duplicates().

        '''

        # Array does not contain duplicates variables.
        simulator.check_duplicates(['x1', 'x2', 'x3', 'x4'])

        # Array contain duplicates variables.
        with self.assertRaises(AssertionError):
            simulator.check_duplicates(['x1', 'x1', 'x3', 'x4'])

    def test_sanitize_name(self):
        '''
        Test the function sanitize_name().

        '''

        # Testing name conversions.
        name = simulator.sanitize_name('test+name')
        self.assertEqual(name, 'test_name', 'Names are not matching.')

        name = simulator.sanitize_name('0test+*.name')
        self.assertEqual(name, 'f_0test___name', 'Names are not matching.')

    def test_xml_validator(self):
        '''
        Test the function xml_validator().

        '''

        # Testing validation of xml file
        Simulator_T.xml_validator()

    def test_xml_parser(self):
        '''
        Test the function xml_validator().

        '''

        # Testing validation of xml file
        Simulator_T.xml_parser()

    def test_print_mo(self):
        '''
        Test the function print_mo().

        '''

        # Testing function to print Modelica model.
        Simulator_T.print_mo()

    def test_simulator_to_fmu(self):
        '''
        Test the export of an FMU with various options.

        '''

        for tool in  ['dymola', 'jmodelica', 'openmodelica']:       
            retVal=self.find_executable(tool)
            if ((retVal is not None) and retVal!=1):
                print("======tool={!s} was found. Unit Test will be run".format(tool))
            else:
                continue

            if (platform.system().lower() == 'linux' and tool == 'openmodelica'):
                print ('tool={!s} is not supported on Linux.'.format(tool))
                continue
            if tool == 'openmodelica':
                modPat = 'OPENMODELICALIBRARY'
                mosT = MOS_TEMPLATE_PATH_OPENMODELICA
            elif tool == 'dymola':
                modPat = 'MODELICAPATH'
                mosT = MOS_TEMPLATE_PATH_DYMOLA
            elif tool == 'jmodelica':
                if (os.environ.get('MODELICAPATH') is not None):
                    del os.environ['MODELICAPATH']
                modPat = None
                mosT = MOS_TEMPLATE_PATH_JMODELICA
            for version in ['1', '2']:
                if (tool == 'openmodelica' or tool == 'jmodelica'):
                    version = str(float(version))
                for api in ['me', 'cs']:
                    if (tool == 'openmodelica' and version == '1.0' and api == 'cs'):
                        print (
                            'tool={!s} with FMI version={!s} and FMI API={!s} is not supported.'.format(
                                tool, version, api))
                        continue
                    for cs_xml in ['true']:
                        if (version == '1'):
                            continue
                        Simulator_Test = simulator.SimulatorToFMU(
                            'con_path',
                            XML_INPUT_FILE,
                            SimulatorToFMU_LIB_PATH,
                            MO_TEMPLATE_PATH,
                            mosT,
                            XSD_FILE_PATH,
                            '27',
                            python_scripts_path,
                            version,
                            api,
                            tool,
                            None,
                            modPat,
                            cs_xml)

                        print (
                            'Export the simulator with tool={!s}, FMI version={!s}, FMI API={!s}'.format(
                                tool, version, api))
                        start = datetime.now()
                        Simulator_Test.print_mo()
                        Simulator_Test.generate_fmu()
                        Simulator_Test.clean_temporary()
                        Simulator_Test.rewrite_fmu()
                        end = datetime.now()
                        print(
                            'Export Simulator as an FMU in {!s} seconds.'.format(
                                (end - start).total_seconds()))
                              
    def test_updates_fmu(self):
        '''
        Test the export and updates of FMUs.

        '''

        for tool in  ['dymola', 'jmodelica', 'openmodelica']:       
            retVal=self.find_executable(tool)
            if ((retVal is not None) and retVal!=1):
                print("======tool={!s} was found. Unit Test will be run".format(tool))
            else:
                continue
            
            if (platform.system().lower() == 'linux' and tool == 'openmodelica'):
                print ('tool={!s} is not supported on Linux.'.format(tool))
                continue
            if tool == 'openmodelica':
                modPat = 'OPENMODELICALIBRARY'
                mosT = MOS_TEMPLATE_PATH_OPENMODELICA
            elif tool == 'dymola':
                modPat = 'MODELICAPATH'
                mosT = MOS_TEMPLATE_PATH_DYMOLA
            elif tool == 'jmodelica':
                if (os.environ.get('MODELICAPATH') is not None):
                    del os.environ['MODELICAPATH']
                modPat = None
                mosT = MOS_TEMPLATE_PATH_JMODELICA
            for version in ['2']:
                if (tool == 'openmodelica' or tool == 'jmodelica'):
                    version = str(float(version))
                for api in ['me']:
                    if (tool == 'openmodelica' and version == '1.0' and api == 'cs'):
                        print (
                            'tool={!s} with FMI version={!s} and FMI API={!s} is not supported.'.format(
                                tool, version, api))
                        continue
                    for cs_xml in ['true']:
                        if (version == '1'):
                            continue
                        Simulator_Test = simulator.SimulatorToFMU(
                            'con_path',
                            XML_INPUT_FILE,
                            SimulatorToFMU_LIB_PATH,
                            MO_TEMPLATE_PATH,
                            mosT,
                            XSD_FILE_PATH,
                            '27',
                            python_scripts_path,
                            version,
                            api,
                            tool,
                            None,
                            modPat,
                            cs_xml)

                        print (
                            'Export the simulator with tool={!s}, FMI version={!s}, FMI API={!s}'.format(
                                tool, version, api))
                        start = datetime.now()
                        Simulator_Test.print_mo()
                        Simulator_Test.generate_fmu()
                        Simulator_Test.clean_temporary()
                        Simulator_Test.rewrite_fmu()
                        end = datetime.now()
                        print(
                            'Export Simulator as an FMU in {!s} seconds.'.format(
                                (end - start).total_seconds()))
                        fmu_path = os.path.join(
                        script_path, '..', 'fmus', tool, platform.system().lower())
                        print(
                            'Copy Simulator.fmu to {!s}.'.format(fmu_path))
                        shutil.copy2('Simulator.fmu', fmu_path)
                        
    def test_run_simulator_all(self):
        '''
        Test the execution of one Simulator FMU.

        '''

        # Export FMUs which are needed to run the cases.
        for tool in  ['dymola', 'jmodelica', 'openmodelica']:       
            retVal=self.find_executable(tool)
            if ((retVal is not None) and retVal!=1):
                print("======tool={!s} was found. Unit Test will be run.".format(tool))
                print('=======The unit test will be run for tool={!s}.'.format(tool))
                self.run_simulator (tool)
            else:
                continue

    def test_run_simulator_dymola(self):
        '''
        Test the execution of one Simulator FMU.

        '''
        
        retVal=self.find_executable('dymola')
        if ((retVal is not None) and retVal!=1):
            print("======tool=dymola was found. Unit Test will be run.")
            print('=======The unit test will be run for Dymola.')
            print('=======Make sure that Dymola is on the System Path otherwise the simulation will fail.')
            # Run the cases
            self.run_simulator ('dymola')
        else:
            return
    
    def test_run_simulator_jmodelica(self):
        '''
        Test the execution of one Simulator FMU.

        '''
        
        retVal=self.find_executable('jmodelica')
        if ((retVal is not None) and retVal!=1):
            print("======tool=jmodelica was found. Unit Test will be run.")
            print('=======The unit test will be run for JModelica.')
            print('=======Make sure that JModelica is on the System Path otherwise the simulation will fail.')
            # Run the cases
            self.run_simulator ('jmodelica')
        else:
            return
        
    def test_run_simulator_openmodelica(self):
        '''
        Test the execution of one Simulator FMU.

        '''
        
        retVal=self.find_executable('openmodelica')
        if ((retVal is not None) and retVal!=1):
            print("======tool=openmodelica was found. Unit Test will be run.")
            print('=======The unit test will be run for OpenModelica.')
            print('=======Make sure that OpenModelica is on the System Path otherwise the simulation will fail.')
            # Run the cases
            self.run_simulator ('openmodelica')
        else:
            return
                                    
if __name__ == "__main__":
        # Check command line options
    if (platform.system().lower() in ['windows', 'linux']):
        unittest.main()
    else:
        print('=========SimulatorToFMU is only supported on Linux and Windows.')
