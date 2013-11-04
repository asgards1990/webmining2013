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

#########################


##########################


## Options Ligne de commande
parser = argparse.ArgumentParser()

#Liste tous les arguments que l'on peut saisir sur la ligne de commandes
parser.add_argument('-fd', '--fresh_debug', dest = 'fresh_debug', help = "Si présent, le fichier de debug est vidé avant l'exécution", action='store_true')
parser.add_argument('-imdb_ex', '--imdb-extractor', dest = 'imdb_extractor', help = "Si présent, lance l'extraction des fichiers HTML en provenace de IMDB", action='store_true')
parser.add_argument('-imdb_sp', '--imdb-spider', dest = 'imdb_spider', help = "Si présent, lance le spider pour IMDB", action='store_true')
parser.add_argument('-imdb_psp', '--imdb-priority-spider', dest = 'imdb_priority_spider', help = "Si présent, lance le spider pour les priorités IMDB", action='store_true')
parser.add_argument('-imdb_fdw', '--imdb-film-downloader', dest = 'imdb_film_downloader', help = "Si présent, lance le downloader des films IMDB", action='store_true')
parser.add_argument('-imdb_pdw', '--imdb-person-downloader', dest = 'imdb_person_downloader', help = "Si présent, lance le downloader des personnes IMDB", action='store_true')
parser.add_argument('-imdb_cdw', '--imdb-company-downloader', dest = 'imdb_company_downloader', help = "Si présent, lance le downloader des entreprises IMDB", action='store_true')
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

if initConfig.args.imdb_spider:
    logger.info ('Lancement du Spider')
    import Spider.IMDBSpider

if initConfig.args.imdb_priority_spider:
    logger.info ('Lancement du Spider de Priorités')
    import Spider.IMDBPrioritySpider

if initConfig.args.imdb_film_downloader:
    logger.info ('Lancement du IMDB Film Downloader')
    import Downloader.IMDBFilmDownloader

if initConfig.args.imdb_person_downloader:
    logger.info ('Lancement du IMDB Person Downloader')
    import Downloader.IMDBPersonDownloader

if initConfig.args.imdb_company_downloader:
    logger.info ('Lancement du IMDB Company Downloader')
    import Downloader.IMDBCompanyDownloader

###############
if initConfig.args.imdb_extractor:
   logger.info("Lancement de l'extracteur IMDB")
   import UserAgent.userAgent
   import FilmExtractor.IMDBExtractor_init 

