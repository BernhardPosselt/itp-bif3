# System includes


# Django includes


# Project includes
from infoscreen.infoscreen_screen.models import *
from infoscreen.inc.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from gmapi import maps
from gmapi.maps import Geocoder
from lxml import etree
from infoscreen.infoscreen_screen.parser import *
import gtk.gdk

def index(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/index.html", ctx)


def settings(request):
    """
    Doku
    """
    ctx = {}
    return render(request, "infoscreen_screen/index.html", ctx)

def bildschirm_links(request):
    """
    Doku
    """
    testxml = XML("tests/xml/eldisdata.xml")
    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_links.html", ctx)


def bildschirm_rechts(request):
    """
    Doku
    """
    
  
    # Calculate the size of the whole screen
    screenw = gtk.gdk.screen_width()
    screenh = gtk.gdk.screen_height()

    # Get the root and active window
    root = gtk.gdk.screen_get_default()

    if root.supports_net_wm_hint("_NET_ACTIVE_WINDOW") and root.supports_net_wm_hint("_NET_WM_WINDOW_TYPE"):
        active = root.get_active_window()
        # You definately do not want to take a screenshot of the whole desktop, see entry 23.36 for that
        # Returns something like ('ATOM', 32, ['_NET_WM_WINDOW_TYPE_DESKTOP'])
        if active.property_get("_NET_WM_WINDOW_TYPE")[-1][0] == '_NET_WM_WINDOW_TYPE_DESKTOP' :
            print False

        # Calculate the size of the wm decorations
        relativex, relativey, winw, winh, d = active.get_geometry()
        w = winw + (relativex*2)
        h = winh + (relativey+relativex)

        # Calculate the position of where the wm decorations start (not the window itself)
        screenposx, screenposy = active.get_root_origin()
    else:
        print False

    screenshot = gtk.gdk.Pixbuf.get_from_drawable(gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, w, h),
        gtk.gdk.get_default_root_window(),
        gtk.gdk.colormap_get_system(),
        screenposx, screenposy, 0, 0, w, h)

    # Either "png" or "jpeg" (case matters)
    format = "png"

    # Pixbuf's have a save method
    # Note that png doesnt support the quality argument.
    screenshot.save("screenshot." + format, format)

    ctx = {}
    return render(request, "infoscreen_screen/bildschirm_rechts.html", ctx)
   
   
def javascript(request, src):
    """Generates the javascript from templates

    Keyword arguments:
    src -- The javascript part which should be generated 
    """
    if src == 'main':
        tpl = 'javascript/main.js'
    elif src == 'loader':
        tpl = 'javascript/loader.js'
        
    return render(request, tpl)
