#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Django includes
from django.conf import settings
# Project includes
from infoscreen.inc.config import WebsiteConfig
from infoscreen.infoscreen_screen.parser import XML
import urllib2
import time
import threading

def xml_api_query():
    while True:
        config = WebsiteConfig(settings.WEBSITE_CFG)
        response = urllib2.urlopen(config.xml_url)
        xmlfile = response.read()
        einsatzxml = XML(xmlfile)
        time.sleep(5)
