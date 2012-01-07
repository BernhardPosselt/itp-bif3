#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Django imports
from django.db import models


#News  
class News(models.Model):
    datum = models.DateTimeField("Datum")
    titel = models.CharField("Titel", max_length=400)
    text = models.TextField("Beschreibung")
    modifiziert = models.DateTimeField(auto_now=True)
    released = models.BooleanField("Veröffentlicht", blank=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __unicode__(self):
        return self.titel   

#Alarmstufen        
class Alarmstufen(models.Model):
	stufe = models.CharField("Alarmstufe", max_length=2, primary_key=True)
	modifiziert = models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name = "Alarmstufe"
		verbose_name_plural = "Alarmstufen"
		
	def __unicode__(self):
		return self.stufe
		
#Meldebilder        
class Meldebilder(models.Model):
	beschreibung = models.CharField("Beschreibung", max_length=200)
	stufe = models.ForeignKey("Alarmstufen")
	modifiziert = models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name = "Meldebild & Ausrückordnung"
		verbose_name_plural = "Meldebilder & Ausrückordnungen"
		
	def __unicode__(self):
		return self.beschreibung


        
#Einsatz
class Einsaetze(models.Model):
    """
    Diese Eintraege werden automatisch vom Hauptserver abgerufen und in die
    Datenbank geschrieben. Bitte nur aendern, wenn es wirklich notwendig ist!
    Die Daten fuer den Einsatz. Ein Einsatz kann an mehrere 
    :model:`infoscreen_screen.Dispo` vergeben werden. 
    """
    einsatz = models.CharField("Einsatz ID", unique=True, max_length=200,
        help_text="Die Nummer die für den Einsatz von der Leistelle vergeben \
            wird. Ist immer eindeutig.")
    strasse = models.CharField("Adresse", max_length=300, blank=True)
    nummer1 = models.CharField("Hausnummer", max_length=50, blank=True)
    nummer2 = models.CharField("Stiege", max_length=50, blank=True)
    nummer3 = models.CharField("Tür", max_length=50, blank=True)
    plz = models.IntegerField("Postleitzahl", blank=True, null=True)
    ort = models.CharField("Ort", max_length=200, blank=True)    
    bemerkung = models.TextField("Bemerkungen", blank=True)
    objekt = models.CharField("Objekt", blank=True, max_length=200)
    einsatznr = models.IntegerField("Einsatznummer", unique=True) # unique?
    einsatzerzeugt = models.DateTimeField("Einsatz erzeugt")    
    meldebild = models.ForeignKey("Meldebilder")    
    melder = models.TextField("Melder", blank = True, max_length=200)
    abgeschlossen = models.BooleanField("Abgeschlossen", blank=True)
    ausgedruckt = models.BooleanField("Ausgedruckt", blank=True)
    modifiziert = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Einsatz"
        verbose_name_plural = "Einsätze"

    def __unicode__(self):
        return "%s: %s" % (self.einsatz, self.bemerkung)
    
#Dispo - Feuerwehren alarmiert  
class Dispos(models.Model):
    einsatz = models.ForeignKey("Einsaetze")
    dispo = models.IntegerField("Dispo ID")
    disponame = models.CharField("Name", max_length=200)
    zeitdispo = models.DateTimeField("Dispozeit")
    zeitalarm = models.DateTimeField("Alarmierungszeit", blank=True, null=True)
    zeitaus = models.DateTimeField("Ausrückzeit", blank=True, null=True)
    zeitein = models.DateTimeField("Einrückzeit", blank=True, null=True)
    hintergrund = models.CharField("Hintergrund", max_length =200,blank=True)
    modifiziert = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dispo"
        verbose_name_plural = "Dispos"
        unique_together = ("einsatz", "dispo")

    def __unicode__(self):
        return self.disponame
        
#Fahrzeuge    
class Fahrzeuge(models.Model):
    kennzeichen = models.CharField("Kennzeichen", max_length=200, blank=True)
    funkrufname = models.CharField("Funkrufname", max_length=200, blank=True)
    kuerzel = models.CharField("Kürzel", max_length=12)
    beschreibung = models.CharField("Beschreibung", max_length=100)
    modifiziert = models.DateTimeField(auto_now=True)
    reperatur = models.BooleanField("In Reperatur", blank=True)

    class Meta:
        verbose_name = "Fahrzeug"
        verbose_name_plural = "Fahrzeuge"

    def __unicode__(self):
        return self.kuerzel
        
        
# Geraete    
class Geraete(models.Model):
    beschreibung = models.CharField("Beschreibung", max_length=100)
    modifiziert = models.DateTimeField(auto_now=True)
    reperatur = models.BooleanField("In Reperatur", blank=True)

    class Meta:
        verbose_name = "Gerät"
        verbose_name_plural = "Geräte"

    def __unicode__(self):
        return self.beschreibung
        
   
class Ausrueckordnungen(models.Model):
    fahrzeug = models.ForeignKey("Fahrzeuge")
    meldebild = models.ForeignKey("Meldebilder")
    position = models.PositiveSmallIntegerField("Position")
    modifiziert = models.DateTimeField(auto_now=True)
 
    class Meta:		
        verbose_name = "Ausrückordnung"
        verbose_name_plural = "Ausrückordnungen"
        ordering = ["position"]
        unique_together = ("fahrzeug", "meldebild")

    def __unicode__(self):
        return self.meldebild.beschreibung
