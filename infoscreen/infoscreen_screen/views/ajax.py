# System includes
from time import mktime
import datetime

# Django includes
from django.conf import settings
from django.db.models import Count

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
    running_missions = Einsaetze.objects.filter(abgeschlossen=False)
    missions_len = missions['id__count']
    if missions_len == 0:
        mission = False
    else:
        mission = True
    
    ctx = {
        'update_interval': update_interval,
        'mission': mission,
        'running_missions': running_missions,
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
    preview = request.POST.get('preview', '')
    if preview != '':
        news = News.objects.all().order_by('-datum')[:5]
    else:
        news = News.objects.filter(released=True).order_by('-datum')[:5]
    
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
    return render(request, "infoscreen_screen/ajax/update_vehicles.html", ctx)
    
    
def update_utils(request):
    """Returns html with all broken utils
    """
    utils = Geraete.objects.filter(reperatur=True)
    ctx = {
        'utils': utils
    }
    return render(request, "infoscreen_screen/ajax/update_utils.html", ctx)
    

def update_vehicle_order(request):
    """Returns html for the mission with the vehicle order
    """
    mission_id = int(request.POST.get('mission_id', 0))
    if mission_id == 0:
        mission_id = int(request.GET.get('mission_id', 0))
    mission = get_object_or_404(Einsaetze, id=mission_id)
    vehicle_order = mission.meldebild.ausrueckordnungen_set.all()
    ctx = {
        'vehicle_order': vehicle_order
    }
    return render(request, "infoscreen_screen/ajax/update_vehicle_order.html", ctx)


def update_mission(request):
    """Returns json for the mission
    """
    mission_id = int(request.POST.get('mission_id', 0))
    if mission_id == 0:
        mission_id = int(request.GET.get('mission_id', 0))
    mission = get_object_or_404(Einsaetze, id=mission_id)
    ctx = {
        'mission': mission
    }
    return render(request, "infoscreen_screen/ajax/update_mission.json", ctx)


def update_dispos(request):
    """Returns html for the dispos
    """
    mission_id = int(request.POST.get('mission_id', 0))
    if mission_id == 0:
        mission_id = int(request.GET.get('mission_id', 0))
    mission = get_object_or_404(Einsaetze, id=mission_id)
    dispos = mission.dispos_set.all()
    ctx = {
        'dispos': dispos
    }
    return render(request, "infoscreen_screen/ajax/update_dispos.html", ctx)

