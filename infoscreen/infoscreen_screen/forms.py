#!/usr/bin/env python
#-*- coding:utf-8 -*-

# System imports
import os

# Django imports
from django import forms
from django.contrib.auth.models import User
from django.conf import settings

# Project imports
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import handle_uploaded_file
from infoscreen.inc.config import WebsiteConfig


class SettingsForm(forms.Form):
    """This form is used to set values
    """
    xml_url = forms.URLField(label='XML URL', 
        help_text='Die URL die für neue Einsätze abgefragt wird.')
    kml_file = forms.FileField(label='Google Maps KML Datei', 
        help_text='Die Datei aus welcher die Google Maps Favoriten (Hydranten)\
            ausgelesen werden.', required=False)
    gmap_key = forms.CharField(label='Google Maps API key', 
        help_text='Der Key, der benötigt wird, um sich mit Google Maps zu verbinden')
    title_msg = forms.CharField(label='Titel', 
        help_text='Der Titel der zuoberst auf der Website standardmäßig angezeigt wird')
    welcome_msg = forms.CharField(label='Willkommens Nachricht', 
        help_text='Die Nachricht, die in Friedenszeiten links angezeigt wird.')
    update_interval = forms.IntegerField(label='Update Intervall in Sekunden', 
        help_text='Die Geschwindigkeit in der die Website auf neue Elemente prüfen \
            kann. Sollte nicht zu hoch sein, da das prüfen auf updates aufwändig ist')


    def save(self):
        """Saves the values into the config file
        """
        config = WebsiteConfig(settings.WEBSITE_CFG)
        config.update_interval = self.cleaned_data['update_interval']
        config.xml_url = self.cleaned_data['xml_url']
        config.gmap_key = self.cleaned_data['gmap_key']
        config.welcome_msg = self.cleaned_data['welcome_msg']
        config.title_msg = self.cleaned_data['title_msg']
        config.save()
        
        
    def upload_kml(self, upload_file):
        """
        Checks if a the kml is already in the folder, if true, it deletes the 
        file and overwrites it
        
        Keyword arguments:
        upload_file -- The upload file object which we get from request.FILES
        """
        name = 'hydranten.kml'
        upload_theme_path = os.path.join( settings.MEDIA_ROOT, 'kml/' )
        dest_name = '%s%s' % (upload_theme_path, name)
        
        # check if theres already a kml file in the media with the same name
        # if so, just delete it
        if name in os.listdir( upload_theme_path ):
            os.unlink( dest_name )
        
        # move kml file to the kml folder
        handle_uploaded_file( upload_file, dest_name )
