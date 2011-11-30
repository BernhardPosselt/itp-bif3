# Django imports
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from infoscreen.gmapi import maps
from infoscreen.gmapi.forms.widgets import GoogleMap


class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':900, 'height':900}))


# Project imports
from infoscreen.infoscreen_screen.models import *
