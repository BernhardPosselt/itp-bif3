#!/usr/bin/env python
#-*- coding:utf-8 -*-

from lxml import etree
from infoscreen.infoscreen_screen.models import Einsaetze as EinsatzModel
from datetime import *
import re
from infoscreen.infoscreen_screen.models import Meldebilder as MeldebildModel
from infoscreen.infoscreen_screen.models import Dispos as DispoModel


class EinsatzKlasse(object):
    """
    Diese Klasse dient dazu die geparsten Einsätze zu 
    überprüfen und in die Db zu speichern
    """
    def __init__(self):
        
        #Hier werden die Default-Werte gesetzt
        datal  = date(2001,01,01)
        zeital = time(0,0,0)
        tstamp = datetime.combine(datal,zeital)
        self.einsatz = 0
        self.alarmstufe = ""
        self.meldebild= ""
        self.nummer1 = ""
        self.nummer2 = ""
        self.nummer3 = ""
        self.plz= 0
        self.strasse = ""
        self.ort = ""
        self.bemerkung = ""
        self.objekt = ""
        self.melder = ""
        self.einsatznr = 0
        self.einsatzerzeugt = tstamp
        self.abgeschlossen = False
        self.ausgedruckt = False 
      
    
    
    def getModel(self):
        """
        Diese Methode prüft ob bereits ein Einsatz mit dieser ID existiert
        Wenn ja: wird dieser zurückgegeben (update)
        Wenn nein: wird False zurückgegeben und ein neuer Einsatz  (insert)
        """
        try:
            einsatzmod = EinsatzModel.objects.get(einsatz=self.einsatz)
            return einsatzmod
        except EinsatzModel.DoesNotExist:
            return False

    def save(self):
        """
        Speichert die Einträge des Objekts in die Datenbank
        """
        
        # get the database model of the einsatz
        
        einsatzmod = self.getModel()
        if not einsatzmod:
            einsatzmod = EinsatzModel()
            
        #Alle möglichen Attribute werden durchgegangen
        einsatztags = [ "einsatz", "alarmstufe", "meldebild", "nummer1", "nummer2",
            "nummer3", "plz", "strasse", "objekt","ort", "bemerkung", "einsatzerzeugt", 
            "melder", "meldertel", "einsatznr", "abgeschlossen", "ausgedruckt"] 
        try:
            for attr in einsatztags:
                if attr == "meldebild":
                    # Meldebild wird dem Datebankobjekt zugewiesen, gibt es kein Meldebild wird dies in der DB vermerkt
                    try:
                        meldebild_beschreibung = MeldebildModel.objects.get(beschreibung = self.meldebild)
                        einsatzmod.meldebild = meldebild_beschreibung
                    except Meldebild.DoesNotExist:
                        meldebild_beschreibung = MeldebildModel.objects.get(beschreibung = "Kein Meldebild vorhanden")
                        einsatzmod.meldebild = meldebild_beschreibung
                #Datumangaben werden überprüft
                elif attr == "einsatzerzeugt":
                    try:
                        hilf = re.split('\.+|\:+|\ +',self.einsatzerzeugt,5)
                        datal = date(int(hilf[2]),int(hilf[1]),int(hilf[0]))
                    except:
                        datal = date(2001,01,01)
                    try:
                        if hilf[3]:
                            zeital = time(int(hilf[3]),int(hilf[4]),int(hilf[5]))
                    
                    except:
                        zeital = time(0,0,0)
                    # Timestamp aus Datum und Zeit wird generiert
                    tstamp = datetime.combine(datal,zeital)
                    einsatzmod.einsatzerzeugt  = tstamp
                else:
                    setattr(einsatzmod, attr, getattr(self, attr) )
            #Objekt wird in die DB gespeichert
            einsatzmod.save()
        # Sollte ein unerwarteter Fehler auftreten wird dies auf der Console ausgegeben und nicht in die DB gespeichert
        except:
            print "Fehler bei Einsatz mit Id: " + str(self.einsatz)
            
        
    def closeeinsatz(self, closeeinsatz_id):
        """
        Diese Methode updatet bestehende Einsätze,
        indem sie das abgeschlossen-Attribut auf true setzt
        """
        try:  
            einsatz = EinsatzModel.objects.get(einsatz = closeeinsatz_id)
        except EinsatzModel.DoesNotExist:
            return False
        if einsatz:
            einsatz.abgeschlossen = True
            einsatz.save()


