# /usr/bin/env python
# -*- coding: latin-1 -*-


####################################################################

#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import IMDBExtractor_config as IMDBExtractorConfig

import Connector.IMDBStatusConnector
import FilmExtractor.IMDB_Extractor

from status.models import *
from cinema.models import *

import threading
import time
import random
logger = initLogger.getLogger(IMDBExtractorConfig.EXTRACTOR_PERSON_PIC_LOGGER_NAME)

###################################################################

year_min=1980
year_max=2012
priority_max=1000


film_conn = Connector.IMDBStatusConnector.IMDBFilmStatusConnector()
film_id_tab = film_conn.getExtractedWithAwards()
for film_id in film_id_tab:
   logger.debug('Film en cours d extraction : {}'.format(film_id))
   Connector.IMDBStatusConnector.IMDBFilmStatusConnector().setExtractedStatus(film_id, "0")
   FilmExtractor.IMDB_Extractor.IMDB_awardsExtract(film_id)
   Connector.IMDBStatusConnector.IMDBFilmStatusConnector().setExtractedStatus(film_id, "1")
   

#Potentiel problème avec : [<IMDBFilmStatus: tt0099533 status>, <IMDBFilmStatus: tt0165436 status>, <IMDBFilmStatus: tt1318830 status>, <IMDBFilmStatus: tt0155902 status>]



