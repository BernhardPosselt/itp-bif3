# Create your views here.


# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render


def index(request):
    """
    Main page
    """
    einsatz = Einsatz.objects.all()
    return render(request, "infoscreen_screen/index.html", {"test": einsatz })
