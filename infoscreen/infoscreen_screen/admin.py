#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from infoscreen.infoscreen_screen.models import *


class EinsatzAdmin(admin.ModelAdmin):
    list_display = ('adresse', 'hausnummer', 'stiege', 'alarmstufe', 'meldebild', 'erzeugt')
    list_filter = ("alarmstufe", 'postleitzahl')
    ordering = ("modifiziert",)
    date_hierarchy = 'erzeugt'
    search_fields = ["adresse", 'hausnummer']
    
admin.site.register(Einsatz, EinsatzAdmin)
