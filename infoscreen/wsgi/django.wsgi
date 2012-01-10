#!/usr/bin/env python
import os
import sys
from os.path import dirname
# append laudio's parent directory to the sys path
relPath = dirname(dirname(dirname( os.path.abspath(__file__) )))
sys.path.append(os.path.abspath(relPath))

os.environ['DJANGO_SETTINGS_MODULE'] = 'infoscreen.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
