# System includes

# Django includes

# Project includes
from infoscreen.inc.shortcuts import render

def gmap(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/gmap/gmap.html", ctx)
