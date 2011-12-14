#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from infoscreen.infoscreen_screen.models import *

class EinsatzAdmin(admin.ModelAdmin):
    list_display = ('nummer1', 'nummer2', 'nummer3', 'meldebild', 'einsatzerzeugt')
    list_filter = ("meldebild", 'plz')
    ordering = ("modifiziert",)
    date_hierarchy = 'einsatzerzeugt'
    search_fields = ["nummer1", 'nummer2']
    
    
class AusrueckeordnungAdmin(admin.TabularInline):
	model = Ausrueckordnung
	sortable_field_name = "position"
	extra = 0
    
class FahrzeugAdmin(admin.ModelAdmin):
	list_display = ('kuerzel', 'beschreibung')	
    
class MeldebildAdmin(admin.ModelAdmin):	
	list_display = ('beschreibung', 'stufe');
	ordering = ('stufe',)
	search_fields = ['beschreibung']
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
