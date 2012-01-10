#!/bin/bash

# software needed to build: 
# sudo apt-get install dpkg-dev debhelper build-essential dh-make

build_pkg=/usr/bin/dpkg-buildpackage


# create build dir and copy relevant files into it
mkdir build
cp -r infoscreen/ build/
cp -r dist/ build/
cp -r doc/ build/
cp AUTHORS build/
cp COPYING build/
cp MANIFEST.in build/
cp README.rst build/
cp setup.py build/

# remove non wanted files
rm -rf build/doc/tutorials
rm -rf build/dist/Druckjob
rm -f build/dist/Django-1.3.1.tar.gz

# create infoscreen folder and package
mkdir infoscreen-1.0
mv build/* infoscreen-1.0
mv infoscreen-1.0 build/
cd build/
tar czf infoscreen_1.0.orig.tar.gz infoscreen-1.0

# now make a sandbox and move files into it
mkdir sandbox
mv infoscreen-1.0 sandbox/
mv infoscreen_1.0.orig.tar.gz sandbox/
cp -r ../debian sandbox/infoscreen-1.0/

# change into directory and build package
cd sandbox/infoscreen-1.0
$build_pkg

# copy deb file into root folder and rm build folder
cd ..
cp *.deb ../../
cd ../../
rm -rf build/



