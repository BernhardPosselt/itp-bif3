# System includes
from reportlab.pdfgen import canvas

# Django includes
from django.http import HttpResponse

# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render


def einsatzfax(request):
    """
    Returns an xml with all einsaetze which were not printed yet
    
    Keyword arguments:
    
    id -- The id (databaseid, not einsatzID) of the einsatz 
    """
    pdfs = Einsatz.objects.filter(ausgedruckt=False)
    ctx = {
        "einsaetze": pdfs,
    }
    return render(request, "infoscreen_screen/einsatzfax/einsatzfax.xml", ctx)


def einsatzfax_pdf(request, id):
    """
    Creates a pdf of an einsatz ready for printing
    """
    try:
        # TODO: create pdf from Einsatz
        einsatz = Einsatz.objects.get(id=id)
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 100, "Hello world.")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response
    except Einsatz.DoesNotExist:
        return render(request, "infoscreen_screen/einsatzfax/einsatzfax_pdf.xml", ctx)
    
    
def einsatzfax_pdf_ausgedruckt(request, id):
    """
    Sets an einsatz to ausgedruckt
    
    Keyword arguments:
    
    id -- The id (databaseid, not einsatzID) of the einsatz 
    """
    try:
        einsatz = Einsatz.objects.get(id=id)
        einsatz.ausgedruckt = True
        einsatz.save()
        ok = True
    except Einsatz.DoesNotExist:
        ok = False
    ctx = {
        "ok": ok,
    }
    return render(request, "infoscreen_screen/einsatzfax/einsatzfax_pdf_ausgedruckt.xml", ctx)
