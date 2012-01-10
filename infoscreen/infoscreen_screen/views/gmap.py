#!/usr/bin/env python
#-*- coding:utf-8 -*-

# System includes

# Django includes
from django.shortcuts import render
from django.conf import settings

# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.config import WebsiteConfig

def gmap(request, id):
    """
    Gmap.html wird augerufen und der Googlemap_API key
    wird aus der Config-Datei übergeben
    """
    config = WebsiteConfig(settings.WEBSITE_CFG)
   
    ctx = {
        'id': id,
        'key': config.gmap_key
    }
    return render(request, "infoscreen_screen/gmap/gmap.html", ctx)


def gmap_adresse(request, id):
    """
    Der Javascript Datei gmaps.js werden die Werte des 
    angefragten Einsatzes übergeben
    """
    einsatz = Einsaetze.objects.get(id=id)
    
   
    tpl = 'javascript/gmaps.js'
    print einsatz.ort
    ctx = {
        'plz': einsatz.plz,
        'ort': einsatz.ort,
        'strasse': einsatz.strasse,
        'hausnummer': einsatz.nummer1,
    }
    return render(request, tpl,ctx)
