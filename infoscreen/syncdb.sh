#!/bin/bash

# This file is a simple shortcut for deleting and recreating the database
# It's used to alter the table structure, i.e. when models changed

# check if python2 exists, otherwise use python as interpreter
if [ -e "/usr/bin/python2" ]; then
    PYTHON_INT="/usr/bin/python2"
else 
    PYTHON_INT="/usr/bin/python"
fi

# remove database and syncdb
rm -rf ./infoscreen.db
$PYTHON_INT ./manage.py syncdb --noinput
