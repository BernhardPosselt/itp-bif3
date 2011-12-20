# System includes
from time import mktime

# Django includes
from django.conf import settings

# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render
from infoscreen.inc.config import WebsiteConfig


def update(request, screen):
    """
    This function queries, of elements in the datagbase have been updated or
    deleted/added. If so the request will see it and can update the according 
    element of the page
    
    Keyword arguments
    request -- The request object
    screen -- which page we're on, 0 for left screen, 1 for right screen
    """
    # FIXME: performance and working updates!!!
    
    config = WebsiteConfig(settings.WEBSITE_CFG)
    update_interval = config.update_interval
    willkommen =  config.welcome_msg
    
    # set default values
    news_len = 0
    geraet_len = 0
    fahrzeug_len = 0
    ausrueckordnung_len = 0
    dispo_len = 0
    letze_aenderung = []
    anzahl = []
    
    # check if we got frieden or einsatz
    einsatz = Einsaetze.objects.filter(abgeschlossen=False).order_by('-modifiziert')
    einsatz_len = len(einsatz)
    if einsatz_len == 0:
        frieden = True
    else:
        frieden = False
        letze_aenderung.append(int(mktime(einsatz[0].modifiziert.timetuple())))

    # depending on frieden or einsatz we query the database    
    if frieden:
    
        if screen == 0:
            pass
                            
        elif screen == 1:
            news = News.objects.all().order_by('-modifiziert')  
            fahrzeug = Fahrzeuge.objects.all().order_by('-modifiziert')
            geraet = Geraete.objects.filter(reperatur=True).order_by('-modifiziert')
            # FIXME: len of 0 elements returns none apparently
            # get nr of elements
            news_len = len(news)
            geraet_len = len(geraet)
            fahrzeug_len = len(fahrzeug)
            anzahl.append(einsatz_len)
            anzahl.append(ausrueckordnung_len)
            anzahl.append(fahrzeug_len)
            # check if we have to push a lastchange
            if news_len != 0:
                letze_aenderung.append(int(mktime(news[0].modifiziert.timetuple())))
            else:
                letze_aenderung.append(0)
            if geraet_len != 0:
                letze_aenderung.append(int(mktime(geraet[0].modifiziert.timetuple())))
            else:
                letze_aenderung.append(0)
            if fahrzeug_len != 0:
                letze_aenderung.append(int(mktime(fahrzeug[0].modifiziert.timetuple())))
            else:
                letze_aenderung.append(0)
            
    else:

        if screen == 0:
            ausrueckordnung = Ausrueckordnungen.objects.all().order_by('-modifiziert')
            fahrzeug = Fahrzeuge.objects.all().order_by('-modifiziert')
            # get nr of elements
            ausrueckordnung_len = len(ausrueckordnung)
            anzahl.append(news_len)
            anzahl.append(geraet_len)
            anzahl.append(fahrzeug_len)
            # check if we have to push a lastchange
            if ausrueckordnung_len != 0:
                letze_aenderung.append(int(mktime(ausrueckordnung[0].modifiziert.timetuple())))
            else:
                letze_aenderung.append(0)
            
        elif screen == 1:
            dispo = Dispos.objects.all().order_by('-modifiziert')
            # get nr of elements      
            dispo_len = len(dispo) 
            anzahl.append(dispo_len)
            anzahl.append(einsatz_len)
            # check if we have to push a lastchange
            if dispo_len != 0:
                letze_aenderung.append(int(mktime(fahrzeug[0].modifiziert.timetuple())))
            else:
                letze_aenderung.append(0)
    
    ctx = {
        'letze_aenderung': letze_aenderung,
        'anzahl': anzahl,
        'update_interval': update_interval,
        'einsatz': not frieden,
        'willkommen': willkommen
    }
    return render(request, "infoscreen_screen/ajax/update.json", ctx)

    
def reload_data(request):
    """
    Doku
    """
    div = request.GET.get(id, '')
    # TODO: write reloads
    ctx = {}
    return render(request, "infoscreen_screen/ajax/update_einsatz.json", ctx)

