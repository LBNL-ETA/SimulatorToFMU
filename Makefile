############################################################
# Makefile for the regression tests that are run on travis
############################################################
ROOT = .

test-documentation:
	(cd simulatortofmu/doc/userGuide && make dist)

test-jmodelica:
	(cd $(ROOT)/simulatortofmu/bin && python runUnitTest.py)
