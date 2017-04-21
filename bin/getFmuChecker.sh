#/bin/sh
#######################################################
# Script to get the fmuChecker from the repository on 
# Unix machines.
# TSNouidui@lbl.gov                            2016-09-06
#######################################################
# This script is used to 
# download the FMUChecker and copy
# to the folder where it will be afterwards
# used for running unitTests.
# This file must either be run before 
# the unit test. Alternatively
# follow the instructions in the 
# top level Readme.txt file.

rm -rf *.zip
version="$1"
echo $version
if [ ${#version} -lt 1 ];then 
  echo "FMUChecker version is not specified." 
  echo "Please specify the version of the FMU Checker to the script."
  echo "This will download the FMUChecker from the repository. If the version"
  echo "is not correctly specify, then the checker won't be found."
else
   echo "Version $version of the FMUChecker will be downloaded"
   echo "for Linux 64 and Windows 64 bit operating system." 
   echo "This version will be used by default for FMUChecker."
fi

svn export https://svn.fmi-standard.org/fmi/branches/public/Test_FMUs/Compliance-Checker/FMUChecker-$version-linux64.zip
svn export https://svn.fmi-standard.org/fmi/branches/public/Test_FMUs/Compliance-Checker/FMUChecker-$version-win64.zip

echo Unzip FMUChecker
unzip -o FMUChecker-$version-linux64.zip
unzip -o FMUChecker-$version-win64.zip

echo Copy unzipped directories to fmuChecker folder
rsync -a  FMUChecker-$version-linux64 ../fmuChecker
rsync -a  FMUChecker-$version-win64 ../fmuChecker

echo Copy the executable to the fmuChecker folder
cp FMUChecker-$version-linux64/fmuCheck.linux64 ../fmuChecker
cp FMUChecker-$version-win64/fmuCheck.win64.exe ../fmuChecker

echo Clean directories
rm -rf *.zip FMUChecker-$version-linux64 FMUChecker-$version-win64




