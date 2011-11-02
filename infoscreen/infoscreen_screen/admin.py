#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from infoscreen.infoscreen_screen.models import *


class EinsatzAdmin(admin.ModelAdmin):
    list_display = ('adresse', 'hausnummer', 'stiege', 'alarmstufe', 'meldebild')
    list_filter = ("alarmstufe",)
    ordering = ("modifiziert",)
    
admin.site.register(Einsatz, EinsatzAdmin)
