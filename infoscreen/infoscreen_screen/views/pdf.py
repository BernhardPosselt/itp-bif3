# System includes
from reportlab.pdfgen import canvas

# Django includes
from django.http import HttpResponse

# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render


def einsatzfax(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/einsatzfax/einsatzfax.json", ctx)
    

def einsatzfax_pdf(request):
    """
    Doku
    """
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
    
    
def einsatzfax_pdf_printed(request, id):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/einsatzfax/einsatzfax_pdf_printed.html", ctx)
