#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Laudio - A webbased musicplayer

Copyright (C) 2010 Bernhard Posselt, bernhard.posselt@gmx.at

Laudio is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Laudio is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Laudio.  If not, see <http://www.gnu.org/licenses/>.

"""

# System imports
import os
import ConfigParser
import re


class WebsiteConfig(object):
    """
    Interface for writing to the config file
    """
    
    def __init__(self, configs):
        """Constructor
    
        Keyword arguments:
        configs -- A dict with config filepaths
        """
        self.mainConfig = configs['MAIN_CFG']
        self.apacheConfig = configs['APACHE_CFG']
    
        # set default values
        self.parserError = False
        self.url = '/'
        self.collectionPath = ''
        # in seconds
        self.update_interval = 5
        self.xmlAuth = False
        
        # read in main config
        try:
            config = ConfigParser.SafeConfigParser(allow_no_value=True)
            config.read(self.mainConfig)
                
            try:
                self.collectionPath = config.get('settings', 'collection_path')
            except ConfigParser.NoOptionError:
                self.parserError = True
                
            try:
                self.tokenLifespan = config.getint('settings', 'update_interval')
            except ConfigParser.NoOptionError:
                self.parserError = True        

            try:
                self.xmlAuth = config.getboolean('settings', 'xml_auth')
            except ConfigParser.NoOptionError:
                self.parserError = True   

        # if there was something wrong with the config or parsing, write default
        # values
        except ConfigParser.NoSectionError:
            self.save()
        if self.parserError:
            self.save()
        
        # now try to read in the server config
        try:
            with open(self.apacheConfig, 'r') as confFile:
                conf = confFile.read()
                regex = r'WSGIScriptAlias (.*) .*wsgi/django.wsgi'
                url = re.search(regex, conf).group(1)
                if url.endswith('/'):
                    url = url[:-1]
                self.url = url
        # only for early developement
        except IOError:
            print "No Config file available or writeable!"


    def save(self):
        """Writes the current values into the configfile
        """
        config = ConfigParser.SafeConfigParser()
        config.add_section('settings')
        # music settings
        config.set('settings', 'collection_path', str(self.collectionPath))
        config.set('settings', 'update_interval', str(self.update_interval))
        config.set('settings', 'xml_auth', str(self.xmlAuth))
        try:
            with open(self.mainConfig, 'wb') as confFile:
                config.write(confFile)
        # only for early developement
        except IOError:
            print "No Config file available or writeable!"