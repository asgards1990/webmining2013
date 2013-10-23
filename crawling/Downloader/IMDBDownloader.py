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

# Logger for this module
logger = initLogger.getLogger(DownloaderConfig.DOWNLOADER_LOGGER_NAME)

####################################################################

# Custom User-Agent to load IMDB search results

class IMDBSpiderURLopener(FancyURLopener):
    version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"

urllib._urlopener = IMDBSpiderURLopener()


####################################################################

def checkDownloadedHTML(dest):
    logger.debug("Check the size of downloaded HTML page {}".format(dest))
    
    statinfo = os.stat(dest)
    logger.debug("Size: {}".format(statinfo.st_size))
    
    if (statinfo.st_size > DownloaderConfig.DOWNLOADER_MIN_PAGE_SIZE):
        logger.debug("The html page has a correct size")
        return True
    else:
        logger.warning("The html page has not a correct size")
        return False


def downloadHTML(url, dest):
    logger.debug("Download the HTML page from url {0} to file {1}".format(url, dest))
    
    try:
        logger.debug("Try to download the HTML page")
        u = urllib.urlopen(url)
    except IOError as e:
        logger.error(url)
        logger.error('We failed to reach a server or the server couldn\'t fulfill the request.')
        logger.error('Error: {}'.format(e.errno))
        logger.error('Reason: {}'.format(e.strerror))
        return False        
    else:
        f = open(dest, 'wb')
        f.write(u.read())
        f.close()
        u.close()
        logger.debug("HTML page downloaded")
        
        if checkDownloadedHTML(dest):
            return True
        else:
            logger.warning("Deleting the downloaded HTML page")
            os.remove(dest)
            return False

####################################################################

def downloadFilmPage(imdb_id):
    logger.debug("Download the Film Page for film {}".format(imdb_id))

def downloadFilmCast(imdb_id):
    logger.debug("Download the Film Cast for film {}".format(imdb_id))

def downloadFilmAwards(imdb_id):
    logger.debug("Download the Film Awards for film {}".format(imdb_id))

def downloadFilmReviews(imdb_id):
    logger.debug("Download the Film Reviews for film {}".format(imdb_id))

def downloadFilmKeywords(imdb_id):
    logger.debug("Download the Film Keywords for film {}".format(imdb_id))

####################################################################

def startDownloader():
    logger.debug("Start the downloader")

url = "http://www.imdb.com/title/tt0203259/"
dest = "test.html"

downloadHTML(url, dest)

