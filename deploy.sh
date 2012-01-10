#!/bin/bash

# software needed to build: 
apt-get -y install dpkg-dev debhelper build-essential dh-make

# purge and install infoscreen
apt-get -y purge infoscreen --
git pull
./build
dpkg -i infoscreen*.deb
apt-get -y -f install




