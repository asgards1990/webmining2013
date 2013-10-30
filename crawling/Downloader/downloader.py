# /usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################

#importe les modules internes

import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import downloader_config as DownloaderConfig

import urllib
from urllib import FancyURLopener

import re

import random

import os

####################################################################

# Custom User-Agent to load IMDB search results

class IMDBSpiderURLopener(FancyURLopener):
    version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"


####################################################################

class Downloader:
    
    def __init__(self):
        # Logger
        self.logger = initLogger.getLogger(DownloaderConfig.DOWNLOADER_LOGGER_NAME)
        urllib._urlopener = IMDBSpiderURLopener()

    def checkDownloadedHTML(self, dest):
        self.logger.debug("Check the size of downloaded HTML page {}".format(dest))
    
        statinfo = os.stat(dest)
        self.logger.debug("Size: {}".format(statinfo.st_size))
    
        if (statinfo.st_size > DownloaderConfig.DOWNLOADER_MIN_PAGE_SIZE):
            self.logger.debug("The html page has a correct size")
            return True
        else:
            self.logger.warning("The html page has not a correct size")
            return False


    def checkHTTPStatus(self, u):
        self.logger.debug("Check HTTP status of page {}".format(u.geturl()))

        if u.getcode() == 200:
            self.logger.debug("Status code 200 - The request has suceeded")
            return True
        else:
            self.logger.warning("Status code {} - There can be a problem with the request".format(u.getcode()))
            return False
    
    def downloadHTML(self, url, dest):
        self.logger.debug("Download the HTML page from url {0} to file {1}".format(url, dest))
        
        try:
            self.logger.debug("Try to download the HTML page")
            u = urllib.urlopen(url)
        except IOError as e:
            self.logger.warning(url)
            self.logger.warning('We failed to reach a server or the server couldn\'t fulfill the request.')
            self.logger.warning('Error: {}'.format(e.errno))
            self.logger.warning('Reason: {}'.format(e.strerror))
            return False

        try:
            r = u.read()
        except Exception as e:
            self.logger.warning('We failed to read the page')
            self.logger.warning('Error: {}'.format(e))
            return False
        
        if not self.checkHTTPStatus(u):
            u.close()
            return False
           
        try:
            f = open(dest, 'wb')
            f.write(r)
        except Exception as e:
            self.logger.warning('We failed to write the page')
            self.logger.warning('Error: {}'.format(e))
            return False

        f.close()
        u.close()
        self.logger.debug("HTML page downloaded")

        if self.checkDownloadedHTML(dest):
            return True
        else:
            self.logger.warning("Deleting the downloaded HTML page")
            os.remove(dest)
            return False
 
    def manageDownloads(self, urls, dests, stop_limits, required_limits, getFunctions, setFunctions):
        self.logger.debug("Manage downloads")

        for i in range(len(urls)):
            status = getFunctions[i]() 
            if status < stop_limits[i]:
                if self.downloadHTML(urls[i], dests[i]):
                    self.logger.debug("{} downloaded".format(urls[i]))
                    setFunctions[i](100) 
                else:
                    self.logger.debug("{} not downloaded".format(urls[i]))
                    setFunctions[i](status + 1)
                    return False
            else:
                if status < required_limits[i]:
                    self.logger.warning("Download required!")
                    return False
                else:
                    self.logger.debug("Download not required")
        return True

