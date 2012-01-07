#!/usr/bin/env python
#-*- coding:utf-8 -*-


# Django imports
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper
from django.template import RequestContext

# Project imports
from infoscreen.infoscreen_screen.models import Einsaetze

"""Keep your usefull tools here
"""
def is_mission():
    """Returns the numbers of running missions, otherwise false
    """
    # check if we got frieden or einsatz
    missions = Einsaetze.objects.filter(abgeschlossen=False).aggregate( Count('id') )
    running_missions = Einsaetze.objects.filter(abgeschlossen=False)
    missions_len = missions['id__count']
    if missions_len == 0:
        return False
    else:
        return missions_len
 

def render(request, tpl, tplvars={}):
    """Shortcut for renewing csrf cookie and passing request context
    
    Keyword arguments:
    tpl -- the template we want to use
    args -- the template variables

    """
    tplvars.update(csrf(request))
    # pass config vars
    # tplvars["config"] = "hi"
    return render_to_response(tpl, tplvars,
                               context_instance=RequestContext(request))


def send_file(request, path):
    """                                                                         
    Send a file    
    
    Keyword arguments:
    download -- the path to the file
                                              
    """
    filename = os.path.basename(path).replace(" ", "_")                            
    wrapper = FileWrapper(file(path))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Disposition'] = u'attachment; filename=%s' % filename
    response['Content-Length'] = os.path.getsize(path)
    return response
