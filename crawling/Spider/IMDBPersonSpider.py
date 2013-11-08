# /usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################

#importe les modules internes

import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import Extractor.superExtractor
from Extractor.extractorHTML import ExtractorHTML
import Extractor.customisedCleaner as CustomCleaner

from Connector.IMDBStatusConnector import IMDBPersonStatusConnector

import spider_config as SpiderConfig

import urllib
from urllib import FancyURLopener

import re

import random

# Logger for this module
logger = initLogger.getLogger(SpiderConfig.IMDB_SPIDER_LOGGER_NAME)


####################################################################

# Custom User-Agent to load IMDB search results

class IMDBSpiderURLopener(FancyURLopener):
    version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"

urllib._urlopener = IMDBSpiderURLopener()

####################################################################

def searchURL(start_pos):
    logger.debug("Compute the url for IMDB search:")

    url = "http://www.imdb.com/search/name?birth_date={0},{1}&count=250&sort=starmeter,asc&start={2}&view=simple".format(1900, 2013, start_pos)
    logger.debug(url)
    return url

####################################################################

class IMDBPersonSearchResultsExtractor:

    def __init__(self, url):
        logger.debug("Create IMDB Person Search Result Extractor")
         
        page = urllib.urlopen(url)
        t = page.read()
        cleaner = CustomCleaner.CustomedCleaner_HTML()
        self.extractor = ExtractorHTML(t,cleaner)
        #logger.debug(self.extractor.cleanString)
        logger.debug("IMDB Person Search Result Extractor created for webpage {} ".format(url))
    
    def extractNumberOfResults(self):
        logger.debug("Extract Number of Search Results")
         
        text = self.extractor.extractXpathText('//div[@id="left"]')[0]
        nb = int(re.findall(r'\d+', text.replace(",", ""))[-1])
        logger.debug("Number of Results: {}".format(nb))
        return nb

    def extractIds(self):
        logger.debug("Extract IMDB ids")

        links = self.extractor.extractXpathElement('//td[@class="name"]//a/@href')
        ids = map(lambda s: re.findall(r'nm\d+', s)[0], links)
        logger.debug("IMDB ids: {}".format(ids))
        return ids
    
    def extractPositions(self):
        logger.debug("Extract positions (priorities)")
        
        labels = self.extractor.extractXpathText('//td[@class="number"]')
        positions = map(lambda s: int(re.findall(r'\d+', s)[0]), labels)
        logger.debug("Positions: {}".format(positions))
        return positions

####################################################################

def insertResults(imdb_ids, priorities):
    logger.debug("Insert priority results into the database")
    
    connector = IMDBPersonStatusConnector()

    for i in range(len(imdb_ids)):
        imdb_id = imdb_ids[i]    
        priority = priorities[i]
        if connector.id_exists(imdb_id):
            logger.debug("Inserting priority result: imdb_id={0} priority={1}".format(imdb_id, priority))
            connector.setPriority(imdb_id, priority)
        else:
            logger.debug("Creating person status")
            connector.insert(imdb_id)
            logger.debug("Inserting priority result: imdb_id={0} priority={1}".format(imdb_id, priority))
            connector.setPriority(imdb_id, priority)

####################################################################

def startSpider():
    logger.debug("Extract all Star IMDB search results")
    
    pos_init = 0

    page_init = 1 # (pos_init - 1) / 250 + 1

    url_init = searchURL(1 + 250 * (page_init - 1))
    extr_init = IMDBPersonSearchResultsExtractor(url_init)
  	
    insertResults(extr_init.extractIds(), extr_init.extractPositions())

    pos_max = extr_init.extractNumberOfResults() # POSITION MAXIMALE A PARSER   
    page_max = (pos_max - 1) / 250 + 1 # PAGE MAXIMALE A PARSER 
    
    for page in range(page_init + 1, page_max + 1):
        url = searchURL(1 + 250 * (page - 1))
        extr = IMDBPersonSearchResultsExtractor(url)
        
        insertResults(extr.extractIds(), extr.extractPositions())

####################################################################

startSpider()
