#!/usr/bin/env python
#-*- coding:utf-8 -*-

# System includes
from lxml import etree

# Django includes
from django.db.models import Count
from django.conf import settings
from django.shortcuts import render

# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.infoscreen_screen.parser import *
from infoscreen.inc.config import WebsiteConfig
from infoscreen.inc.shortcuts import is_mission
import gtk.gdk

def index(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/index.html", ctx)


def website_settings(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/index.html", ctx)

def bildschirm_einsatz_links(request):
    """
    Doku
    """
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
    config = WebsiteConfig(settings.WEBSITE_CFG)
    ctx = {
        'config': config
    }
    if src == 'update':
        tpl = 'javascript/update.js'
    elif src == 'gmaps':
        tpl = 'javascript/gmaps.js'
    return render(request, tpl, ctx)


def javascript_main(request, screen, mission):
    """Generates the main javascript, we need this extra function to set screen
    and mission variables

    Keyword arguments:
    screen -- The screen where the js is loaded to, 0 for left, 1 for right
    missino -- If the current view represents a mission 1, otherwise 0
    """
    # check if we got frieden or einsatz
    mission = int(mission)
    if mission == 1:
        mission = True
    else:
        mission = False
    ctx = {
        'screen': screen,
        'mission': mission
    }
    return render(request, 'javascript/main.js', ctx)
