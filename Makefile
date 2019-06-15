############################################################
# Makefile for the regression tests that are run on travis
############################################################

test-jmodelica:
	(cd simulatortofmu/bin && python runUnitTest.py)
