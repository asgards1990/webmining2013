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

# Pages local PATHs

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

def manageDownloads(downloader, urls, dests, stop_limits, required_limits, getFunctions, setFunctions):
    logger.debug("Manage downloads")

    for i in range(len(urls)):
        status = getFunctions[i]() 
        if status < stop_limits[i]:
            if downloader.downloadHTML(urls[i], dests[i]):
                logger.debug("{} downloaded".format(urls[i]))
                setFunctions[i](100) 
            else:
                logger.debug("{} not downloaded".format(urls[i]))
                setFunctions[i](status + 1)
                return False
        else:
            if status < required_limits[i]:
                logger.warning("Download required!")
                return False
            else:
                logger.debug("Download not required")
    return True

####################################################################

class IMDBFilmDownloader:

    def __init__(self):
        self.downloader = Downloader()
        self.failed_requests = 0
        self.logger = initLogger.getLogger(DownloaderConfig.IMDB_FILM_DOWNLOADER_LOGGER_NAME)
        self.connector = IMDBFilmStatusConnector()
        self.onepage_limit = DownloaderConfig.IMDB_FILM_DOWNLOADER_ONEPAGE_REQUESTS_LIMIT
        self.global_limit = DownloaderConfig.IMDB_FILM_DOWNLOADER_GLOBAL_REQUESTS_LIMIT
        self.logger.debug("IMDB Film Downloader Created")

    def downloadFilm(self, imdb_id):
        self.logger.debug("Download pages for the film with id {}".format(imdb_id))

        urls = [
            filmMainPageURL(imdb_id),
            filmFullCreditsURL(imdb_id),
            filmAwardsURL(imdb_id),
            filmReviewsURL(imdb_id),
            filmKeywordsURL(imdb_id),
            filmCompanyCreditsURL(imdb_id),
            ]
        dests = [
            filmMainPagePath(imdb_id),
            filmFullCreditsPath(imdb_id),
            filmAwardsPath(imdb_id),
            filmReviewsPath(imdb_id),
            filmKeywordsPath(imdb_id),
            filmCompanyCreditsPath(imdb_id),
            ]
        getFunctions = [
            lambda: self.connector.getFilmMainPageStatus(imdb_id),
            lambda: self.connector.getFilmFullCreditsStatus(imdb_id),
            lambda: self.connector.getFilmAwardsStatus(imdb_id),
            lambda: self.connector.getFilmReviewsStatus(imdb_id),
            lambda: self.connector.getFilmKeywordsStatus(imdb_id),
            lambda: self.connector.getFilmCompanyCreditsStatus(imdb_id),
            ]
        setFunctions = [
            lambda s: self.connector.setFilmMainPageStatus(imdb_id, s),
            lambda s: self.connector.setFilmFullCreditsStatus(imdb_id, s),
            lambda s: self.connector.setFilmAwardsStatus(imdb_id, s),
            lambda s: self.connector.setFilmReviewsStatus(imdb_id, s),
            lambda s: self.connector.setFilmKeywordsStatus(imdb_id, s),
            lambda s: self.connector.setFilmCompanyCreditsStatus(imdb_id, s),
            ]
        stop_limits = [self.onepage_limit, self.onepage_limit, self.onepage_limit, self.onepage_limit, self.onepage_limit, self.onepage_limit,]
        required_limits = [100, self.onepage_limit, self.onepage_limit, self.onepage_limit, self.onepage_limit, self.onepage_limit,]
        
        if manageDownloads(self.downloader, urls, dests, stop_limits, required_limits, getFunctions, setFunctions):
            self.connector.setDownloadedStatus(imdb_id, 1)
        else:
            self.failed_requests += 1
            

    def start(self):
        self.logger.debug("Start the IMDB Film Downloader")
        while self.failed_requests < self.global_limit:
            imdb_ids = self.connector.getNotDownloaded()
            try:
                imdb_id = random.choice(imdb_ids)
            except IndexError as e:
                self.logger.debug("Nothing to download")
                return
            else:
                self.downloadFilm(imdb_id)
        self.logger.error("The total number of requests cannot exceed {}".format(self.global_limit))
        self.logger.error("Stopping the downloader")
            
####################################################################

class IMDBPersonDownloader:

    def __init__(self):
        self.downloader = Downloader()
        self.failed_requests = 0
        self.logger = initLogger.getLogger(DownloaderConfig.IMDB_PERSON_DOWNLOADER_LOGGER_NAME)
        self.connector = IMDBPersonStatusConnector()
        self.onepage_limit = DownloaderConfig.IMDB_PERSON_DOWNLOADER_ONEPAGE_REQUESTS_LIMIT
        self.global_limit = DownloaderConfig.IMDB_PERSON_DOWNLOADER_GLOBAL_REQUESTS_LIMIT
        self.logger.debug("IMDB Person Downloader Created")

    def downloadPerson(self, imdb_id):
        self.logger.debug("Download pages for the person with id {}".format(imdb_id))

        urls = [
            filmPersonURL(imdb_id),
            ]
        dests = [
            filmPersonPath(imdb_id),
            ]
        getFunctions = [
            lambda: self.connector.getDownloadedStatus(imdb_id),
            ]
        setFunctions = [
            lambda s: pass
            ]
        stop_limits = [1,] 
        required_limits = [1,]
        
        if manageDownloads(self.downloader, urls, dests, stop_limits, required_limits, getFunctions, setFunctions):
            self.connector.setDownloadedStatus(imdb_id, 1)
        else:
            self.failed_requests += 1
            

    def start(self):
        self.logger.debug("Start the IMDB Person Downloader")
        while self.failed_requests < self.global_limit:
            imdb_ids = self.connector.getNotDownloaded()
            try:
                imdb_id = random.choice(imdb_ids)
            except IndexError as e:
                self.logger.debug("Nothing to download")
                return
            else:
                self.downloadPerson(imdb_id)
        self.logger.error("The total number of requests cannot exceed {}".format(self.global_limit))
        self.logger.error("Stopping the downloader")
            
####################################################################

d = IMDBFilmDownloader()

d.start()

