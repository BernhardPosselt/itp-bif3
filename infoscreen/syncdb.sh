#!/bin/bash
rm ./infoscreen.db
python2 ./manage.py syncdb --noinput
