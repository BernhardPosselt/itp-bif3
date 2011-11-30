# System includes


# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from infoscreen.infoscreen_screen.forms import MapForm




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
    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_links.html", ctx)


def bildschirm_rechts(request):
    """
    Doku
    """
    gmap = maps.Map(opts = {
<<<<<<< HEAD
         'center': maps.LatLng(38, -97),
         'mapTypeId': maps.MapTypeId.ROADMAP,
         'zoom': 3,
         'mapTypeControlOptions': {
              'style': maps.MapTypeControlStyle.DROPDOWN_MENU
         },
=======
        'center': maps.LatLng(38, -97),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 3,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
>>>>>>> 050c4f9bee72794c457b55e020c652ff4b3cab38
    })

    ctx = {'form': MapForm(initial={'map': gmap})}

    return render(request, "infoscreen_screen/bildschirm_rechts.html", ctx)
    
