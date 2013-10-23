# /usr/bin/env python
# -*- coding: utf-8 -*-



####################################################################

#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import spider_config as SpiderConfig

import Extractor.superExtractor
from Extractor.extractorHTML import ExtractorHTML

import urllib
from urllib import FancyURLopener

import Extractor.customisedCleaner as CustomCleaner

logger = initLogger.getLogger(SpiderConfig.SPIDER_LOGGER_NAME)


####################################################################

class IMDBSpiderURLopener(FancyURLopener):
    version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"

urllib._urlopener = IMDBSpiderURLopener()

####################################################################

def search_url(year, start_pos):
    logger.debug("Compute the url for IMDB search:")

    url = "http://www.imdb.com/search/title?count=250&release_date=" + str(year) + "," + str(year) + "&sort=release_date_us,asc&start=" + str(start_pos) + "&title_tyearpe=feature,documentary&view=simple"
    logger.debug(url)
    return url

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
        logger.debug("Extract Number of Search Results:")
        return self.extractor.extractXpathText('//div[@id="left"]')

    def extractURLs(self):
        logger.debug("Extract IMDB ids:")
        return self.extractor.extractXpathText('//td[@class="title"]')
    
    def extractPositions(self):
        logger.debug("Extract positions:")
        return self.extractor.extractXpathText('//td[@class="number"]')

def process_page(page, year):
    logger.debug("Extract IDs from search results:")

    urls = page.xpath('//td[@class="title"]/a/@href')
    positions = page.xpath('//td[@class="number"]')
    
    for i in range(len(urls)):
        url = urls[i]
        imdb_id='tt' + regexp(r'd+',url)    
        
        # TODO: METTRE dans Imdb_status (imdb_id, year, position, 0, 0, 0, 0, 0, -1)

url = search_url(1999,1000)

extractor = IMDBSearchResultsExtractor(url)
extractor.extractNumberOfResults()
extractor.extractIMDBIds()
extractor.extractPositions()

