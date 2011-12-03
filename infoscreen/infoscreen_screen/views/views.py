# System includes


# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from infoscreen.infoscreen_screen.forms import MapForm
from gmapi import maps
from gmapi.maps import Geocoder

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
   
    geocoder = Geocoder()
   
    einsatzort = "10,Mitterweg,3502,Krems"
    results, status_code = geocoder.geocode({'address': einsatzort})
    result = results[0]
    lat, lng = result['geometry']['location']['arg']

    gmap = maps.Map(opts = {
         'center': maps.LatLng(lat, lng),
         'mapTypeId': maps.MapTypeId.ROADMAP,
         'zoom': 16,
         'size': maps.Size(1100,750),
         'mapTypeControlOptions': {
              'style': maps.MapTypeControlStyle.DEFAULT
         },
         'navigationControlStyle': {
            'style': maps.NavigationControlStyle.DEFAULT
         },
        
    })
    k = maps.Marker()
    k.setPosition(maps.LatLng(lat, lng))
    k.setMap(gmap)
    ctx = {'form': MapForm(initial={'map': gmap})}

    return render(request, "infoscreen_screen/bildschirm_rechts.html", ctx)
    
