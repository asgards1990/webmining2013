
# /usr/bin/env python
# -*- coding: latin-1 -*-



####################################################################


#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import UserAgent.userAgent_config as userAgentConfig
from urllib import FancyURLopener
import urllib

logger = initLogger.getLogger(userAgentConfig.USER_AGENT_LOGGER_NAME)

###################################################################


####################################################################

# Custom User-Agent to load IMDB search results

class CustomURLopener(FancyURLopener):
    version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"

logger.debug('Modification du User Agent')
urllib._urlopener = CustomURLopener()

####################################################################
