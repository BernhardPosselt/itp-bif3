#!/usr/bin/env python
#-*- coding:utf-8 -*-

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
        self.xml_url = "http://127.0.0.1:8000/static/xml/infoscreen.xml"
        self.gmap_key = "ABQIAAAA6qiASEwfhYtcYhMd2vJTQRQorY6mP03n72EKZcQG5HcZqK1IwRSlvhuDn4o5b4Mzk8fUw0cst-Ix_Q"
        self.welcome_msg = 'Hallo'
        self.title_msg = 'Feuerwehr Infoscreen'
        self.update_interval = 10 # in seconds
        
        # read in main config
        try:
            config = ConfigParser.SafeConfigParser()
            config.read(self.mainConfig)
                
            try:
                self.xml_url = config.get('settings', 'xml_url')
            except ConfigParser.NoOptionError:
                self.parserError = True

            try:
                self.gmap_key = config.get('settings', 'gmap_key')
            except ConfigParser.NoOptionError:
                self.parserError = True

            try:
                self.welcome_msg = config.get('settings', 'welcome_msg')
            except ConfigParser.NoOptionError:
                self.parserError = True
            
            try:
                self.title_msg = config.get('settings', 'title_msg')
            except ConfigParser.NoOptionError:
                self.parserError = True

            try:
                self.update_interval = config.getint('settings', 'update_interval')
            except (ConfigParser.NoOptionError, ValueError):
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
            print "No Apache Config file available or writeable!"


    def save(self):
        """Writes the current values into the configfile
        """
        config = ConfigParser.SafeConfigParser()
        config.add_section('settings')
        # music settings
        config.set('settings', 'xml_url', str(self.xml_url))
        config.set('settings', 'update_interval', str(self.update_interval))
        config.set('settings', 'welcome_msg', str(self.welcome_msg))
        config.set('settings', 'title_msg', str(self.title_msg))
        config.set('settings', 'gmap_key', str(self.gmap_key))
        try:
            with open(self.mainConfig, 'wb') as confFile:
                config.write(confFile)
        # only for early developement
        except IOError:
            print "No Config file available or writeable!"
