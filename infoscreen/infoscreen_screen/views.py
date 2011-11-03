# System includes


# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render


def index(request):
    """
    Main page
    """
    einsatz = Einsatz.objects.all()
    # debug your code like this, prints the string in the console
    print "hey hier is n fehler %s" % einsatz[0].einsatzID
    return render(request, "infoscreen_screen/index.html", {"test": einsatz })
