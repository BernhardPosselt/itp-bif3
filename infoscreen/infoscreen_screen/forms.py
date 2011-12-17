#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Django imports
from django import forms
from django.contrib.auth.models import User
from django.conf import settings

# Project imports
from infoscreen.infoscreen_screen.models import *


class SettingsForm(forms.ModelForm):
    """This form is used to set values
    """
    collection_path = forms.CharField(label='', help_text='')
    xml_auth = forms.BooleanField(required=False, label='')
    update_interval = forms.IntegerField(label='Update Intervall in Sekunden', 
        help_text='Die Geschwindigkeit in der die Website auf neue Elemente prüfen \
            kann. Sollte nicht zu hoch sein, da das prüfen auf updates aufwändig ist')


    def save(self):
        """Saves the values into the config file
        """
        config = LaudioConfig(settings.WEBSITE_CFG)
        config.collectionPath = self.cleaned_data['collection_path']
        config.xmlAuth = self.cleaned_data['xml_auth']
        config.tokenLifespan = self.cleaned_data['token_lifespan']
        config.save()
