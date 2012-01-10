#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Django imports
from django.db import models


#News  
class News(models.Model):
    datum = models.DateTimeField("Datum", help_text="Das Datum des Eintrages. \
        Die Einträge werden absteigend nach dem neuesten Datum sortiert. Nur \
        die neuesten 5 Einträge werden angezeigt.")
    titel = models.CharField("Titel", max_length=400, help_text="Die Überschrift \
        des Newseintrages")
    text = models.TextField("Beschreibung", help_text="Die Beschreibung beinhaltet \
        den eigentlichen Newstext. In der Beschreibung ist HTML erlaubt. Für \
        Bilder sind 2 CSS Klassen definiert: left und right. Damit werden die \
        Bilder im Textfluss links oder rechts platziert. Um ein Bild zB. rechts \
        im Textfluss zu platzieren tragen sie das Bild folgendermaßen ein:\
            &lt;img src=\"http://pfad.com/zum/bild.jpg\" class=\"left\" /&gt;\
        Absätze werden Automatisch in HTML Absätze umgewandelt.")
    modifiziert = models.DateTimeField(auto_now=True)
    released = models.BooleanField("Veröffentlicht", blank=True, 
        help_text="Ob der Newsbeitrag veröffentlicht \
            werden soll. Ist die Checkbox bei \"Veröffentlicht\" nicht gesetzt,\
             kann der Beitrag nur aufgerufen werden, wenn man ein ?preview=true\
              an der URL anhängt, zB:\
            /bildschirm/frieden/rechts/?preview=true\
            Das ermöglicht eine Vorschau des Beitrages ohne ihn zu veröffentlichen.")

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __unicode__(self):
        return self.titel   

#Alarmstufen        
class Alarmstufen(models.Model):
	stufe = models.CharField("Alarmstufe", max_length=2, primary_key=True, help_text="Alarmstufe mit max. Länge von 2 Zeichen, muss eindeutig sein")
	modifiziert = models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name = "Alarmstufe"
		verbose_name_plural = "Alarmstufen"
		
	def __unicode__(self):
		return self.stufe
		
#Meldebilder        
class Meldebilder(models.Model):
	beschreibung = models.CharField("Beschreibung", max_length=200, help_text = "Beschreibung des Meldebildes")
	stufe = models.ForeignKey("Alarmstufen", help_text = "Jedes Meldebild muss einer Alarmstufe zugewiesen sein")
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
        help_text="Die Nummer die für den Einsatz von der Leitstelle vergeben \
            wird. Ist immer eindeutig.")
    strasse = models.CharField("Adresse", max_length=300, blank=True, help_text = "Die Adresse des Einsatzes")
    nummer1 = models.CharField("Hausnummer", max_length=50, blank=True, help_text = "Hausnummer der Einsatzadresse")
    nummer2 = models.CharField("Stiege", max_length=50, blank=True, help_text = "Stiege der Einsatzadresse")
    nummer3 = models.CharField("Tür", max_length=50, blank=True, help_text = "Türnummer der Einsatzadresse")
    plz = models.IntegerField("Postleitzahl", blank=True, null=True, help_text = "Postleitzahl der Einsatzadresse")
    ort = models.CharField("Ort", max_length=200, blank=True, help_text = "Ort der Einsatzdresse")    
    bemerkung = models.TextField("Bemerkungen", blank=True, help_text = "Die Bemerkungen des Einsatzes, welche beim \
	Erstellen des Einsatzes angegeben wurden, enthalten meist wichtige Informationen zum Einsatz selbst")
    objekt = models.CharField("Objekt", blank=True, max_length=200, help_text = "Objekt in dem ein Einsatz nötig ist (z.B.: Krankenhaus, Schule, ...)")
    einsatznr = models.IntegerField("Einsatznummer", help_text = "Eindeutige Nummer für den Einsatz")
    einsatzerzeugt = models.DateTimeField("Einsatz erzeugt", help_text = "Datum und Uhrzeit an dem der Einsatz angelegt wurde")    
    meldebild = models.ForeignKey("Meldebilder", help_text = "Meldebild des Einsatzes")    
    melder = models.TextField("Melder", blank = True, max_length=200, help_text ="Person, welche den Einsatz gemeldet hat")
    abgeschlossen = models.BooleanField("Abgeschlossen", blank=True, help_text= "Ob der Einsatz bereits abgeschlossen wurde")
    ausgedruckt = models.BooleanField("Ausgedruckt", blank=True, help_text = "Ob der Einsatz bereits ausgedruckt wurde")
    modifiziert = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Einsatz"
        verbose_name_plural = "Einsätze"

    def __unicode__(self):
        return "%s: %s" % (self.einsatz, self.bemerkung)
    
