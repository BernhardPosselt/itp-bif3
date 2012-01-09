#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Django imports
from django import forms
from django.contrib.auth.models import User
from django.conf import settings

# Project imports
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.config import WebsiteConfig


class SettingsForm(forms.Form):
    """This form is used to set values
    """
    xml_url = forms.URLField(label='XML URL', 
        help_text='Die URL die für neue Einsätze abgefragt wird.')
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
