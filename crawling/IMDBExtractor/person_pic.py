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
import time
logger = initLogger.getLogger(FilmExtractorConfig.EXTRACTOR_IMDB_INIT_LOGGER_NAME)

###################################################################

priority_min=0
priority_max=10000

person_id_tab = person_conn.getDownloadedNotExtractedFiltered(priority_min,priority_max)[:1000]
for person_id in person_id_tab:
   FilmExtractor.IMDB_Extractor.IMDB_PersonExtractorPicture(person_id)
   


