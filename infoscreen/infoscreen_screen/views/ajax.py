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


def update(request):
    """
    This function queries, of elements in the datagbase have been updated or
    deleted/added. If so the request will see it and can update the according 
    element of the page
    """
    
    config = WebsiteConfig(settings.WEBSITE_CFG)
    update_interval = config.update_interval
    
    # check if we got frieden or einsatz
    missions = Einsaetze.objects.filter(abgeschlossen=False).aggregate( Count('id') )
    missions_len = mission['id__count']
    if missions_len == 0:
        mission = False
    else:
        mission = True
    
    ctx = {
        'update_interval': update_interval,
        'mission': mission
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
    

def update_vehicle_order(request):
    """Returns html for the mission with the vehicle order
    
    Keyword arguments:
    missionid -- The id of the mission
    """
    missionid = request.GET.get('missionid', '')
    mission = get_object_or_404(Einsaetze, id=missionid)
    vehicle_order = mission.meldebild.ausrueckordnungen_set.all()
    ctx = {
        'vehicle_order': vehicle_order
    }
    return render(request, "infoscreen_screen/ajax/update_vehicle_order.html", ctx)


def update_mission(request):
    """Returns json for the mission
    
    Keyword arguments:
    missionid -- The id of the mission
    """
    missionid = request.GET.get('missionid', '')
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
