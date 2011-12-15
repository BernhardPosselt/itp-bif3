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
