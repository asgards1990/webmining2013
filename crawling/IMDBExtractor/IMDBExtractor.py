# /usr/bin/env python
# -*- coding: latin-1 -*-



####################################################################


#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import IMDBExtractor_config as IMDBExtractorConfig

import Extractor.superExtractor
from Extractor.extractorHTML import ExtractorHTML

import urllib

import Extractor.customisedCleaner as CustomCleaner

logger = initLogger.getLogger(IMDBExtractorConfig.IMDB_EXTRACTOR_LOGGER_NAME)

###################################################################

awards_suffixe = '/awards'
cast_suffixe = '/fullcredits'
companycredits_suffixe = '/companycredits'
keywords_suffixe = '/keywords'
film_page_default = '/title/'
actor_page_default= '/name/'
page_prefixe = 'http://www.imdb.com'
film_id = 'tt1454468'
the_artist_id="tt1655442"

#################################################################


class IMDBExtractor:

   def __init__(self,url):
      
      logger.debug("Création de IMDB Extracteur")
      page = urllib.urlopen(url)
      t = page.read()
      cleaner = CustomCleaner.CustomedCleaner_HTML()
      self.extractor = ExtractorHTML(t,cleaner)
      #logger.debug(self.extractor.cleanString)
      logger.debug("IMDB Extracteur Créé pour la page {} ".format(url))


   def extractTitle(self):
      logger.debug("Extract Title : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/h1[@class="header"]/span[@itemprop="name"]')

   def extractPoster(self):
      logger.debug("Extract Poster : ")
      return self.extractor.extractXpathElement('//td[@id="img_primary"]/*/a/img/@src')

   def extractYear(self):
      logger.debug("Extract Year : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/h1[@class="header"]/span[@class="nobr"]/a')

   def extractReleaseDate(self):
      logger.debug("Extract Release Date : ")
      return self.extractor.extractXpathElement('//td[@id="overview-top"]/div[@class="infobar"]/span[@class="nobr"]/a/meta[@itemprop="datePublished"]/@content')

   def extractDuration(self):
      logger.debug("Extract Duration : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/div[@class="infobar"]/time[@itemprop="duration"]')

   def extractGenre(self):
      logger.debug("Extract Genre : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/div[@class="infobar"]/a/span[@itemprop="genre"]')

   def extractSynopsis(self):
      logger.debug("Extract Synopsis : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/p[@itemprop="description"]')

   def extractStoryLine(self):
      logger.debug("Extract StoryLine  : ")
      return self.extractor.extractXpathText('//div[@class="inline canwrap" and @itemprop="description"]/p')

   def extractKeywords(self):
      logger.debug("Extract keywords : ")
      return self.extractor.extractXpathText('//div[@class="see-more inline canwrap" and @itemprop="keywords"]/a/span')

   def extractDirector(self):
      logger.debug("Extract Directors : ")
      #Main page
      #return self.extractor.extractXpathText('//td[@id="overview-top"]/div[@itemprop="director"]/a/span[@itemprop="name"]')
      #Page fullcredits
      return self.extractor.extractXpathText('//td[@id="overview-top"]/div[@itemprop="director"]/a/span[@itemprop="name"]')

      

   def extractWriter(self):
      logger.debug("Extract Writers : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/div[@itemprop="creator"]/a/span[@itemprop="name"]')

   def extractCountry(self):
      logger.debug("Extract country : ")
      return self.extractor.extractXpathText('//div[@id="titleDetails"]/div/a[contains(@href,"country")]')

   def extractProducers(self):
      logger.debug("Extract Producers : ")
      # Principal producers sur la main page
      #return self.extractor.extractXpathText('//span[contains(@itemtype,"Organization") and @itemprop="creator"]/a/span[@itemprop="name"]')
      return self.extractor.extractXpathText('//div[@class="article listo"]/div[@id="company_credits_content"]/ul[@class="simpleList"][1]/li/a')


   def extractBudget(self):
      logger.debug("Extract Budget : ")
      return self.extractor.extractXpathText('//h4[contains(text(),"Budget")]/parent::*')

   def extractBoxOffice(self):
      logger.debug("Extract BoxOffice : ")
      return self.extractor.extractXpathText('//h4[contains(text(),"Gross")]/parent::*')

   def extractAwards(self):
      logger.debug("Extract Awards (à remettre en forme) : ")
      institution_list = self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/h3')
      #award_list = self.sanitizeList(self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="award_description"]')
      award_category_list=self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="title_award_outcome"]/span[@class="award_category"]')
      award_category_status=self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="title_award_outcome"]/b')

      for i in range(1,len(institution_list)+1):
         print '###########  ' + institution_list[i-1] +'  ##############'
         for j in self.extractor.extractXpathElement('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]['+str(i)+']/tr/td[@class="title_award_outcome"]/@rowspan'):
            print award_category_status[0]
            print award_category_list[0]
            print j
	    award_category_status.pop(0)
            award_category_list.pop(0)

   def extractActors(self):
      logger.debug("Extract Actors : ")
      return self.extractor.extractXpathText('//span[@itemprop="name"]')

   def extractKeywords(self):
      logger.debug("Extract Keywords : ")
      return self.extractor.extractXpathText('//td/a')

   def extractRatingCount(self):
      #Extrait le nombre de personne ayant voté sur le film
      logger.debug("Extract rating count : ")      
      return self.extractor.extractXpathText('//span[@itemprop="ratingCount"]')

   def extractRatingValue(self):
      #Extrait la note moyenne du film
      logger.debug("Extract rating value : ")      
      return self.extractor.extractXpathText('//span[@itemprop="ratingValue"]')

   def extractReviewCount(self):
      #Extrait le nombre de personne ayant commenté le film
      logger.debug("Extract review count (user/critics) : ")      
      return self.extractor.extractXpathText('//span[@itemprop="reviewCount"]')

   def extractBirthDate(self):
      #Extrait le nombre de personne ayant commenté le film
      logger.debug("Extract Actor Birth Date : ")      
      return self.extractor.extractXpathElement('//time[@itemprop="birthDate"]/@datetime')

   def extractBirthCountry(self):
      #Extrait le nombre de personne ayant commenté le film
      logger.debug("Extract Actor Birth Date : ")      
      return self.extractor.extractXpathText('//a[contains(@href,"?birth_place=")]')

#IMDB PAGE

def filmExtract(film_id_):

   #MAIN
   logger.debug('FILM MAIN INFO')
   main_page = IMDBExtractor(page_prefixe+film_page_default+film_id_)

   main_page.extractPoster()
   main_page.extractTitle()
   main_page.extractYear()
   main_page.extractDuration()
   main_page.extractGenre()
   main_page.extractReleaseDate()
   main_page.extractStoryLine()
   main_page.extractCountry()
   main_page.extractBudget()
   main_page.extractBoxOffice()
   main_page.extractDirector()
   main_page.extractWriter()
   main_page.extractRatingCount()
   main_page.extractRatingValue()
   main_page.extractReviewCount()

   #CREDITS
   logger.debug('FILM CREDIT')
   company_credit_page = IMDBExtractor(page_prefixe+film_page_default+film_id_+companycredits_suffixe)
   company_credit_page.extractProducers()

   #IMBD AWARDS
   logger.debug('FILM AWARS')
   exAw = IMDBExtractor(page_prefixe+film_page_default+film_id_+awards_suffixe)
   exAw.extractAwards()

   #IMDB CAST
   logger.debug('FILM CASTING')
   cast_page = IMDBExtractor(page_prefixe+film_page_default+film_id_+cast_suffixe)
   cast_page.extractActors()

   #IMDB KEYWORDS
   logger.debug('IMDB KEYWORDS')
   keyword_page = IMDBExtractor(page_prefixe+film_page_default+film_id_+keywords_suffixe)
   keyword_page.extractKeywords()

   #IMDB CRITICS
   

def actorExtract(actor_id_):
   logger.debug('ACTOR MAIN INFO')
   main_page = IMDBExtractor(page_prefixe+actor_page_default+actor_id_)

   main_page.extractBirthDate()
   main_page.extractBirthCountry()


#filmExtract('tt1454468')
#actorExtract('nm1082477')
actorExtract('nm0000288')
