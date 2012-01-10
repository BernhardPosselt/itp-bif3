#!/usr/bin/env python

import sys, os
from os.path import dirname, abspath

# append infoscreens's parent directory to the sys path
relPath = dirname(dirname(dirname( abspath(__file__) )))
sys.path.append(abspath(relPath))

os.environ['DJANGO_SETTINGS_MODULE'] = 'infoscreen.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

