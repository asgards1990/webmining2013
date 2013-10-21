#! /usr/bin/env python
# -*- coding: latin-1 -*-

## LOGGERS
# Cette classe definit le logger de base

#Import des classes du projet
import logger_config as loggerConfig
import Init.init_config as initConfig
#Import des classes exterieures au projet
import logging


def init_loggers():
    # Crée le logger
    logger = logging.getLogger(loggerConfig.LOGGER_BASE_NAME)
    logger.setLevel (logging.DEBUG)
    logger.propagate = False # Ne remonte pas au root, certains modules pourrissent le logger global

    # Définit le niveau d'output du logger dans le fichier LOG_FILE
    fh = logging.FileHandler(initConfig.RUN_TIME_FOLDER + loggerConfig.LOG_FILE, mode = 'a')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt = '%(asctime)s - %(name)s - %(levelname)s | %(message)s', datefmt = '%d/%m %H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Définit le niveau d'output du logger dans la console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter2 = logging.Formatter(fmt = '%(name)s - %(levelname)s | %(message)s')
    ch.setFormatter(formatter2)
    logger.addHandler(ch)

def getLogger (subLogger):
   return logging.getLogger ('{}.{}'.format(loggerConfig.LOGGER_BASE_NAME, subLogger))

#Lance les loggers
init_loggers()
