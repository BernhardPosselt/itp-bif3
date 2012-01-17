# This file can be called as standalone script to update the database entries
# from the xml api interface


# system imports
import urllib, urllib2
import os

# add settings to syspath to be able to execute code of the project
os.environ['DJANGO_SETTINGS_MODULE'] = infoscreen.settings

# django imports
from django.core.urlresolvers import reverse
from django.conf import settings

# Project includes
from infoscreen.inc.config import WebsiteConfig
from infoscreen.infoscreen_screen.parser import XML


def main():
    try:
        config = WebsiteConfig(settings.WEBSITE_CFG)
        response = urllib2.urlopen(config.xml_url)
        xmlfile = response.read()
        einsatzxml = XML(xmlfile)
    except(urllib2.HTTPError, urllib2.URLError):
        pass
        
        
if __name__ == '__main__':
    main()




