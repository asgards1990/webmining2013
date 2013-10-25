#! /usr/bin/env python
# -*- coding: latin-1 -*-


""" Point d'entrée """

########################

#importe les modules internes
import Logger.init_logger as initLogger

import Init.init_config as initConfig
import Logger.logger_config as loggerConfig

#Importe les modules exterieures à l'application
import argparse
import os

#########################

def exportSettings():
   os.system(initConfig.DJANGO_SETTINGS_MODULE)
   os.system(initConfig.PYTHONPATH)

##########################


## Options Ligne de commande
parser = argparse.ArgumentParser()

#Liste tous les arguments que l'on peut saisir sur la ligne de commandes
parser.add_argument('-fd', '--fresh_debug', dest = 'fresh_debug', help = "Si présent, le fichier de debug est vidé avant l'exécution", action='store_true')
parser.add_argument('-imdb_ex', '--imdb-extractor', dest = 'imdb_extractor', help = "Si présent, lance l'extraction des fichiers HTML en provenace de IMDB", action='store_true')
parser.add_argument('-s', '--spider', dest = 'spider', help = "Si présent, lance le spider", action='store_true')
parser.add_argument('-d', '--downloader', dest = 'downloader', help = "Si présent, lance le downloader", action='store_true')
#Crée le tableau global qui donne accès aux arguments passés en paramètres sur la ligne de commande
initConfig.args = parser.parse_args()

##########
# Crée les loggers & co
logger = initLogger.getLogger (initConfig.SCRAPER_INIT_LOGGER_NAME)
logger.debug('Logger {} créé'.format(initConfig.SCRAPER_INIT_LOGGER_NAME))

#################
# Vide le fichier de log si demandé
debug_file = initConfig.RUN_TIME_FOLDER + loggerConfig.LOG_FILE
if initConfig.args.fresh_debug:
    logger.info ('Vide le fichier {}...'.format(debug_file))
    open(debug_file, 'w').close()

if initConfig.args.spider:
    logger.info ('Lancement du Spider')
    import Spider.IMDBSpider

if initConfig.args.downloader:
    logger.info ('Lancement du Downloader')
    import Downloader.IMDBDownloader

###############
if initConfig.args.imdb_extractor:
   exportSettings()
   import UserAgent.userAgent
   import IMDBExtractor.IMDBExtractor


