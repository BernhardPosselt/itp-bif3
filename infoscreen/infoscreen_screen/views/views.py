#!/usr/bin/env python
#-*- coding:utf-8 -*-

# System includes
from lxml import etree

# Django includes
from django.db.models import Count
from django.shortcuts import render

# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.infoscreen_screen.parser import *
import gtk.gdk

def index(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/index.html", ctx)


def settings(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/index.html", ctx)

def bildschirm_einsatz_links(request):
    """
    Doku
    """
    testxml = XML("tests/xml/einsatz.xml")
    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_einsatz_links.html", ctx)


def bildschirm_einsatz_rechts(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_einsatz_rechts.html", ctx)

def bildschirm_frieden_links(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_frieden_links.html", ctx)


def bildschirm_frieden_rechts(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_frieden_rechts.html", ctx)

   
def javascript(request, src):
    """Generates the javascript from templates

    Keyword arguments:
    src -- The javascript part which should be generated 
    """
    if src == 'update':
        tpl = 'javascript/update.js'
    elif src == 'gmaps':
        tpl = 'javascript/gmaps.js'
    return render(request, tpl)


def javascript_main(request, screen):
    """Generates the main javascript, we need this extra function to set screen
    and mission variables

    Keyword arguments:
    screen -- The screen where the js is loaded to, 0 for left, 1 for right
    """
    # check if we got frieden or einsatz
    missions = Einsaetze.objects.filter(abgeschlossen=False).aggregate( Count('id') )
    missions_len = missions['id__count']
    if missions_len == 0:
        mission = False
    else:
        mission = True
    ctx = {
        'screen': screen,
        'mission': mission
    }
    return render(request, 'javascript/main.js', ctx)
