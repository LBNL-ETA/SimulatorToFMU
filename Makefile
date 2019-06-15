############################################################
# Makefile for the regression tests that are run on travis
############################################################
ROOT = .


test-dymola:
	(cd $(ROOT)/Buildings && python ../bin/runUnitTests.py --batch --single-package $(PACKAGE) --tool dymola)

test-jmodelica:
	(cd $(ROOT)/simulatortofmu/bin && python runUnitTests.py
