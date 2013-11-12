# /usr/bin/env python
# -*- coding: latin-1 -*-

####################################################################


#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import FilmExtractor_config as FilmExtractorConfig

from IMDBExtractor.IMDBExtractor import *
from cinema.models import *

logger = initLogger.getLogger(FilmExtractorConfig.IMDB_FILM_EXTRACTOR_LOGGER_NAME)

###################################################################

################################################################
#
#                        IMDB_*Extract Family
#
##################################################################

""" Les fonctions de ce module créent les objets nécessaires à l'extraction et remplissent la DB en appelant les fonction du module FilmExtractor_utils. Il existe une fonction par type de page"""


   

def IMDB_filmExtract(film_id):
   logger.debug("Lancement de l'extraction de la Page film pour le film {}".format(film_id))
   filmPage = IMDBExtractor_Film(film_id)      # Sur la main page directement
   if filmPage.isExtractable :
      filmPage.extractFilmPage_DB()


def IMDB_awardsExtract(film_id):
   #sur la page awards
   logger.debug("Lancement de l'extraction des awards pour le film {}".format(film_id))
   awardsPage = IMDBExtractor_Awards(film_id)
   if awardsPage.isExtractable:
      awardsPage.extractAwardsPage_DB()

def IMDB_awardsExtractInstitution(film_id):
   #sur la page awards
   logger.debug("Lancement de l'extraction des awards pour le film {}".format(film_id))
   awardsPage = IMDBExtractor_Awards(film_id)
   if awardsPage.isExtractable:
      awardsPage.extractInstitution()


def IMDB_actorsDirectorsExtract(film_id):
   logger.debug("Lancement de l'extraction des acteurs/directeurs  pour le film {}".format(film_id))
   fullCreditsPage = IMDBExtractor_fullCredits(film_id)
   if fullCreditsPage.isExtractable:
      fullCreditsPage.extractFullCredit_Actor_DB()


def IMDB_reviewsExtract(film_id):
   logger.debug("Lancement de l'extraction des reviews pour le film {}".format(film_id))
   reviewPage = IMDBExtractor_Reviews(film_id)
   if reviewPage.isExtractable:
      reviewPage.extractReviewsPage_DB()
   

   #TODO extraire le FullReviewURL

def IMDB_keywordsExtract(film_id):
   #sur la page keywords
   logger.debug("Lancement de l'extraction des keywords pour le film {}".format(film_id))
   keywordsPage = IMDBExtractor_Keyword(film_id)
   if keywordsPage.isExtractable:
      keywordsPage.extractKeywordsPage_DB()


def IMDB_companyCreditsExtractor(film_id):
   #sur la page companycredits
   logger.debug("Lancement de l'extraction des de la page Company Credits pour le film {}".format(film_id))
   companyCreditsPage = IMDBExtractor_companyCredits(film_id)
   if companyCreditsPage.isExtractable:
      companyCreditsPage.extractCompanyCreditsPage_DB()


def IMDB_fullCreditsExtractor(film_id):
   logger.debug("Lancement de l'extraction des de la page full credits pour le film {}".format(film_id))
   fullCreditsPage = IMDBExtractor_fullCredits(film_id)
   if fullCreditsPage.isExtractable:
      fullCreditsPage.extractFullCreditsPage_DB()


def IMDB_PersonExtractor(person_id):
   logger.debug("Lancement de l'extraction de la page person pour {}".format(person_id))
   personPage = IMDBExtractor_Person(person_id)
   if personPage.isExtractable:
      personPage.extractPerson_DB()
   
   conn = IMDBPersonStatusConnector()
   IMDB_setIsExtracted(person_id,conn)

def IMDB_PersonExtractorPicture(person_id):
   logger.debug("Lancement de l'extraction de la page person pour {}".format(person_id))
   personPage = IMDBExtractor_Person(person_id)
   personPage.createExtractorEngine()
   personPage.extractPic()
      

def IMDB_CompanyExtractor(company_id):
   logger.debug("Lancement de l'extraction de la page company pour {}".format(company_id))
   companyPage = IMDBExtractor_Producer(company_id)
   if companyPage.isExtractable:
      companyPage.extractCompany_DB()
   conn = IMDBCompanyStatusConnector()
   IMDB_setIsExtracted(company_id,conn)


def IMDB_SuperExtractor(film_id):
   IMDB_filmExtract(film_id) 
   IMDB_awardsExtract(film_id)
   IMDB_keywordsExtract(film_id)
   IMDB_reviewsExtract(film_id) 
   IMDB_companyCreditsExtractor(film_id)
   IMDB_fullCreditsExtractor(film_id)

   conn = IMDBFilmStatusConnector()
   IMDB_setIsExtracted(film_id,conn)



def IMDB_setIsExtracted(id_,conn):
   conn.setExtractedStatus(id_,1)

