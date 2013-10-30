#! /usr/bin/env python
# -*- coding: latin-1 -*-

########################

#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
from Extractor.superExtractor import SuperExtractor #Charge la super classe

import Logger.logger_config as loggerConfig
import Extractor.extractor_config as extractorConfig

#Importe les modules exterieures à l'application
from lxml import etree
from lxml.html.clean import Cleaner
import StringIO

logger = initLogger.getLogger(extractorConfig.EXTRACTOR_HTML_LOGGER_NAME)
#########################




""" La classe ExtractorHTML herite de la classe SuperExtractor. Elle permet de définir les fonctions nécessaire à l'extraction de données dans un document HTML, dont la chaine de caractère est donnée en paramètre de l'objet"""

class ExtractorHTML(SuperExtractor):
   def __init__(self,htmlString,cleaner):
      SuperExtractor.__init__(self,htmlString)
      self.htmlString = self.string.replace("\n","").replace("\r","")

      self.parser = etree.HTMLParser()
      self.cleaner = cleaner
      self.cleanString = self.cleaner.clean_html(self.htmlString)

      #Définit l'arbre sur lequel se feront toutes les XPath extraction
      self.tree = etree.parse(StringIO.StringIO(self.cleanString),self.parser)
      

   def extractXpathElement(self,xpath,caller=None):
      #Retourne un tableau d'éléments extraits
      try :
         e = self.tree.xpath(xpath)
         res = [x.strip() for x in e if len(x.strip())>0]
         if ((len(res) > 0) and (caller == None)) :
            logger.debug(res)
         elif (caller == None):
            logger.warning("L'extraction de l'élément {} est de taille nulle".format(xpath))
         return res

      except Exception as e: 
         logger.error("Erreur dans l'extraction de l'élément {}; Error: {}".format(xpath,e))
         return []

   def extractXpathText(self,xpath):
      s = self.extractXpathElement(xpath+'/text()')
      return [x.strip() for x in s if len(x.strip())>0] 
         
   def extractTitle(self):
      return self.extractXpathText('//title')

   def extractH1(self):
      return self.extractXpathText('//h1')

   def extractH2(self):
      return self.extractXpathText('//h2')

   def extractH3(self):
      return self.extractXpathText('//h3')

   def extractStrong(self):
      return self.extractXpathText('//strong')

   def extractLink(self):
      return self.extractXpathElement('//a/@href') #retourne un tableau de lien, certains absolus, certains relatifs

   def extractLinkContent(self):
      return self.extractXpathText('//a')

   def extractEm(self):
      return self.extractXpathText('//em')
   
   def extractImgAlt(self):
      return self.extractXpathElement('//img/@alt')

   def extractFooters(self):
      pass

   def extractMetaDescription(self):
      return self.extractXpathElement('//meta/@name="description"')


