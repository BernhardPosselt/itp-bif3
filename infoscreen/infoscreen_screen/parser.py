from lxml import etree
from infoscreen.infoscreen_screen.models import Einsatz as EinsatzModel
from datetime import *
import re
from infoscreen.infoscreen_screen.models import Meldebilder as MeldebildModel
from infoscreen.infoscreen_screen.models import Dispo as DispoModel



class XML(object):
    """
    DOKU
    """
    
    # static vars for debug purposes

    dispotags = {"dispo", "disponame"}

    def __init__(self, xml):
        """
        DOKU
        """
        einsatztags = { "einsatz", "alarmstufe", "meldebild", "nummer1", "nummer2",
            "nummer3", "plz", "strasse", "ort", "objekt", "bemerkung", "einsatzerzeugt", 
            "melder", "einsatznr"}
        self.einsatz = 0
        self.alarmstufe = "DEF"
        self.meldebild= "DEFAULT"
        self.nummer1 = -1
        self.nummer2 = -1
        self.nummer3 = -1
        self.plz= -1
        self.adresse = "DEFAULT"
        self.ort = "DEFAULT"
        self.bemerkung = "DEFAULT"
        self.objekt = "DEFAULT"
        self.einsatznr = -1
        self.melder = "DEFAULT"
        self.einsatzerzeugt = date(2001,01,01)
        self.abgeschlossen = date(2001,01,01)
        self.ausgedruckt = False 
        self.modified = False
        self.lastModified = datetime.now()
        
        melder = 'Default'
        meldertel = 'Default'
         
        xml_tree = etree.parse(xml)
        xml_root = xml_tree.getroot()
        for mytag in einsatztags:
            context = etree.iterwalk(xml_root, tag=mytag)
            for action, elem in context:
                if elem.tag == "einsatz":
                    setattr( self,mytag, elem.get("id"))
                elif elem.text:
                    setattr( self, mytag, elem.text)
              

    def __setattr__(self, name, value):
        """Setter"""
        
        object.__setattr__(self, name, value)
    
     
    def isModified(self, einsatz):
        """
        Returns true if the timestamp from the file is newer than the
        Database entry
        """
        return einsatz.modifiziert == self.lastModified
    
    
    def getModel(self):
        """
        DOKU
        """
        try:
            einsatz = EinsatzModel.objects.get(einsatz=self.einsatz)
            return einsatz
        except EinsatzModel.DoesNotExist:
            return False



    def save(self):
        """
        Saves the values of the object into the database
        """
        
        # get the database model of the einsatz
        
        einsatz = self.getModel()
        if not einsatz:
            einsatz = EinsatzModel()
           

        # only save to database if einsatz is modified
        """if self.isModified(einsatz):     """      
        einsatztags = { "einsatz", "alarmstufe", "meldebild", "nummer1", "nummer2",
            "nummer3", "plz", "strasse", "ort", "objekt", "bemerkung", "einsatzerzeugt", 
            "melder", "einsatznr"}  
        for attr in einsatztags:
            if attr == "meldebild":
                meldebild_beschreibung = MeldebildModel.objects.get(beschreibung = self.meldebild)
                einsatz.meldebild = meldebild_beschreibung
            elif attr == "einsatzerzeugt":
                hilf = re.split('\.+|\:+|\ +',self.einsatzerzeugt,5)
                datal = date(int(hilf[2]),int(hilf[1]),int(hilf[0]))
                try:
                    if hilf[3]:
                        zeital = time(int(hilf[3]),int(hilf[4]),int(hilf[5]))
                
                except:
                    zeital = time(0,0,0)
                tstamp = datetime.combine(datal,zeital)
                einsatz.einsatzerzeugt  = tstamp
            else:
                setattr( einsatz, attr, getattr(self, attr) )
        
        einsatz.save()


