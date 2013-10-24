#! /usr/bin/env python
# -*- coding: latin-1 -*-

#verifier que tous les modules peuvent être importés avant de commencer l'application
import Logger.init_logger as initLogger #initialise le logger
import init_config as initConfig

logger = initLogger.getLogger(initConfig.IMPORTS_LOGGER_NAME)


import MySQLdb

try:
   import lxml
except:
   logger.critical("Le module lxml est nécessaire pour l'application, mais n'a pas été trouvé. Installation requise")
   exit(1)
