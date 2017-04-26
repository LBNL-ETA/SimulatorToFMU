#!/usr/bin/env python
#######################################################
# Script with unit tests for CyDER
#
# TSNouidui@lbl.gov                            2016-09-06
#######################################################
import unittest
import os, sys
from pyfmi import load_fmu
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
SimulatorModelicaTemplate_OpenModelica_MOS = 'SimulatorModelicaTemplate_OpenModelica.mos'
XML_MODELDESCRIPTION = 'SimulatorModelDescription.xml'
# Get the path to the templates files
script_path = os.path.dirname(os.path.realpath(__file__))
utilities_path = os.path.join(script_path, '..', 'parser', 'utilities')
PYTHON_SCRIPT_PATH=os.path.join(utilities_path, 'Simulator.py')
MO_TEMPLATE_PATH_DYMOLA = os.path.join(utilities_path, SimulatorModelicaTemplate_MO)
MOS_TEMPLATE_PATH_DYMOLA = os.path.join(utilities_path, SimulatorModelicaTemplate_Dymola_MOS)
MOS_TEMPLATE_PATH_OPENMODELICA = os.path.join(utilities_path, SimulatorModelicaTemplate_OpenModelica_MOS)
XSD_FILE_PATH = os.path.join(utilities_path, XSD_SCHEMA)
XML_INPUT_FILE = os.path.join(utilities_path, XML_MODELDESCRIPTION)
SimulatorToFMU_LIB_PATH = os.path.join(script_path, 'libraries', 'modelica')

Simulator_T = simulator.SimulatorToFMU('con_path',
                            XML_INPUT_FILE,
                            SimulatorToFMU_LIB_PATH,
                            MO_TEMPLATE_PATH_DYMOLA,
                            MOS_TEMPLATE_PATH_DYMOLA,
                            XSD_FILE_PATH,
                            '3.5',
                            PYTHON_SCRIPT_PATH,
                            '2.0',
                            'me',
                            'dymola',
                            'MODELICAPATH')



class Tester(unittest.TestCase):
    ''' 
    Class that runs all regression tests.
    
    '''

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


    def test_run_simulator_fmu(self):
        '''  
        Test the simulation of one Simulator FMU.

        '''

        # Parameters which will be arguments of the function
        start_time = 0.0
        stop_time  = 5.0
    
        # Path to configuration file
        path_config=os.path.abspath('config.json')
        simulator_con_val_str = bytes(path_config, 'utf-8')
        
        simulator_input_valref=[] 
        simulator_output_valref=[]
        
        fmu_path = os.path.join(script_path, '..', 'fmus', 'Dymola', 'Simulator.fmu')
        simulator = load_fmu(fmu_path, log_level=7)
        simulator.setup_experiment(start_time=start_time, stop_time=stop_time)
        
        # Define the inputs
        simulator_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
        simulator_input_values = [2520, 2520, 2520, 0, -120, 120]
        simulator_output_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
        
        # Get the value references of simulator inputs
        for elem in simulator_input_names:
            simulator_input_valref.append(simulator.get_variable_valueref(elem))   
            
        # Get the value references of simulator outputs 
        for elem in simulator_output_names:
            simulator_output_valref.append(simulator.get_variable_valueref(elem))  
    
        # Set the flag to save the results
        simulator.set('_saveToFile', 0)
        # Get value reference of the configuration file 
        simulator_con_val_ref = simulator.get_variable_valueref('_configurationFileName')
        
        # Set the configuration file
        simulator.set_string([simulator_con_val_ref], [simulator_con_val_str])
        
        # Initialize the FMUs
        simulator.initialize()
        
        # Call event update prior to entering continuous mode.
        simulator.event_update()
        
        # Enter continuous time mode
        simulator.enter_continuous_time_mode()
        
        print ('Starting the time integration' )    
        start = datetime.now()
        simulator.set_real(simulator_input_valref, simulator_input_values)
        print('This is the result of the angle IAngleA: ' 
              + str(simulator.get_real(simulator.get_variable_valueref('IAngleA'))))
        
        # Terminate FMUs
        simulator.terminate()
        end = datetime.now()
        
        print('Ran a single Simulator simulation in ' + 
              str((end - start).total_seconds()) + ' seconds.')

    def test_print_mo(self):
        '''  
        Test the function print_mo().

        '''

        # Testing function to print Modelica model.
        Simulator_T.print_mo()
        import filecmp

        # Check if file is the same as the reference.
        assert(filecmp.cmp
               ('Simulator.mo', 
                os.path.join(utilities_path, 'Simulator_ref.mo'))), \
                'Printed file is different' + \
                ' from reference Simulator_ref.mo.'

if __name__ == '__main__':
    unittest.main()
