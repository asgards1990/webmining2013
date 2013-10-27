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

   filmPage.extractFilmPage_DB()


def IMDB_awardsExtract(film_id):
   #sur la page awards
   logger.debug("Lancement de l'extraction des awards pour le film {}".format(film_id))
   awardsPage = IMDBExtractor_Awards(film_id)

   awardsPage.extractAwardsPage_DB()


def hasWon(status):
   return True if status.upper()=="WON" else False

def IMDB_reviewsExtract(film_id):
   logger.debug("Lancement de l'extraction des reviews pour le film {}".format(film_id))
   reviewPage = IMDBExtractor_Reviews(film_id)

   reviewPage.extractReviewsPage_DB()
   

   #TODO extraire le FullReviewURL

def IMDB_keywordsExtract(film_id):
   #sur la page keywords
   logger.debug("Lancement de l'extraction des keywords pour le film {}".format(film_id))
   keywordsPage = IMDBExtractor_Keyword(film_id)

   keywordsPage.extractKeywordsPage_DB()


def IMDB_companyCreditsExtractor(film_id):
   #sur la page companycredits
   logger.debug("Lancement de l'extraction des de la page Company Credits pour le film {}".format(film_id))
   companyCreditsPage = IMDBExtractor_companyCredits(film_id)

   companyCreditsPage.extractCompanyCreditsPage_DB()


def IMDB_fullCreditsExtractor(film_id):
   logger.debug("Lancement de l'extraction des de la page full credits pour le film {}".format(film_id))
   fullCreditsPage = IMDBExtractor_fullCredits(film_id)

   fullCreditsPage.extractFullCreditsPage_DB()


def IMDB_personExtractor(person_id):
   logger.debug("Lancement de l'extraction de la page person pour {}".format(person_id))
   personPage = IMDBExtractor_Person(person_id)

   personPage.extractPerson_DB()

def IMDB_SuperExtractor(film_id):
   IMDB_filmExtract(film_id) 
   IMDB_awardsExtract(film_id)
   IMDB_keywordsExtract(film_id)
   IMDB_reviewsExtract(film_id) 
   IMDB_companyCreditsExtractor(film_id)
   IMDB_fullCreditsExtractor(film_id)

