"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
from lxml import etree
from infoscreen.infoscreen_screen.parser import *
from infoscreen.infoscreen_screen.models import Einsaetze as EinsatzModel
from infoscreen.infoscreen_screen.models import Meldebilder as MeldebildModel
from infoscreen.infoscreen_screen.models import Alarmstufen as AlarmModel
from datetime import *
import re
import gtk.gdk




class Testparser(unittest.TestCase):
    def test_tags(self):
        """
        Der Parser wird überprüft
        """
        createdb = DBCREATE()
        createdb.create_database()
        
        testxml = XML("tests/xml/dummy.xml")
        testxml = XML("tests/xml/dummy1.xml")
        testxml = XML("tests/xml/einsatz.xml")
        testxml = XML("tests/xml/eldisdata.xml")
        testeintrag = EinsatzModel.objects.all()
        for eins in testeintrag:
            print eins.einsatznr
    
class DBCREATE(object):
    def create_database(self):
        """
        Die Testdatenbank wird mit Testdaten befüllt
        """
        alarmstufen = ["B1","B2","B3","B4","T1","T2","T3","S1","S2","S3"]
        MeldB1 = ["Autobahn - Fahrzeugbrand", "Bahndammbrand", "Brandverdacht",
        "Flurbrand", "Kaminbrand", "Kleinbrand", "Muellbehaelterbrand", "TUS- od. Infranet-Alarm",
        "Ueberhitzter Ofen"]
        MeldB2 = ["Fahrzeugbrand", "Kellerbrand", "Kuechenbrand", "Trafobrand", "Waldbrand",
        "Wohnungsbrand", "Zimmerbrand"]
        MeldB3 = ["Brand in kl. Gewerbebetrieb", "Dachstuhlbrand", "Geschaeftsbrand", 
        "Gewerbebetrieb-klein", "Scheunen- od. Schuppenbrand", "Wohnhausbrand"]
        MeldB4 = ["Gewerbebetrieb- gross", "Industrieobjekt", "Landw. Objekt"]
        MeldS1 = ["Autobahn - Oelspur", "Benzin- bzw. Oelspur",
        "Benzin- bzw. Oelspur beseitigen", "Gasaustritt bzw. -gebrechen"]
        MeldS2 = ["Autobahn - Schadstoffeinsatz", "Chlorgasaustritt", "Kl. Gewaesserschaden",
        "Oeltreiben", "Oertl. Chemieunfall"]
        MeldS3 = ["Chemieunfall m. groesseren Umweltschaeden", "Tankwagenunfall"]
        MeldT1 = ["Auspumparbeiten", "Autobahn - Bergung", "Bootsbergung", "Eisstoss",
        "Fahrzeugbergung", "Hochwasser", "LKW-Bergung", "Motorradbergung", "Person(en) in Aufzug",
        "Personensuche", "Sturmschaden", "Taucheinsatz", "Technische Hilfeleistung", "Tierrettung",
        "Tueroeffnung", "Unwettereinsatz", "Verkehrsunfall", "Wassergebrechen", "Wasserversorgung"]
        MeldT2 = ["Autobahn - Menschenrettung", "Menschenrettung (1 eingekl. Person)", "Person in Notlage",
        "VU mit 1 eingekl. Person"]
        MeldT3 = ["Autobahn - Schwere Bergung", "Autobusunfall", "Eisenbahnunglueck", "Menschenrettung (mehrere eingekl. Personen)",
        "Schiffsunglueck", "VU mit mehreren eingekl. Personen"]
        
        
        for attr in alarmstufen:
            alarm = AlarmModel()
            alarm.stufe = attr
            alarm.save()
        
        for attr in MeldB1:
            mbild = MeldebildModel()
            mbild.beschreibung = attr
            alarm_stufe = AlarmModel.objects.get(stufe = "B1")
            mbild.stufe = alarm_stufe
            mbild.save()
        
        for attr in MeldB2:
            mbild = MeldebildModel()
            mbild.beschreibung = attr
            alarm_stufe = AlarmModel.objects.get(stufe = "B2")
            mbild.stufe = alarm_stufe
            mbild.save()
        
        for attr in MeldB3:
            mbild = MeldebildModel()
            mbild.beschreibung = attr
            alarm_stufe = AlarmModel.objects.get(stufe = "B3")
            mbild.stufe = alarm_stufe
            mbild.save()
            
        for attr in MeldB4:
            mbild = MeldebildModel()
            mbild.beschreibung = attr
            alarm_stufe = AlarmModel.objects.get(stufe = "B4")
            mbild.stufe = alarm_stufe
            mbild.save()
            
        for attr in MeldS1:
            mbild = MeldebildModel()
            mbild.beschreibung = attr
            alarm_stufe = AlarmModel.objects.get(stufe = "S1")
            mbild.stufe = alarm_stufe
            mbild.save()
            
        for attr in MeldS2:
            mbild = MeldebildModel()
            mbild.beschreibung = attr
            alarm_stufe = AlarmModel.objects.get(stufe = "S2")
            mbild.stufe = alarm_stufe
            mbild.save()
            
        for attr in MeldS3:
            mbild = MeldebildModel()
            mbild.beschreibung = attr
            alarm_stufe = AlarmModel.objects.get(stufe = "S3")
            mbild.stufe = alarm_stufe
            mbild.save()
            
        for attr in MeldT1:
            mbild = MeldebildModel()
            mbild.beschreibung = attr
            alarm_stufe = AlarmModel.objects.get(stufe = "T1")
            mbild.stufe = alarm_stufe
            mbild.save()
            
        for attr in MeldT2:
            mbild = MeldebildModel()
            mbild.beschreibung = attr
            alarm_stufe = AlarmModel.objects.get(stufe = "T2")
            mbild.stufe = alarm_stufe
            mbild.save()
        
        for attr in MeldT3:
            mbild = MeldebildModel()
            mbild.beschreibung = attr
            alarm_stufe = AlarmModel.objects.get(stufe = "T3")
            mbild.stufe = alarm_stufe
            mbild.save()
    
        
class Testdb(unittest.TestCase):
    def test_db(self):
        """
        Funktion der Datenbankmodels und deren Beziehungen wird überprüft
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
        einsatz.einsatz = 1
        einsatz.bemerkung = "test"
        einsatz.einsatznr = 129
        einsatz.ort = "Bernhardsthal"
        einsatz.plz = 2275
        einsatz.einsatzerzeugt = datetime.now()
        meldebild_beschreibung = MeldebildModel.objects.get(beschreibung = "Kaminbrand")
        einsatz.meldebild = meldebild_beschreibung
        einsatz.abgeschlossen = False
        
        einsatz.save()
        
        unabgeschl = EinsatzModel.objects.filter(abgeschlossen = False)
        for unab in test:
            print unab.einsatz
        
class Testdates(unittest.TestCase):
    def test_dates(self):
        """
        Erstellen der Timestamps wird getestet
        """
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

class Testscreenshot(unittest.TestCase):
    def test_sshot(self):
        """
        Screenshot unter Linux 
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