#Dispo - Feuerwehren alarmiert  
class Dispos(models.Model):
    einsatz = models.ForeignKey("Einsaetze", help_text ="Einsatz dem der Dispo zugeordnet ist")
    dispo = models.IntegerField("Dispo ID", help_text = "ID des Dispo, muss nicht eindeutig sein")
    disponame = models.CharField("Name", max_length=200, help_text = "Name der alarmierten Feuerwehr")
    zeitdispo = models.DateTimeField("Dispozeit", help_text = "Zeit zu welcher der Dispo erstellt wurde")
    zeitalarm = models.DateTimeField("Alarmierungszeit", blank=True, null=True, help_text = "Zeit zu welcher die Feuerwehr alarmiert wurde")
    zeitaus = models.DateTimeField("Ausrückzeit", blank=True, null=True, help_text = "Zeitpunkt des Ausrückens der Feuerwehr")
    zeitein = models.DateTimeField("Einrückzeit", blank=True, null=True, help_text = "Zeitpunkt des Zurückkehrens der Feuerwehr")
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
    kennzeichen = models.CharField("Kennzeichen", max_length=200, blank=True, help_text = "Kennzeichen (Nummernschild) des Einsatzfahrzeuges")
    funkrufname = models.CharField("Funkrufname", max_length=200, blank=True)
    kuerzel = models.CharField("Kürzel", max_length=12 , help_text = "Kürzel des Fahrzeugs welches am Einsatzbildschirm unter Ausrückeordnung angezeigt wird")
    beschreibung = models.CharField("Beschreibung", max_length=100, help_text = "Beschreibung des Fahrzeuges die zu Friedenszeiten auf dem rechten Bildschirm angezeigt wird.")
    modifiziert = models.DateTimeField(auto_now=True)
    reperatur = models.BooleanField("In Reperatur", blank=True, help_text= "Zeigt an ob das Fahrzeug in Reperatur ist")

    class Meta:
        verbose_name = "Fahrzeug"
        verbose_name_plural = "Fahrzeuge"

    def __unicode__(self):
        return self.kuerzel
        
        
# Geraete    
class Geraete(models.Model):
    beschreibung = models.CharField("Beschreibung", max_length=100, help_text="Kurze Beschreibung des Gerätes, welche zu Friedenszeiten auf dem rechten Bildschirm angezeigt wird")
    modifiziert = models.DateTimeField(auto_now=True)
    reperatur = models.BooleanField("In Reperatur", blank=True, help_text = "Zeigt an ob sich das Gerät in Reperatur befindet")

    class Meta:
        verbose_name = "Gerät"
        verbose_name_plural = "Geräte"

    def __unicode__(self):
        return self.beschreibung
        
   
class Ausrueckordnungen(models.Model):
    fahrzeug = models.ForeignKey("Fahrzeuge", help_text ="Bitte ein bereits angelegtes Fahrzeug auswählen")
    meldebild = models.ForeignKey("Meldebilder", help_text = "Bitte ein bereits angelegtes Meldebild auswählen")
    position = models.PositiveSmallIntegerField("Position", "Reichenfolge des Fahrzeuges bei einem Einsatz")
    modifiziert = models.DateTimeField(auto_now=True)
 
    class Meta:		
        verbose_name = "Ausrückordnung"
        verbose_name_plural = "Ausrückordnungen"
        ordering = ["position"]
        unique_together = ("fahrzeug", "meldebild")

    def __unicode__(self):
        return self.meldebild.beschreibung
