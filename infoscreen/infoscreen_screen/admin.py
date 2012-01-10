#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from infoscreen.infoscreen_screen.models import *

def finish(modeladmin, request, queryset):
	queryset.update(abgeschlossen=True)
finish.short_description = "Einsaetze abschliessen"

def unfinish(modeladmin, request, queryset):
	queryset.update(abgeschlossen=False)
unfinish.short_description = "Einsaetze aktivieren"

def printed(modeladmin, request, queryset):
	queryset.update(ausgedruckt=True)
printed.short_description = "Einsaetze als ausgedruckt markieren"

def notprinted(modeladmin, request, queryset):
	queryset.update(ausgedruckt=False)
notprinted.short_description = "Einsaetze als nicht ausgedruckt markieren"

def inrepairvehicles(modeladmin, request, queryset):
	queryset.update(reperatur=True)
inrepairvehicles.short_description = "Fahrzeuge in Reparatur"

def notinrepairvehicles(modeladmin, request, queryset):
	queryset.update(reperatur=False)
notinrepairvehicles.short_description = "Fahrzeuge nicht in Reparatur"

def inrepairutils(modeladmin, request, queryset):
	queryset.update(reperatur=True)
inrepairutils.short_description = "Geraete in Reparatur"

def notinrepairutils(modeladmin, request, queryset):
	queryset.update(reperatur=False)
notinrepairutils.short_description = "Geraete nicht in Reparatur"

def released(modeladmin, request, queryset):
	queryset.update(released=True)
released.short_description = "News veroeffentlichen"

def unreleased(modeladmin, request, queryset):
	queryset.update(released=False)
unreleased.short_description = "News nicht veroeffentlichen"


class DispoAdmin(admin.TabularInline):
	model = Dispos
	extra = 0

class EinsatzAdmin(admin.ModelAdmin):
    list_display = ('einsatz', 'bemerkung','nummer1', 'strasse', 'plz', 'ort',
                    'meldebild', 'einsatzerzeugt', 'abgeschlossen')
    list_filter = ("meldebild__stufe", "abgeschlossen", "meldebild", 'modifiziert')
    ordering = ("modifiziert",)
    date_hierarchy = 'einsatzerzeugt'
    search_fields = ["nummer1", "strasse", "plz", "ort", "bemerkung"]
    inlines = (DispoAdmin, )
    actions = [finish, unfinish, printed, notprinted]
    
    
class AusrueckeordnungAdmin(admin.TabularInline):
	model = Ausrueckordnungen
	sortable_field_name = "position"
	extra = 0
    
class FahrzeugAdmin(admin.ModelAdmin):
	list_display = ('kuerzel', 'funkrufname', 'beschreibung', 'reperatur')
	list_filter = ("reperatur", )
	search_fields = ["kuerzel", "funkrufname", "beschreibung"]
	actions = [inrepairvehicles, notinrepairvehicles]	

class GeraetAdmin(admin.ModelAdmin):
	list_display = ('beschreibung', 'reperatur')
	list_filter = ("reperatur", )	
	search_fields = ["beschreibung"]
	actions = [inrepairutils, notinrepairutils]

class MeldebildAdmin(admin.ModelAdmin):	
	list_display = ('beschreibung', 'stufe');
	list_filter = ("stufe", )
	ordering = ('stufe',)
	search_fields = ['beschreibung']
	inlines = (AusrueckeordnungAdmin, )
	
class NewsAdmin(admin.ModelAdmin):
	list_display = ('titel', 'datum')
	list_filter = ("released", "datum")
	search_fields = ["titel", "beschreibung"] 
	actions = [released, unreleased]


admin.site.register(News, NewsAdmin)	    
admin.site.register(Einsaetze, EinsatzAdmin)
admin.site.register(Meldebilder, MeldebildAdmin)
admin.site.register(Fahrzeuge, FahrzeugAdmin)
admin.site.register(Geraete, GeraetAdmin)
