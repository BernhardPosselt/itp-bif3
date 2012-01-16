#!/usr/bin/env python
#-*- coding:utf-8 -*-

# System includes
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Frame, Paragraph
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor

# Django includes
from django.http import HttpResponse
from django.shortcuts import render

# Project includes
from infoscreen.infoscreen_screen.models import *


def einsatzfax(request):
    """
    Returns an xml with all einsaetze which were not printed yet
    
    Keyword arguments:
    
    id -- The id (databaseid, not einsatzID) of the einsatz 
    """
    pdfs = Einsaetze.objects.filter(ausgedruckt=False)
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
        einsatz = Einsaetze.objects.get(id=id)
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=einsatzfax.pdf' 

        # Create the PDF object, using the response object as its "file" in DIN A4 format
        p = canvas.Canvas(response,pagesize=A4)

	# A4 width and height
	breite, hoehe = A4
	# Define the styles
	styleHeader = ParagraphStyle('Header', fontName='Helvetica', fontSize=36, leading=40, spaceAfter=40, alignment=TA_LEFT)
	styleText = ParagraphStyle('Text', fontName='Helvetica', fontSize=16, leading=20, alignment=TA_LEFT)
	styleLine = ParagraphStyle('Line', fontName='Helvetica', fontSize=16, leading=20, alignment=TA_LEFT, textColor=HexColor(0xFFFFFF))
	# Creating a list, which contains the content
	content = []
	# Create the frame where the content will be placed
	f = Frame(1*cm,1*cm,breite-(2*cm),hoehe-(2*cm))

	# Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        
	# Generate content
        meldeb = Meldebilder.objects.get(id = einsatz.meldebild_id)
        alarm = Alarmstufen.objects.get(stufe = meldeb.stufe_id)
	content.append(Paragraph(alarm.stufe + " " + meldeb.beschreibung, styleHeader))
	content.append(Paragraph(einsatz.strasse + " " + einsatz.nummer1 + " " + einsatz.nummer2 + " " + einsatz.nummer3, styleText))
	content.append(Paragraph(str(einsatz.plz) + " " + einsatz.ort, styleText))
	content.append(Paragraph("a", styleLine))
	if einsatz.objekt:
		content.append(Paragraph("Objekt: " + einsatz.objekt, styleText))
	if einsatz.melder:
		content.append(Paragraph("Melder: " + einsatz.melder, styleText))
	if einsatz.meldertel:
		content.append(Paragraph("Meldertelefon: " + einsatz.meldertel, styleText))
	if einsatz.einsatzerzeugt:
		content.append(Paragraph("Meldezeitpunkt: " + str(einsatz.einsatzerzeugt), styleText))
	content.append(Paragraph("a", styleLine))
	content.append(Paragraph(einsatz.bemerkung, styleText))

	# Add content
	f.addFromList(content,p)

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response
    except Einsaetze.DoesNotExist:
        return render(request, "infoscreen_screen/einsatzfax/einsatzfax_pdf.xml", ctx)
    
    
def einsatzfax_pdf_ausgedruckt(request, id):
    """
    Sets an einsatz to ausgedruckt
    
    Keyword arguments:
    
    id -- The id (databaseid, not einsatzID) of the einsatz 
    """
    try:
        einsatz = Einsaetze.objects.get(id=id)
        einsatz.ausgedruckt = True
        einsatz.save()
        ok = True
    except Einsaetze.DoesNotExist:
        ok = False
    ctx = {
        "ok": ok,
    }
    return render(request, "infoscreen_screen/einsatzfax/einsatzfax_pdf_ausgedruckt.xml", ctx)
