.. contents:: Inhaltsverzeichnis

======================
 Feuerwehr Infoscreen
======================

:Version: 0.1
:Keywords: python, jquery, django, web, html5, javascript, firefighters, infoscreen

Schreib hier die Beschreibung!!!

Setup
=====

Abhängigkeiten
--------------

* Django 1.3

* Python 2

* Python MySQL 

* Apache & mod_wsgi

* MySQL Server

* Python Docutils

* Python ReportLab

Ubuntu 11.10
------------
Das ganze kann wie folgt auf einem aktuellen Ubuntu installiert werden:

  sudo apt-get install python-django python-mysqldb apache2 libapache2-mod-wsgi mysql-server python-docutils python-reportlab

Debian oder älteres Ubuntu
--------------------------
Zuerst führt man folgendes aus:

  sudo apt-get install python-mysqldb apache2 libapache2-mod-wsgi mysql-server python python-support python-docutils python-reportlab

  
Danach muss das aktuelle Django von der Django-Homepage
heruntergeladen und installiert werden: https://www.djangoproject.com/download/



Developen
=========

Dazu geht man mit der Konsole (Bash) in das Projektverzeichnis und führt
folgendes aus:

  python manage.py runserver
  
Die Seite ist dann auf http://127.0.0.1:8000/ verfügbar

MySQL Tabellen werden von den Models mit folgendem Befehl generiert bzw upgedated

  ./syncdb.sh
  
Statischer Content wird von infoscreen_screen/static mit folgendem Befehl
in das Static-Verzeichnis kopiert:

  python manage.py collectstatic


Deployen mit Apache & Debian
============================
TBD

Code Conventions
================

* Einrücken mit 4 Spaces (kann man in den meisten Editoren konfigurieren)

.. image::  http://dl.dropbox.com/u/15205713/spaces.png

* Funktions/Methoden Kommentare in folgender Form (:PEP:`257`):

.. line-block::

  """Methodenbeschreibung   
   
   
  Keyword arguments:
  
  argument1 -- Beschreibung für argument 1 
  
  argument2 -- Beschreibung für argument 2
               
                                            
  """

README Markup Hilfe
===================
GOTO 

* http://docutils.sourceforge.net/docs/user/rst/quickref.html

* http://docutils.sourceforge.net/docs/ref/rst/directives.html
