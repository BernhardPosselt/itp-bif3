# System includes

# Django includes
from django.shortcuts import render
from django.conf import settings

# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.config import WebsiteConfig

def gmap(request, id):
    """
    Doku
    """
    config = WebsiteConfig(settings.WEBSITE_CFG)
   
    ctx = {
        'id': id,
        'key': config.gmap_key
    }
    return render(request, "infoscreen_screen/gmap/gmap.html", ctx)


def gmap_adresse(request, id):
    """Generates the javascript from templates

    Keyword arguments:
    src -- The javascript part which should be generated 
    """
    einsatz = Einsaetze.objects.get(id=id)
    
   
    tpl = 'javascript/gmaps.js'
    config = WebsiteConfig(settings.WEBSITE_CFG)
    
    ctx = {
        'plz': str(einsatz.plz),
        'ort': str(einsatz.ort),
        'strasse': str(einsatz.strasse),
        'hausnummer': str(einsatz.nummer1),
        'kml_url': config.kml_url
    }
    return render(request, tpl,ctx)
