#!/bin/sh
echo "!! This program will set up everything you need to use the GeniSys NLU Engine !!"
echo " "
echo "-- Installing requirements.txt"
pip3 install --upgrade pip
pip3 install -r requirements.txt --user
echo " "
echo "-- Installing MITIE"
git clone https://github.com/mit-nlp/MITIE.git
cd MITIE/mitielib
mkdir build && cd build
cmake ..
cmake --build . --config Release --target install