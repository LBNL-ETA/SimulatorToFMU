import os
from setuptools import setup
# Python setup file.
# See http://packages.python.org/an_example_pypi_project/setuptools.html


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="SimulatorToFMU",
    version="1.0.0rc12",
    author="Thierry S. Nouidui",
    author_email="TSNouidui@lbl.gov",
    description=("Package for exporting a Simulator as a Functional Mock-up Unit"),
    long_description=read('README.rst'),
    license="3-clause BSD",
    url="https://github.com/LBNL-ETA/SimulatorToFMU/",
    install_requires=['lxml',
                      'jinja2'],
    packages=['simulatortofmu'],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities"
    ]
)
