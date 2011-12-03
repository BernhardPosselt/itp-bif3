# Django imports
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from infoscreen.gmapi import maps
from infoscreen.gmapi.forms.widgets import GoogleMap

# Project imports
from infoscreen.infoscreen_screen.models import *

class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':1100, 'height':750}))



