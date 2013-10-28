# /usr/bin/env python
# -*- coding: latin-1 -*-


####################################################################

#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import FilmExtractor_config as FilmExtractorConfig

import Connector.IMDBStatusConnector
import FilmExtractor.IMDB_Extractor

from status.models import *
from cinema.models import *

import threading

logger = initLogger.getLogger(FilmExtractorConfig.EXTRACTOR_IMDB_INIT_LOGGER_NAME)

###################################################################


def setUnextractedToBuggyPerson():
   """Met le bit extracted à 0 sur les personnes bugguées"""
   object_list = Person.objects.filter(name="")
   person_id_tab = map(lambda s: s.imdb_id, object_list)
   for person_id in person_id_tab:
      Connector.IMDBStatusConnector.IMDBPersonStatusConnector().setExtractedStatus(person_id, "0")

def setUnextractedToAllPerson():
   """Met le bit extracted à 0 sur toutes les personnes"""
   object_list = Person.objects.all()
   person_id_tab = map(lambda s: s.imdb_id, object_list)
   for person_id in person_id_tab:
      Connector.IMDBStatusConnector.IMDBPersonStatusConnector().setExtractedStatus(person_id, "0")

def reExtractAllPerson():
   """Ré extrait toutes les personnes dont le champ name est nul (caractéristique d'un bug)"""
   object_list = Person.objects.all()
   person_id_tab = map(lambda s: s.imdb_id, object_list)

   setUnextractedToAllPerson()

   for person_id in person_id_tab:
      FilmExtractor.IMDB_Extractor.IMDB_personExtractor(person_id)

def setUnextractedToBuggyCompany():
   """Met le bit extracted à 0 sur les personnes bugguées"""
   object_list = ProductionCompany.objects.filter(name="")
   company_id_tab = map(lambda s: s.imdb_id, object_list)
   for company_id in company_id_tab:
      Connector.IMDBStatusConnector.IMDBPCompanyStatusConnector().setExtractedStatus(company_id, "0")

def reExtractBuggyPerson():
   """Ré extrait toutes les personnes dont le champ name est nul (caractéristique d'un bug)"""
   object_list = Person.objects.filter(name="")
   person_id_tab = map(lambda s: s.imdb_id, object_list)

   setUnextractedToBuggyPerson()

   for person_id in person_id_tab:
      FilmExtractor.IMDB_Extractor.IMDB_personExtractor(person_id)

def reExtractBuggyCompany():
   """Ré extrait toutes les personnes dont le champ name est nul (caractéristique d'un bug)"""
   object_list = ProductionCompany.objects.filter(name="")
   company_id_tab = map(lambda s: s.imdb_id, object_list)

   setUnextractedToBuggyCompany()

   for company_id in company_id_tab:
      FilmExtractor.IMDB_Extractor.IMDB_companyExtractor(company_id)

#TODO Lancer des Threads sur les 3


film_conn = Connector.IMDBStatusConnector.IMDBFilmStatusConnector()
person_conn =  Connector.IMDBStatusConnector.IMDBPersonStatusConnector()
company_conn =  Connector.IMDBStatusConnector.IMDBCompanyStatusConnector()

class getIMDBFilm(threading.Thread):
    def __init__(self, nom = 'getIMDBFilm'):
        threading.Thread.__init__(self)
        self.nom = nom
        self._stopevent = threading.Event( )
    def run(self):
       while True:
          film_id_tab = film_conn.getDownloadedNotExtracted()[:100]
          for film_id in film_id_tab:
             FilmExtractor.IMDB_Extractor.IMDB_SuperExtractor(film_id)

class getIMDBPerson(threading.Thread):
    def __init__(self, nom = 'getIMDBPerson'):
        threading.Thread.__init__(self)
        self.nom = nom
        self._stopevent = threading.Event( )
    def run(self):
       while True:
          person_id_tab = person_conn.getDownloadedNotExtracted()[:1000]
          for person_id in person_id_tab:
             PersonExtractor.IMDB_Extractor.IMDB_PersonExtractor(person_id)

class getIMDBCompany(threading.Thread):
    def __init__(self, nom = 'getIMDBCompany'):
        threading.Thread.__init__(self)
        self.nom = nom
        self._stopevent = threading.Event( )
    def run(self):
       while True:
          company_id_tab = company_conn.getDownloadedNotExtracted()[:1000]
          for company_id in company_id_tab:
             CompanyExtractor.IMDB_Extractor.IMDB_CompanyExtractor(company_id)


IMDB_FILM_EXTRACTOR = getIMDBFilm()
IMDB_PERSON_EXTRACTOR = getIMDBPerson()
IMDB_COMPANY_EXTRACTOR = getIMDBCompany()

IMDB_FILM_EXTRACTOR.start()
IMDB_PERSON_EXTRACTOR.start()
IMDB_COMPANY_EXTRACTOR.start()


