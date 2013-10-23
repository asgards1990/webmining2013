# /usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################

#importe les modules internes

import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

from downloader import Downloader
import downloader_config as DownloaderConfig

import urllib
from urllib import FancyURLopener

import re

import random

import os

# Logger for this module
logger = initLogger.getLogger(DownloaderConfig.IMDB_DOWNLOADER_LOGGER_NAME)


####################################################################

def downloadFilmPage(downloader, imdb_id):
    logger.debug("Download the Film Page for film {}".format(imdb_id))

    url = "http://www.imdb.com/title/{0}/".format(imdb_id)

    dest = "testFilmPage.html"
    # TODO: Déterminer le fichier de destination (ATTENTION si ce n'est pas Tiresias ?)
    
    if downloader.downloadHTML(url, dest):
        logger.debug("Film Page downloaded")
        # TODO: MAJ la base de donnée
    else:
        logger.warning("Film Page not downloaded")
        # TODO: MAJ la base de donnée avec la gestion d'erreur

def downloadFilmCast(downloader, imdb_id):
    logger.debug("Download the Film Cast for film {}".format(imdb_id))
    
    url = "http://www.imdb.com/title/{0}/fullcredits".format(imdb_id) 
    dest = "testFilmCast.html"
    # TODO: Déterminer le fichier de destination (ATTENTION si ce n'est pas Tiresias ?)
    
    if downloader.downloadHTML(url, dest):
        logger.debug("Film Page downloaded")
        # TODO: MAJ la base de donnée
    else:
        logger.warning("Film Page not downloaded")
        # TODO: MAJ la base de donnée avec la gestion d'erreur

def downloadFilmAwards(downloader, imdb_id):
    logger.debug("Download the Film Awards for film {}".format(imdb_id))

    url = "http://www.imdb.com/title/{0}/awards".format(imdb_id) 
    dest = "testFilmAwards.html"
    # TODO: Déterminer le fichier de destination (ATTENTION si ce n'est pas Tiresias ?)
    
    if downloader.downloadHTML(url, dest):
        logger.debug("Film Page downloaded")
        # TODO: MAJ la base de donnée
    else:
        logger.warning("Film Page not downloaded")
        # TODO: MAJ la base de donnée avec la gestion d'erreur

def downloadFilmReviews(downloader, imdb_id):
    logger.debug("Download the Film Reviews for film {}".format(imdb_id))

    url = "http://www.imdb.com/title/{0}/criticreviews".format(imdb_id) 
    dest = "testFilmReviews.html"
    # TODO: Déterminer le fichier de destination (ATTENTION si ce n'est pas Tiresias ?)
    
    if downloader.downloadHTML(url, dest):
        logger.debug("Film Page downloaded")
        # TODO: MAJ la base de donnée
    else:
        logger.warning("Film Page not downloaded")
        # TODO: MAJ la base de donnée avec la gestion d'erreur


def downloadFilmKeywords(downloader, imdb_id):
    logger.debug("Download the Film Keywords for film {}".format(imdb_id))

    url = "http://www.imdb.com/title/{0}/keywords".format(imdb_id) 
    dest = "testFilmKeywords.html"
    # TODO: Déterminer le fichier de destination (ATTENTION si ce n'est pas Tiresias ?)
       
    if downloader.downloadHTML(url, dest):
        logger.debug("Film Page downloaded")
        # TODO: MAJ la base de donnée
    else:
        logger.warning("Film Page not downloaded")
        # TODO: MAJ la base de donnée avec la gestion d'erreur


####################################################################

def startDownloader():
    logger.debug("Start the downloader")

    # TODO: Déterminer les pages à télécharger (ordre random, checker si ça a été téléchargé, s'arrêter en cas d'erreur fréquente...)

d = Downloader()

downloadFilmPage(d, 'tt0372784')
downloadFilmCast(d, 'tt0372784')
downloadFilmAwards(d, 'tt0372784')
downloadFilmReviews(d, 'tt0372784')
downloadFilmKeywords(d, 'tt0372784')
