FROM michaelwetter/ubuntu-1804_jmodelica_trunk

######################
# SimulatorToFMU Docker
######################
ENV ROOT_DIR /usr/local

USER root

RUN apt-get update && apt-get install -y \
	git

# Add a symbolink to Energy+.idd
# RUN ["ln", "-s", "/usr/local/JModelica/bin/jm_python.sh", "/usr/local/JModelica/bin/jm_python.sh"]

USER developer
WORKDIR $HOME

RUN pip install --user \
	lxml \
	jinja2

RUN mkdir git && cd git && \
    mkdir simulatortofmu && cd simulatortofmu && git clone https://github.com/LBNL-ETA/SimulatorToFMU.git

ENV PYTHONPATH $PYTHONPATH:$HOME/git/simulatortofmu/SimulatorToFMU/simulatortofmu/parser/utilities

ENV PATH $PATH:"/usr/local/JModelica/bin"

#WORKDIR $ROOT_DIR
