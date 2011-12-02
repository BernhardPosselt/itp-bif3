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
    
class AusrueckeordnungAdmin(admin.TabularInline):
	model = Ausrueckordnung
	extra = 0
    
class FahrzeugAdmin(admin.ModelAdmin):
	list_display = ('kuerzel', 'beschreibung')	
    
class MeldebildAdmin(admin.ModelAdmin):
	inlines = (AusrueckeordnungAdmin, )
	
class NewsAdmin(admin.ModelAdmin):
	list_display = ('titel', 'datum')
	
class WillkommenAdmin(admin.ModelAdmin):
	pass

admin.site.register(Willkommen, WillkommenAdmin)
admin.site.register(News, NewsAdmin)	    
admin.site.register(Einsatz, EinsatzAdmin)
admin.site.register(Meldebilder, MeldebildAdmin)
admin.site.register(Fahrzeuge, FahrzeugAdmin)
