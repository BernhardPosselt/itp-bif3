# System includes

# Django includes
from django.shortcuts import render

# Project includes
from infoscreen.infoscreen_screen.models import *

def gmap(request, id):
    """
    Doku
    """
    ctx = {
        'id': id
    }
    return render(request, "infoscreen_screen/gmap/gmap.html", ctx)


def gmap_adresse(request, id):
    """Generates the javascript from templates

    Keyword arguments:
    src -- The javascript part which should be generated 
    """
    einsatz = Einsaetze.objects.get(id=id)
    
   
    tpl = 'javascript/gmaps.js'
    
    ctx = {
        'plz': str(einsatz.plz),
        'ort': str(einsatz.ort),
        'strasse': str(einsatz.strasse),
        'hausnummer': str(einsatz.nummer1)
    }
    return render(request, tpl,ctx)
