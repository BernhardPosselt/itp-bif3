# System includes
from time import mktime
import datetime

# Django includes
from django.conf import settings
from django.db.models import Max, Count

# Project includes
from infoscreen.infoscreen_screen.models import *
from django.shortcuts import render, get_object_or_404
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
    
    # set default values
    mission = False
    last_change = []
    count = []
    
    # check if we got frieden or einsatz
    missions = Einsaetze.objects.filter(abgeschlossen=False).aggregate( Count('id'), Max('modifiziert') )
    missions_len = mission['id__count']
    missions_change = mission['modifiziert__max']
    if missions_len == 0:
        mission = True
    
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
        'einsatz': not frieden
    }
    return render(request, "infoscreen_screen/ajax/update.json", ctx)


#-------------------------------------------------------------------------------
# Update requests
#-------------------------------------------------------------------------------
def update_welcome(request):
    """Returns json with the welcome msg
    """
    config = WebsiteConfig(settings.WEBSITE_CFG)
    ctx = {
        'welcome_msg': config.welcome_msg
    }
    return render(request, "infoscreen_screen/ajax/update_welcome.json", ctx)


def update_news(request):
    """Returns html with all news
    """
    news = News.objects.filter(datum__gte=datetime.datetime.now())
    ctx = {
        'news': news
    }
    return render(request, "infoscreen_screen/ajax/update_news.html", ctx)
    
    
def update_vehicles(request):
    """Returns html with all broken vehicles
    """
    vehicles = Fahrzeuge.objects.filter(reperatur=True)
    ctx = {
        'vehicles': vehicles
    }
    return render(request, "infoscreen_screen/ajax/update_vehicles.json", ctx)
    
    
def update_utils(request):
    """Returns html with all broken utils
    """
    utils = Geraete.objects.filter(reperatur=True)
    ctx = {
        'utils': utils
    }
    return render(request, "infoscreen_screen/ajax/update_utils.json", ctx)
    

def update_vehicle_order(request, missionid):
    """Returns html for the mission with the vehicle order
    
    Keyword arguments:
    missionid -- The id of the mission
    """
    mission = get_object_or_404(Einsaetze, id=missionid)
    vehicle_order = mission.meldebild.ausrueckordnungen_set.all()
    ctx = {
        'vehicle_order': vehicle_order
    }
    return render(request, "infoscreen_screen/ajax/update_vehicle_order.html", ctx)


def update_mission(request, missionid):
    """Returns json for the mission
    
    Keyword arguments:
    missionid -- The id of the mission
    """
    mission = get_object_or_404(Einsaetze, id=missionid)
    ctx = {
        'mission': mission
    }
    return render(request, "infoscreen_screen/ajax/update_mission.json", ctx)

   
def running_missions(request):
    """Returns json with ids of all running missions
    
    Keyword arguments:
    missionid -- The id of the mission
    """
    missions = Einsaetze.objects.filter(abgeschlossen=False)
    ctx = {
        'missions': missions
    }
    return render(request, "infoscreen_screen/ajax/running_mission.json", ctx)
