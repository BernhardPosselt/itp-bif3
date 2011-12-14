# System includes


# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from gmapi import maps
from gmapi.maps import Geocoder
from lxml import etree
from infoscreen.infoscreen_screen.parser import *

def index(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/index.html", ctx)
    

def bildschirm_links(request):
    """
    Doku
    """
    testxml = XML("tests/xml/dummy.xml")
    testxml.save()
    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_links.html", ctx)


def bildschirm_rechts(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_rechts.html", ctx)
   
   
    
