# /usr/bin/env python
# -*- coding: utf-8 -*-



####################################################################

#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import spider_config as SpiderConfig

import urllib

logger = initLogger.getLogger(SpiderConfig.SPIDER_LOGGER_NAME)


####################################################################

def search_url(year, start_pos):
    url = "http://www.imdb.com/search/title?count=250&release_date=" + str(year) + "," + str(year) + "&sort=release_date_us,asc&start=" + str(start_pos) + "&title_tyearpe=feature,documentary&view=simple"
    return url


logger.debug("Test search_url: " + search_url(1999,1000))
