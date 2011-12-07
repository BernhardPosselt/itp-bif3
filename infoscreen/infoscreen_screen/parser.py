from lxml import etree
from infoscreen.infoscreen_screen.models import Einsatz as EinsatzModel
import time


class XML(object):
    """
    DOKU
    """
    
    # static vars for debug purposes
   
    

    einsatztags = { "einsatz", "alarmstufe", "meldebild", "nummer1", "nummer2",
    "nummer3", "plz", "strasse", "ort", "objekt", "bemerkung", "einsatzerzeugt", 
    "melder", "einsatznr"}

    dispotags = {"dispo", "disponame"}

    def __init__(self, xml):
        """
        DOKU
        """
        self.einsatzid = 0
        self.alarmstufe = "DEF"
        self.meldebild= "DEFAULT"
        self.hausnummer = -1
        self.stiege = -1
        self.tuer = -1
        self.postleitzahl= -1
        self.adresse = "DEFAULT"
        self.ort = "DEFAULT"
        self.bemerkung = "DEFAULT"
        self.objekt = "DEFAULT"
        self.einsatznummer = -1
        self.erzeugt = 01,01,2001
        self.abgeschlossen = 01,01,2001
        self.ausgedruckt = False 
        self.modified = False
        self.lastModified = time.time()
         
        xml_tree = etree.parse(xml)
        xml_root = xml_tree.getroot()
        for tags in einsatztags:
            context = etree.iterwalk(
                        xml_root, tag=tags)
            for action, elem in context:
                if elem.tag == "einsatz":
                    einsatz = elem.tag,elem.get("id");
                elif elem.tag == "dispo":
                    einsatz = elem.tag,elem.get("id");
                else:
                     einsatz = elem.tag,elem.text;
                     

    def __setattr__(self, name, value):
        """Setter"""
        
                
        object.__setattr__(self, name, value)
    
     
    def isModified(self, einsatz):
        """
        Returns true if the timestamp from the file is newer than the
        Database entry
        """
        return einsatz.lastModified == self.lastModified
    
    
    def getModel(self):
        """
        DOKU
        """
        try:
            einsatz = Einsatzmodel.objects.get(einsatzID=self.einsatzID)
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
        if self.isModified(einsatz):           
            
            for attr in einsatztags:
                setattr( einsatz, attr, getattr(self, attr) )
            
            einsatz.save();


