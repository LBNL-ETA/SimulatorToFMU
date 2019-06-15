############################################################
# Makefile for the regression tests that are run on travis
############################################################
ROOT = .


test-experiment-setup:
	(cd $(ROOT)/Buildings; ../bin/runUnitTests.py --validate-experiment-setup)

test-dymola:
	(cd $(ROOT)/Buildings && python ../bin/runUnitTests.py --batch --single-package $(PACKAGE) --tool dymola)

test-jmodelica:
	(cd $(ROOT)/simulatortofmu/bin && python runUnitTests.py