class DispoKlasse(object):
    """
    Diese Klasse dient dazu die Dispos pro Einsatz
    korrekt in die Db zu speichern
    """
    def __init__(self):
        # Default-Werte werden gesetzt
        datal  = date(2001,01,01)
        zeital = time(0,0,0)
        tstamp = datetime.combine(datal,zeital)
        self.einsatz = 0
        self.dispo = 0
        self.disponame= ""
        self.zeitdispo = tstamp
        self.zeitalarm = tstamp
        self.zeitaus = tstamp
        self.zeitein = tstamp
        self.hintergrund = ""
        
    
    
    def getModel(self):
        """
        Besteht bereits ein Einsatz mit der derselben ID,
        wird dieser herangezogen und geupdatet
        """
        try: 
            einsatz_id = EinsatzModel.objects.get(einsatz = self.einsatz)
            dispomod = DispoModel.objects.get(dispo=self.dispo,einsatz = einsatz_id)
            return dispomod
        except (EinsatzModel.DoesNotExist, DispoModel.DoesNotExist):
            return False



    def save(self):
        """
        Speichert die Attribute des Objekts in die DB
        """
        
        # get the database model of the dispo
       
        dispomod = self.getModel()
        if not dispomod:
            dispomod = DispoModel()
           
        # Alle Dispo-Attribute werden durchgegangen
        dispotags = [ "einsatz", "dispo", "disponame" ,"zeitdispo", "zeitalarm", "zeitaus", "zeitein",
            "hintergrund"] 
        try:
            for attr in dispotags:
                if attr == "einsatz":
                    # Hole das zugehörige Einsatzobjekt aus der DB
                    einsatz_id = EinsatzModel.objects.get(einsatz = self.einsatz)
                    dispomod.einsatz = einsatz_id
                # Datumangaben werden überprüft
                elif attr == "zeitdispo" or attr == "zeitalarm" or attr == "zeitaus" or attr =="zeitein":
                    try: 
                        hilf = re.split('\.+|\:+|\ +',getattr(self,attr),5)
                        datal = date(int(hilf[2]),int(hilf[1]),int(hilf[0]))
                    except:
                        datal = date(2001,01,01)
                    try:
                        if hilf[3]:
                            zeital = time(int(hilf[3]),int(hilf[4]),int(hilf[5]))
                    except:
                        zeital = time(0,0,0)
                    # Timestamp wird aus Datum und Zeit generiert
                    tstamp = datetime.combine(datal,zeital)
                    setattr(dispomod,attr,tstamp)
                else:
                    setattr(dispomod, attr, getattr(self, attr) )
            # Alle Attribute werden in die DB gespeichert
            dispomod.save()
        # Tritt ein unerwarteter Fehler auf wird dieser in der Console ausgegeben
        except:
            print "Fehler bei Dispo mit ID: " + str(self.dispo)
        
    
 

class XML(object):
    """
    Diese Klasse parsed das übergegeben XML-File
    """
    def __init__(self, xml):
        """
        DOKU
        """
        einsatz_id = 0
        xml_root = etree.fromstring(xml)
        context = etree.iterwalk(xml_root, events=("start",))
       
        # Alle Attribute des XML-Files werden durchgelaufen
        for action,elem in context:
            if elem.tag != "root":
                if elem.tag == "einsatz":
                    einsatzobj = EinsatzKlasse()
                    einsatz_id = elem.get("id")
                    setattr(einsatzobj, elem.tag, elem.get("id"))
                elif elem.tag == "einsatznr":
                    setattr(einsatzobj,elem.tag,elem.text)
                    einsatzobj.save()
                elif elem.tag == "dispo":
                    dispoobj = DispoKlasse()
                    setattr(dispoobj, "einsatz", einsatz_id)
                    setattr(dispoobj, elem.tag,elem.get("id"))
                elif elem.tag == "disponame" or elem.tag == "zeitdispo" or elem.tag =="zeitalarm" or elem.tag =="zeitaus" or elem.tag =="zeitein":
                    setattr(dispoobj, elem.tag,elem.text)
                elif elem.tag == "hintergrund":
                    setattr(dispoobj, elem.tag, elem.text)
                    dispoobj.save()
                elif elem.text:
                    setattr(einsatzobj,elem.tag,elem.text)
        
        #Suche nicht abgeschlossene Einsaetze und schliesse sie ggfls. ab
       
        unabgeschl = EinsatzModel.objects.filter(abgeschlossen = False)
        # Alle unabgeschlossenen Einsätze werden durchgelaufen
        for unab in unabgeschl:
            close = 0 
            xml_root = etree.fromstring(xml)
            context = etree.iterwalk(xml_root, events=("start",))
            for action,elem in context:
               if elem.tag == "einsatz":
                    if elem.get("id") == unab.einsatz:
                        close = 1
            # Befindet sich ein nicht abgeschlossener Einsatz nicht in dem XML-File, wird dieser abgeschlossen
            if close == 0: 
                closeeins = EinsatzKlasse()
                closeeins.closeeinsatz(unab.einsatz)
