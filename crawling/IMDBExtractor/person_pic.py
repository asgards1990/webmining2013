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

priority_min=0
priority_max=10000

person_conn =  Connector.IMDBStatusConnector.IMDBPersonStatusConnector()
person_id_tab = person_conn.getDownloadedNoImage(priority_min,priority_max)[:1000]
for person_id in person_id_tab:
   FilmExtractor.IMDB_Extractor.IMDB_PersonExtractorPicture(person_id)
   time.sleep(random.random())
   


