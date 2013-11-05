# /usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################

#importe les modules internes

import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import Extractor.superExtractor
from Extractor.extractorHTML import ExtractorHTML
import Extractor.customisedCleaner as CustomCleaner

from Connector.IMDBStatusConnector import IMDBFilmStatusConnector

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

def searchURL(year, start_pos):
    logger.debug("Compute the url for IMDB search:")

    url = "http://www.imdb.com/search/title?count=250&release_date={0},{0}&sort=moviemeter,asc&start={1}&title_type=feature&view=simple".format(year, start_pos)
    logger.debug(url)
    return url

####################################################################

class IMDBSearchResultsExtractor:

    def __init__(self, url):
        logger.debug("Create IMDB Search Result Extractor")
         
        page = urllib.urlopen(url)
        t = page.read()
        cleaner = CustomCleaner.CustomedCleaner_HTML()
        self.extractor = ExtractorHTML(t,cleaner)
        #logger.debug(self.extractor.cleanString)
        logger.debug("IMDB Search Result Extractor created for webpage {} ".format(url))
    
    def extractNumberOfResults(self):
        logger.debug("Extract Number of Search Results")
         
        text = self.extractor.extractXpathText('//div[@id="left"]')[0]
        nb = int(re.findall(r'\d+', text.replace(",", ""))[-1])
        logger.debug("Number of Results: {}".format(nb))
        return nb

    def extractIds(self):
        logger.debug("Extract IMDB ids")

        links = self.extractor.extractXpathElement('//td[@class="title"]//a/@href')
        ids = map(lambda s: re.findall(r'tt\d+', s)[0], links)
        logger.debug("IMDB ids: {}".format(ids))
        return ids
    
    def extractPositions(self):
        logger.debug("Extract positions (priorities)")
        
        labels = self.extractor.extractXpathText('//td[@class="number"]')
        positions = map(lambda s: int(re.findall(r'\d+', s)[0]), labels)
        logger.debug("Positions: {}".format(positions))
        return positions

####################################################################

def insertResults(imdb_ids, positions, year):
    logger.debug("Insert priority results into the database")
    
    connector = IMDBFilmStatusConnector()

    for i in range(len(imdb_ids)):
        imdb_id = imdb_ids[i]    
        position = positions[i]
        if connector.id_exists(imdb_id):
            logger.debug("Inserting priority result: imdb_id={0} year={1} priority={2}".format(imdb_id, year, position))
            connector.setFilmPriority(imdb_id, position)

####################################################################

def extractYear(year):
    logger.debug("Extract all IMDB search results for year {}".format(year))
    
    # TODO (pas crucial): OBTENIR POSITION MAXIMALE dans la BDD pour l'année year -> pos_init[year] = 
    pos_init = 0

    # TODO (pas crucial): PAGE MAXIMAL (dans la base de donnée) pour l'année year
    page_init = 1 # (pos_init - 1) / 250 + 1

    url_init = searchURL(year, 1 + 250 * (page_init - 1))
    extr_init = IMDBSearchResultsExtractor(url_init)
  	
    insertResults(extr_init.extractIds(), extr_init.extractPositions(), year)

    pos_max = extr_init.extractNumberOfResults() # POSITION MAXIMALE A PARSER   
    page_max = (pos_max - 1) / 250 + 1 # PAGE MAXIMALE A PARSER 
    
    for page in range(page_init + 1, min(page_max + 1, 5)):
        url = searchURL(year, 1 + 250 * (page - 1))
        extr = IMDBSearchResultsExtractor(url)
        
        insertResults(extr.extractIds(), extr.extractPositions(), year)

####################################################################

def startSpider():
    logger.debug("Start the spider")
    logger.debug("START YEAR: {}".format(SpiderConfig.SPIDER_START_YEAR))
    logger.debug("END YEAR: {}".format(SpiderConfig.SPIDER_END_YEAR))
    years = range(SpiderConfig.SPIDER_START_YEAR, SpiderConfig.SPIDER_END_YEAR + 1)
    random.shuffle(years)
    logger.debug("Years order: {}".format(years))
    for year in years:
        extractYear(year)

startSpider()
