#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from infoscreen.infoscreen_screen.models import *

class DispoAdmin(admin.TabularInline):
	model = Dispos
	extra = 0

class EinsatzAdmin(admin.ModelAdmin):
    list_display = ('objekt', 'bemerkung','nummer1', 'strasse', 'plz', 'ort','meldebild', 'einsatzerzeugt')
    list_filter = ("meldebild__stufe", "meldebild", 'modifiziert')
    ordering = ("modifiziert",)
    date_hierarchy = 'einsatzerzeugt'
    search_fields = ["nummer1", 'nummer2']
    inlines = (DispoAdmin, )
    
    
class AusrueckeordnungAdmin(admin.TabularInline):
	model = Ausrueckordnungen
	sortable_field_name = "position"
	extra = 0
    
class FahrzeugAdmin(admin.ModelAdmin):
	list_display = ('kuerzel', 'beschreibung')	

class GeraetAdmin(admin.ModelAdmin):
	list_display = ('beschreibung',)	

class MeldebildAdmin(admin.ModelAdmin):	
	list_display = ('beschreibung', 'stufe');
	ordering = ('stufe',)
	search_fields = ['beschreibung']
	inlines = (AusrueckeordnungAdmin, )
	
class NewsAdmin(admin.ModelAdmin):
	list_display = ('titel', 'datum')


admin.site.register(News, NewsAdmin)	    
admin.site.register(Einsaetze, EinsatzAdmin)
admin.site.register(Meldebilder, MeldebildAdmin)
admin.site.register(Fahrzeuge, FahrzeugAdmin)
admin.site.register(Geraete, GeraetAdmin)
