"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
from lxml import etree
from infoscreen.infoscreen_screen.parser import *
from infoscreen.infoscreen_screen.models import Einsatz as EinsatzModel
from infoscreen.infoscreen_screen.models import Meldebilder as MeldebildModel
from infoscreen.infoscreen_screen.models import Alarmstufen as AlarmModel
from datetime import *
import re
import gtk.gdk


class Testscreenshot(unittest.TestCase):
    def test_sshot(self):
        """
        Screenshottest
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

class Testparser(unittest.TestCase):
    def test_tags(self):
        """
        Einlesen mit Parser
        """
        alarm = AlarmModel()
        alarm.stufe = "B3"
        alarm.save()
        
        alarm = AlarmModel()
        alarm.stufe = "T1"
        alarm.save()
        
        mbild = MeldebildModel()
        mbild.beschreibung = "Wohnhausbrand"
        alarm_stufe = AlarmModel.objects.get(stufe = "B3")
        mbild.stufe = alarm_stufe
        mbild.save()
        
        mbild = MeldebildModel()
        mbild.beschreibung = "Auspumparbeiten"
        alarm_stufe = AlarmModel.objects.get(stufe = "T1")
        mbild.stufe = alarm_stufe
        mbild.save()
        
        testxml = XML("tests/xml/dummy1.xml")
        testeintrag = EinsatzModel.objects.all()
        print testeintrag[0].einsatznr
        
class Testdb(unittest.TestCase):
    def test_db(self):
        """
        Eintragen in die Einsatztabelle"
        """
        alarm = AlarmModel()
        alarm.stufe = "B1"
        alarm.save()
        
        mbild = MeldebildModel()
        mbild.beschreibung = "Kaminbrand"
        alarm_stufe = AlarmModel.objects.get(stufe = "B1")
        mbild.stufe = alarm_stufe
        mbild.save()
        
        einsatz = EinsatzModel()
        einsatz.einsatzid = 1
        einsatz.bemerkung = "test"
        einsatz.einsatznummer = 129
        einsatz.ort = "Bernhardsthal"
        einsatz.plz = 2275
        einsatz.erzeugt = datetime.now()
        meldebild_beschreibung = MeldebildModel.objects.get(beschreibung = "Kaminbrand")
        einsatz.meldebild = meldebild_beschreibung
        
        einsatz.save()
        
        testeintrag = EinsatzModel.objects.all()
        print testeintrag[0].meldebild
        
class Testdates(unittest.TestCase):
    def test_dates(self):
        datumeinsatz = "25.04.2008 18:56:58"
        hilf = re.split('\.+|\:+|\ +',datumeinsatz,5)
        datal = date(int(hilf[2]),int(hilf[1]),int(hilf[0]))
        try:
            if hilf[3]:
                zeital = time(int(hilf[3]),int(hilf[4]),int(hilf[5]))
                
        except:
            zeital = time(0,0,0)
        ollas = datetime.combine(datal,zeital)  
        print ollas
