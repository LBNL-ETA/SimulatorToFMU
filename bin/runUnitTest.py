#!/usr/bin/env python
#######################################################
# Script with unit tests for CyDER
#
# TSNouidui@lbl.gov                            2016-09-06
#######################################################
import unittest
import os
import sys
import logging
from subprocess import call

# Appending parser_path to the system path os required to be able
# to find the CYMDISTToFMU model from this directory
script_path = os.path.dirname(os.path.realpath(__file__))
parser_path = os.path.abspath(os.path.join(script_path, '..', 'parser'))
sys.path.append(parser_path)

import CYMDISTToFMU as cymdist

CYMDISTToFMU_LIB_PATH = ''
utilities_path = os.path.abspath(os.path.join(script_path, '..', 'parser', 'utilities'))
XSD_FILE_PATH = os.path.join(utilities_path, 'CYMDISTModelDescription.xsd')
XML_INPUT_PATH = os.path.join(utilities_path, 'CYMDISTModelDescription.xml')
INPUT_FILE_PATH = os.path.join(utilities_path, 'CYMDIST.inp')
MO_TEMPLATE_PATH = os.path.join(utilities_path, 'CYMDISTModelicaTemplate.mo')
MOS_TEMPLATE_PATH = os.path.join(utilities_path, 'CYMDISTModelicaTemplate.mos')

CYMDIST_T = cymdist.CYMDISTToFMU(XML_INPUT_PATH,
                                CYMDISTToFMU_LIB_PATH,
                                MO_TEMPLATE_PATH, 
                                MOS_TEMPLATE_PATH,
                                XSD_FILE_PATH)



class Tester(unittest.TestCase):
    ''' Class that runs all regression tests.
    '''

    def test_check_duplicates(self):
        '''  Test the function check_duplicates().

        '''

        # Array does not contain duplicates variables.
        cymdist.check_duplicates(['x1', 'x2', 'x3', 'x4'])

        # Array contain duplicates variables.
        with self.assertRaises(AssertionError):
            cymdist.check_duplicates(['x1', 'x1', 'x3', 'x4'])

    def test_sanitize_name(self):
        '''  Test the function sanitize_name().

        '''

        # Testing name conversions.
        name = cymdist.sanitize_name('test+name')
        self.assertEqual(name, 'test_name', 'Names are not matching.')

        name = cymdist.sanitize_name('0test+*.name')
        self.assertEqual(name, 'f_0test___name', 'Names are not matching.')

    def test_xml_validator(self):
        '''  Test the function xml_validator().

        '''

        # Testing validation of xml file
        CYMDIST_T.xml_validator()

    def test_xml_parser(self):
        '''  Test the function xml_validator().

        '''

        # Testing validation of xml file
        CYMDIST_T.xml_parser()

    def test_print_mo(self):
        '''  Test the function print_mo().

        '''

        # Testing function to print Modelica model.
        CYMDIST_T.print_mo()
        import filecmp

        # Check if file is the same as the reference.
        assert(filecmp.cmp
               ('CYMDIST.mo', 
                os.path.join(utilities_path, 'CYMDIST_ref.mo'))), \
                'Printed file is different' + \
                ' from reference CYMDIST_ref.mo.'

    @unittest.skip("Skipping running FMU checker")
    def test_fmucheker_cyder_fmus(self):
        '''  Test FMU with FMU checker

        Detect the operating system,
        switch to the folder which contains FMUs
        with correct binaries, call the fmuChecker
        to run the FMUs with default settings.
        To run the test, the user must make sure
        that the fmuChecker executables are in the
        fmuChekcker folders. These executables
        can be obtained from the fmi-standard
        svn repository.

        '''
        # Log file with logging messages.
        LOG_FILENAME = 'cyder_fmus.log'
        # Set basic configuration.
        logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
        # To stream the logging messages to the standard output.
        logging.getLogger().addHandler(logging.StreamHandler())
        # Identify system.
        PLATFORM_NAME = sys.platform
        is_64bits = sys.maxsize > 2**32
        #
        if(PLATFORM_NAME.startswith('win')):
            if(is_64bits):
                FMU_ARCH = 'win64'
            else:
                FMU_ARCH = 'win32'
        elif(PLATFORM_NAME.startswith('linux')):
            if(is_64bits):
                FMU_ARCH = 'linux64'
            else:
                FMU_ARCH = 'linux32'
        elif(PLATFORM_NAME.startswith('darwin')):
            if(is_64bits):
                FMU_ARCH = 'darwin64'
            else:
                FMU_ARCH = 'darwin32'
        # Set working directory to the one containing this file.
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        # Get the path to the FMUs.
        # This directory depends on the
        # operating system architecture.
        fmus_dir = os.path.join('..', 'fmus', FMU_ARCH)

        # define number of FMUs
        n_fmus = 0

        # Set the path to the fmuChecker
        fmu_checker = os.path.join('..', 'fmuChecker', 'fmuCheck.' + FMU_ARCH)
        logging.info('This is the path to the fmuChecker: ' + str(fmu_checker))

        # Walk through the directories and run unit tests for all found FMUs.
        for root, dirs, files in os.walk(fmus_dir):
            for fil in files:
                if fil.endswith('.fmu'):
                    n_fmus = n_fmus + 1
                    logging.info('Found FMU: ' + str(fil) +
                                 ' in directory: ' + str(root))
                    # Get the path to the FMU
                    fmu_path = os.path.join(root, fil)
                    # Call and execute the fmuChecker
                    logging.info('Run the fmuChecker for FMU: ' + str(fil))
                    call([fmu_checker, fmu_path])

        # Report the number of FMUs checked
        if (n_fmus != 0):
            logging.info('Ran fmuChecker for ' + str(n_fmus) + ' FMU(s).')
        else:
            logging.warning('There is no FMU to check in the FMU folder.')

        # Assert if the number of successful runs is less than one
        self.assertTrue(n_fmus > 0)

if __name__ == '__main__':
    unittest.main()
