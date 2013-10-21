#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""  Ce fichier contient des Cleaners customisés qui étendent la classe cleaner du module lxml pour definir des cleaners de base appropriés et customisés pour les documents HTML type
     cf : http://lxml.de/api/lxml.html.clean.Cleaner-class.html pour plus d'info 
     Liste des attributs par défaut

            scripts = True,\
            javascript = True,\
            comments = True,\
            style = False,\
            links = True,\
            meta = True,\
            page_structure = True,\
            processing_instructions = True,\
            embedded = True,\
            frames = True,\
            forms = True,\
            annoying_tags = True,\
            remove_tags = None,\
            allow_tags = None,\
            kill_tags = None,\
            remove_unknown_tags = True,\
            safe_attrs_only = True,\
            add_nofollow = False,\


"""
 
########################

#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger


import Logger.logger_config as loggerConfig
import Extractor.extractor_config as extractorConfig

#Importe les modules exterieures à l'application
from lxml.html.clean import Cleaner

logger = initLogger.getLogger(extractorConfig.CLEANER_LOGGER_NAME)
#########################

         

class CustomedCleaner_HTML(Cleaner):
   """cleaner de base pour les documents HTML"""

   def __init__(self):
      Cleaner.__init__(self,
            scripts = True,\
            javascript = True,\
            comments = True,\
            style = False,\
            links = True,\
            meta = False,\
            page_structure = True,\
            processing_instructions = True,\
            embedded = True,\
            frames = True,\
            forms = True,\
            annoying_tags = True,\
            remove_tags = None,\
            allow_tags = None,\
            kill_tags = None,\
            remove_unknown_tags = False,\
            safe_attrs_only = False,\
            add_nofollow = False,\
            )

      logger.debug('Cleaner créé')



