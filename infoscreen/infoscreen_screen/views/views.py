# System includes


# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render


def index(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/index.html", ctx)
    

def news(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/news.html", ctx)


def willkommen(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/willkommen.html", ctx)
    
    
def karte(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/karte.html", ctx)


def alarm(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/alarm.html", ctx)
