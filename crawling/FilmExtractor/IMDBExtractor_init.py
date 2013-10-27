# /usr/bin/env python
# -*- coding: latin-1 -*-


####################################################################

#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import FilmExtractor_config as FilmExtractorConfig

import Connector.IMDBStatusConnector
import FilmExtractor.IMDB_Extractor

from cinema.models import *

logger = initLogger.getLogger(FilmExtractorConfig.EXTRACTOR_IMDB_INIT_LOGGER_NAME)

###################################################################


#TODO Lancer des Threads sur les 3


film_conn = Connector.IMDBStatusConnector.IMDBFilmStatusConnector()
#person_conn =  IMDBPersonStatusConnector()
#company_conn =  IMDBCompanyStatusConnector()

film_id_tab = film_conn.getDownloadedNotExtracted()
FilmExtractor.IMDB_Extractor.IMDB_SuperExtractor(film_id_tab[0])         

#for film_id in film_id_tab:
#   FilmExtractor.IMDB_Extractor.IMDB_SuperExtractor(film_id)
"""
person_id_tab = person_conn.getDownloadedNotExtracted()
for person_id in person_id_tab:
   IMDB_personExtractor(person_id)

company_id_tab = company_conn.getDownloadedNotExtracted()
for company_id in company_id_tab:
   IMDB_companyExtractor(person_id)a
"""

