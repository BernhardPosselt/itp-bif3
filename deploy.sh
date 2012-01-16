#!/bin/bash

# purge and install infoscreen
apt-get -y purge infoscreen
dpkg -i infoscreen*.deb
apt-get -y -f install




