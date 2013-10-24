# /usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################

#importe les modules internes

import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

from Connector.IMDBStatusConnector import IMDBFilmStatusConnector

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

# Pages PATHs

def filmMainPagePath(imdb_id):
    path = "{0}{1}{2}.html".format(DownloaderConfig.IMDB_FILM_ROOT, DownloaderConfig.IMDB_FILM_MAINPAGE_SUBPATH, imdb_id)
    return path

def filmFullCreditsPath(imdb_id):
    path = "{0}{1}{2}.html".format(DownloaderConfig.IMDB_FILM_ROOT, DownloaderConfig.IMDB_FILM_FULLCREDITS_SUBPATH, imdb_id)
    return path

def filmAwardsPath(imdb_id):
    path = "{0}{1}{2}.html".format(DownloaderConfig.IMDB_FILM_ROOT, DownloaderConfig.IMDB_FILM_AWARDS_SUBPATH, imdb_id)
    return path

def filmReviewsPath(imdb_id):
    path = "{0}{1}{2}.html".format(DownloaderConfig.IMDB_FILM_ROOT, DownloaderConfig.IMDB_FILM_REVIEWS_SUBPATH, imdb_id)
    return path

def filmKeywordsPath(imdb_id):
    path = "{0}{1}{2}.html".format(DownloaderConfig.IMDB_FILM_ROOT, DownloaderConfig.IMDB_FILM_KEYWORDS_SUBPATH, imdb_id)
    return path

def filmCompanyCreditsPath(imdb_id):
    path = "{0}{1}{2}.html".format(DownloaderConfig.IMDB_FILM_ROOT, DownloaderConfig.IMDB_FILM_COMPANYCREDITS_SUBPATH, imdb_id)
    return path

def personPath(imdb_id):
    path = "{0}{1}.html".format(DownloaderConfig.IMDB_PERSON_ROOT, imdb_id)
    return path

def companyPath(imdb_id):
    path = "{0}{1}.html".format(DownloaderConfig.IMDB_COMPANY_ROOT, imdb_id)
    return path

####################################################################

# Page URLs

def filmMainPageURL(imdb_id):
    url = "http://www.imdb.com/title/{0}/".format(imdb_id)
    return url

def filmFullCreditsURL(imdb_id):
    url = "http://www.imdb.com/title/{0}/fullcredits".format(imdb_id) 
    return url

def filmAwardsURL(imdb_id):
    url = "http://www.imdb.com/title/{0}/awards".format(imdb_id)
    return url

def filmReviewsURL(imdb_id):
    url = "http://www.imdb.com/title/{0}/criticreviews".format(imdb_id)
    return url

def filmKeywordsURL(imdb_id):
    url = "http://www.imdb.com/title/{0}/keywords".format(imdb_id)
    return url

def filmCompanyCreditsURL(imdb_id):
    url =  "http://www.imdb.com/title/{0}/companycredits".format(imdb_id)
    return url

def personURL(imdb_id):
    url = "http://www.imdb.com/name/{0}/".format(imdb_id)
    return url

def companyURL(imdb_id):
    url = "http://www.imdb.com/company/{0}/".format(imdb_id) 
    return url

####################################################################

def manageDownloads(downloader, urls, dests, conditions, successCallbacks, errorCallbacks):
    logger.debug("Manage downloads")

    for i in range(len(urls)):
        if conditions[i]:
            if downloader.downloadHTML(urls[i], dests[i]):
                successCallbacks[i]
            else:
               errorCallbacks[i]
        else:
            logger.debug("Download not required")  

####################################################################

class IMDBFilmDownloader:

    def __init__(self):
        self.downloader = Downloader()
        self.failed_requests = []
        self.logger = initLogger.getLogger(DownloaderConfig.IMDB_FILM_DOWNLOADER_LOGGER_NAME)
        self.connector = IMDBFilmStatusConnector()
        self.limit = DownloaderConfig.IMDB_FILM_DOWNLOADER_MAX_REQUESTS_LIMIT
        self.logger.debug("IMDB Film Downloader Created")

    def successCallback(self, imdb_id, msg, setFunction):
        self.logger.debug(msg)
        # TODO: MAJ la base de donnée
    
    def errorCallback(self, imdb_id, msg, setFunction):
        self.logger.warning(msg)
        # TODO: MAJ la base de donnée avec la gestion d'erreur
        # TODO: MAJ de failed_requests


    def downloadFilm(self, imdb_id):
        self.logger.debug("Download pages for the film with id {}".format(imdb_id))

        urls = [filmMainPageURL(imdb_id),]
        dests = [filmMainPagePath(imdb_id),]
        conditions = [self.connector.getFilmMainPageStatus(imdb_id) < self.limit,]
        successCallbacks = [self.successCallback(imdb_id, "Film Page downloaded", lambda x: x),]
        errorCallbacks = [self.errorCallback(imdb_id, "Film Page not downloaded", lambda x: x),]
        
        manageDownloads(self.downloader, urls, dests, conditions, successCallbacks, errorCallbacks)

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

d = IMDBFilmDownloader()

d.downloadFilm("tt3280488")

