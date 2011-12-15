# System includes
from time import mktime

# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render


def update(request):
    """
    Doku
    """
    news = News.objects.all().order_by('-modifiziert')
    einsatz = Einsaetze.objects.filter(abgeschlossen=False).order_by('-modifiziert')
    dispo = Dispos.objects.all().order_by('-modifiziert')
    fahrzeug = Fahrzeuge.objects.all().order_by('-modifiziert')
    geraet = Geraete.objects.filter(reperatur=True).order_by('-modifiziert')
    ausrueckordnung = Ausrueckordnungen.objects.all().order_by('-modifiziert')
    
    # get the nr of elements on each page and the last modified element
    frieden_rechts_anzahl = [len(news), len(geraet), len(fahrzeug)]
    frieden_rechts_last = [
            int(mktime(news[:1].modifiziert.timetuple()),
            int(mktime(geraet[:1].modifiziert.timetuple()),
            int(mktime(fahrzeug[:1].modifiziert.timetuple())
        ].sort()[-1] 
    einsatz_links_anzahl = [len(einsatz), len(ausrueckordnung), len(fahrzeug)]
    einsatz_links_last = 
        [
            int(mktime(einsatz[:1].modifiziert.timetuple()),
            int(mktime(ausrueckordnung[:1].modifiziert.timetuple()),
            int(mktime(fahrzeug[:1].modifiziert.timetuple())
        ].sort()[-1] 
    einsatz_rechts_anzahl = [len(dispo), len(einsatz)]
    einsatz_rechts_last = [
            int(mktime(dispo[:1].modifiziert.timetuple()),
            int(mktime(einsatz[:1].modifiziert.timetuple())
        ].sort()[-1] 
    ctx = {
        'frieden_rechts_last': frieden_rechts_last,
        'einsatz_links_last': einsatz_links_last,
        'einsatz_rechts_last': einsatz_rechts_last,
        # nr of elems
        'frieden_rechts_anzahl': frieden_rechts_anzahl,
        'einsatz_links_anzahl': einsatz_links_anzahl,
        'einsatz_rechts_anzahl': einsatz_rechts_anzahl
    }
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
