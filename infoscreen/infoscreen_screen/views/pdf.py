# System includes


# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render


def einsatzfax(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/pdf/einsatzfax.json", ctx)
    

def einsatzfax_pdf(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/pdf/einsatzfax_pdf.html", ctx)
    
    
def einsatzfax_pdf_printed(request, id):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/pdf/einsatzfax_pdf_printed.html", ctx)
