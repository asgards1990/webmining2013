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

film_conn = Connector.IMDBStatusConnector.IMDBFilmStatusConnector()
while True:

          film_id_tab = film_conn.getDownloadedNotExtractedFiltered(year_min, year_max, priority_max)[:1000]
          for film_id in film_id_tab:
             logger.debug('Film en cours d extraction : {}'.format(film_id))
             FilmExtractor.IMDB_Extractor.IMDB_awardsExtract(film_id)


