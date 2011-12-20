from lxml import etree
from infoscreen.infoscreen_screen.models import Einsaetze as EinsatzModel
from datetime import *
import re
from infoscreen.infoscreen_screen.models import Meldebilder as MeldebildModel
from infoscreen.infoscreen_screen.models import Dispos as DispoModel

class EinsatzKlasse(object):
    """
    DOKU
    """
    def __init__(self):
        self.einsatz = 0
        self.alarmstufe = "DEF"
        self.meldebild= "DEFAULT"
        self.nummer1 = -1
        self.nummer2 = -1
        self.nummer3 = -1
        self.plz= -1
        self.strasse = "DEFAULT"
        self.ort = "DEFAULT"
        self.bemerkung = "DEFAULT"
        self.objekt = "DEFAULT"
        self.melder = "DEFAULT"
        self.einsatznr = -1
        self.einsatzerzeugt = date(2001,01,01)
        self.abgeschlossen = date(2001,01,01)
        self.ausgedruckt = False 
      
    
    
    def getModel(self):
        """
        DOKU
        """
        try:
            einsatzmod = EinsatzModel.objects.get(einsatz=self.einsatz)
            return einsatzmod
        except EinsatzModel.DoesNotExist:
            return False



    def save(self):
        """
        Saves the values of the object into the database
        """
        
        # get the database model of the einsatz
        
        einsatzmod = self.getModel()
        if not einsatzmod:
            einsatzmod = EinsatzModel()
           

        # only save to database if einsatz is modified
        """if self.isModified(einsatz):     """      
        einsatztags = { "einsatz", "alarmstufe", "meldebild", "nummer1", "nummer2",
            "nummer3", "plz", "strasse", "objekt","ort", "bemerkung", "einsatzerzeugt", 
            "melder", "einsatznr","ausgedruckt"}  
        for attr in einsatztags:
            if attr == "meldebild":
                meldebild_beschreibung = MeldebildModel.objects.get(beschreibung = self.meldebild)
                einsatzmod.meldebild = meldebild_beschreibung
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
                tstamp = datetime.combine(datal,zeital)
                einsatzmod.einsatzerzeugt  = tstamp
            else:
                setattr(einsatzmod, attr, getattr(self, attr) )
        
        einsatzmod.save()

class DispoKlasse(object):
    """
    DOKU
    """
    def __init__(self):
        self.einsatz = 0
        self.dispo = 0
        self.disponame= "DEFAULT"
        self.zeitdispo = date(2001,01,01)
        self.zeitalarm = date(2001,01,01)
        self.zeitaus = date(2001,01,01)
        self.zeitein = date(2001,01,01)
        self.hintergrund = "DEFAULT"
        
    
    
    def getModel(self):
        """
        DOKU
        """
        try:  
            einsatz_id = EinsatzModel.objects.get(einsatz = self.einsatz)
            dispomod = DispoModel.objects.get(dispo=self.dispo,einsatz = einsatz_id)
            return dispomod
        except DispoModel.DoesNotExist:
            return False



    def save(self):
        """
        Saves the values of the object into the database
        """
        
        # get the database model of the dispo
        
        dispomod = self.getModel()
        if not dispomod:
            dispomod = DispoModel()
           

        dispotags = { "einsatz", "dispo", "disponame" ,"zeitdispo", "zeitalarm", "zeitaus", "zeitein",
            "hintergrund"}  
        for attr in dispotags:
            if attr == "einsatz":
                einsatz_id = EinsatzModel.objects.get(einsatz = self.einsatz)
                dispomod.einsatz = einsatz_id
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
                tstamp = datetime.combine(datal,zeital)
                setattr(dispomod,attr,tstamp)
            else:
                setattr(dispomod, attr, getattr(self, attr) )
        
        dispomod.save()

class XML(object):
    """
    DOKU
    """
    

    def __init__(self, xml):
        """
        DOKU
        """
        einsatz_id = 0
        xml_tree = etree.parse(xml)
        xml_root = xml_tree.getroot()
        context = etree.iterwalk(xml_root, events=("start",))
       
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
                

