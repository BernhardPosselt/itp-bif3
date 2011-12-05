#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Django imports
from django.db import models


#Willkommennachrichten
class Willkommen(models.Model):
    titel = models.CharField("Willkommenstitel", max_length=300)
    nachricht = models.TextField("Willkommensnachricht", blank=True)
    
    class Meta:
        verbose_name = "Willkommensnachricht"
        verbose_name_plural = "Willkommensnachrichten"

    def __unicode__(self):
        return self.titel

#News  
class News(models.Model):
    datum = models.DateTimeField("Datum")
    titel = models.CharField("Titel", max_length=400)
    text = models.TextField("Beschreibung")
    modifiziert = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __unicode__(self):
        return self.titel   

#Alarmstufen        
class Alarmstufen(models.Model):
	stufe = models.CharField("Alarmstufe", max_length=2, primary_key=True)
	
	class Meta:
		verbose_name = "Alarmstufe"
		verbose_name_plural = "Alarmstufen"
		
	def __unicode__(self):
		return self.stufe
		
#Meldebilder        
class Meldebilder(models.Model):
	beschreibung = models.CharField("Beschreibung", max_length=200)
	stufe = models.ForeignKey("Alarmstufen")
	
	class Meta:
		verbose_name = "Meldebilder"
		verbose_name_plural = "Meldebilder"
		
	def __unicode__(self):
		return self.beschreibung


        
#Einsatz
class Einsatz(models.Model):
    """
    Diese Eintraege werden automatisch vom Hauptserver abgerufen und in die
    Datenbank geschrieben. Bitte nur aendern, wenn es wirklich notwendig ist!
    Die Daten fuer den Einsatz. Ein Einsatz kann an mehrere 
    :model:`infoscreen_screen.Dispo` vergeben werden. 
    """
    einsatzID = models.CharField("Einsatz ID", unique=True, max_length=200,
        help_text="Die Nummer die für den Einsatz von der Leistelle vergeben \
            wird. Ist immer eindeutig.")
    adresse = models.CharField("Adresse", max_length=300, blank=True)
    hausnummer = models.CharField("Hausnummer", max_length=50, blank=True)
    stiege = models.CharField("Stiege", max_length=50, blank=True)
    tuer = models.CharField("Tür", max_length=50, blank=True)
    postleitzahl = models.IntegerField("Postleitzahl", blank=True)
    ort = models.CharField("Ort", max_length=200, blank=True)    
    bemerkung = models.TextField("Bemerkungen", blank=True)
    objekt = models.CharField("Objekt", blank=True, max_length=200)
    einsatznummer = models.IntegerField("Einsatznummer", unique=True) # unique?
    erzeugt = models.DateTimeField("Einsatz erzeugt")    
    meldebild = models.ForeignKey("Meldebilder")    
    abgeschlossen = models.BooleanField("Abgeschlossen", blank=True)
    ausgedruckt = models.BooleanField("Ausgedruckt", blank=True)
    modifiziert = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Einsatz"
        verbose_name_plural = "Einsätze"

    def __unicode__(self):
        return "%s: %s" % (self.einsatzID, self.bemerkung)
    
#Dispo - Feuerwehren alarmiert  
class Dispo(models.Model):
    einsatz = models.ForeignKey("Einsatz")
    dispoID = models.IntegerField("Dispo ID")
    name = models.CharField("Name", max_length=200)
    zeit = models.DateTimeField("Dispozeit")
    alarm = models.DateTimeField("Alarmierungszeit", blank=True)
    aus = models.DateTimeField("Ausrückzeit", blank=True)
    ein = models.DateTimeField("Einrückzeit", blank=True)
    modifiziert = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dispo"
        verbose_name_plural = "Dispos"

    def __unicode__(self):
        return self.name
        
#Fahrzeuge    
class Fahrzeuge(models.Model):
    kennzeichen = models.CharField("Kennzeichen", max_length=200, blank=True)
    funkrufname = models.CharField("Funkrufname", max_length=200, blank=True)
    kuerzel = models.CharField("Kürzel", max_length=12)
    beschreibung = models.CharField("Beschreibung", max_length=100)
    modifiziert = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fahrzeug"
        verbose_name_plural = "Fahrzeuge"

    def __unicode__(self):
        return self.kuerzel
   
class Ausrueckordnung(models.Model):
    fahrzeug = models.ForeignKey("Fahrzeuge")
    meldebild = models.ForeignKey("Meldebilder")
    position = models.PositiveSmallIntegerField("Position")
 
    class Meta:		
        verbose_name = "Ausrückordnung"
        verbose_name_plural = "Ausrückordnungen"
        ordering = ["position"]

    def __unicode__(self):
        return self.meldebild.beschreibung
