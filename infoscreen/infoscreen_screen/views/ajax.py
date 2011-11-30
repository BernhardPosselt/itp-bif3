# System includes


# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render


def update(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/ajax/update.json", ctx)

    
def update_einsatz(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/ajax/update_einsatz.json", ctx)


def update_news(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/ajax/update_news.json", ctx)
    
    
def update_willkommen(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/ajax/update_willkommen.json", ctx)


def update_karte(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/ajax/update_karte.json", ctx)
