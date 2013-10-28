# /usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################

#importe les modules internes

import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

from Connector.IMDBStatusConnector import IMDBCompanyStatusConnector

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

def companyPath(imdb_id):
    path = "{0}{1}.html".format(DownloaderConfig.IMDB_COMPANY_ROOT, imdb_id)
    return path

####################################################################

# Page URLs

def companyURL(imdb_id):
    url = "http://www.imdb.com/company/{0}/".format(imdb_id)
    return url

####################################################################

class IMDBCompanyDownloader:

    def __init__(self):
        self.downloader = Downloader()
        self.failed_requests = 0
        self.logger = initLogger.getLogger(DownloaderConfig.IMDB_COMPANY_DOWNLOADER_LOGGER_NAME)
        self.connector = IMDBCompanyStatusConnector()
        self.onepage_limit = DownloaderConfig.IMDB_COMPANY_DOWNLOADER_ONEPAGE_REQUESTS_LIMIT
        self.global_limit = DownloaderConfig.IMDB_COMPANY_DOWNLOADER_GLOBAL_REQUESTS_LIMIT
        self.logger.debug("IMDB Company Downloader Created")

    def downloadCompany(self, imdb_id):
        self.logger.debug("Download pages for the company with id {}".format(imdb_id))

        urls = [
            companyURL(imdb_id),
            ]
        dests = [
            companyPath(imdb_id),
            ]
        getFunctions = [
            lambda: self.connector.getDownloadedStatus(imdb_id),
            ]
        setFunctions = [
            lambda s: s
            ]
        stop_limits = [1,] 
        required_limits = [1,]
        
        if self.downloader.manageDownloads(urls, dests, stop_limits, required_limits, getFunctions, setFunctions):
            self.connector.setDownloadedStatus(imdb_id, 1)
        else:
            self.failed_requests += 1
            

    def start(self):
        self.logger.debug("Start the IMDB Company Downloader")
        while self.failed_requests < self.global_limit:
            imdb_ids = self.connector.getNotDownloaded()
            try:
                imdb_id = random.choice(imdb_ids)
            except IndexError as e:
                self.logger.debug("Nothing to download")
                return
            else:
                self.downloadCompany(imdb_id)
        self.logger.error("The total number of requests cannot exceed {}".format(self.global_limit))
        self.logger.error("Stopping the downloader")
            
####################################################################

d = IMDBCompanyDownloader()

d.start()

