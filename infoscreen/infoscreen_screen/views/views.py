#!/usr/bin/env python
#-*- coding:utf-8 -*-

# System includes


# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render
from lxml import etree
from infoscreen.infoscreen_screen.parser import *

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

def bildschirm_links(request):
    """
    Doku
    """
    testxml = XML("tests/xml/eldisdata.xml")
    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_links.html", ctx)


def bildschirm_rechts(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_rechts.html", ctx)
   
   
def javascript(request, src):
    """Generates the javascript from templates

    Keyword arguments:
    src -- The javascript part which should be generated 
    """
    if src == 'main':
        tpl = 'javascript/main.js'
    elif src == 'loader':
        tpl = 'javascript/loader.js'
        
    return render(request, tpl)
