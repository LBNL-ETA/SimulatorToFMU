############################################################
# Makefile for the regression tests that are run on travis
############################################################
ROOT = .

IMG_NAME=simulatortofmu_master

COMMAND_RUN=docker run \
	  --name simulatortofmu \
	  --detach=false \
	  -e DISPLAY=${DISPLAY} \
	  -v /tmp/.X11-unix:/tmp/.X11-unix \
	  --rm \
	  -v `pwd`:/mnt/shared \
	  -i \
          -t \
	  ${IMG_NAME} /bin/bash -c


build:
	docker build --no-cache --rm -t ${IMG_NAME} .

remove-image:
	docker rmi -f ${IMG_NAME}

run:
	$(COMMAND_RUN) \
            "cd ~/git/simulatortofmu/SimulatorToFMU/simulatortofmu/bin && bash jm_python.sh runUnitTest.py"

test-documentation:
	(cd $(ROOT)/simulatortofmu/doc/userGuide && make dist)

test-jmodelica:
	(cd $(ROOT)/ && make build run remove-image)
