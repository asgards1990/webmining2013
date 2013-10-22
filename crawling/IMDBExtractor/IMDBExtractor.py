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

import re

logger = initLogger.getLogger(IMDBExtractorConfig.IMDB_EXTRACTOR_LOGGER_NAME)

###################################################################

awards_suffixe = '/awards'
cast_suffixe = '/fullcredits'
companycredits_suffixe = '/companycredits'
keywords_suffixe = '/keywords'
film_page_default = '/title/'
actor_page_default= '/name/'
page_prefixe = 'http://www.imdb.com'
film_id_ = 'tt1675434'
the_artist_id="tt1655442"

#################################################################


class IMDBExtractor:
   #TODO voir si on peut actoriser en mettant dans un loader universel
   def __init__(self,id_):
      logger.debug("Création de IMDB Extracteur")
      self.id_=id_

   def loadPage(self,url):
      #TODO : vérifie si la page est déjà en local, sinon charge l'url
      logger.info("La page n'existe pas en locale, chargement de la page {}".format(url))
      page = urllib.urlopen(url)
      t = page.read()
      return t

   def createExtractorEngine(self,url):
      t=self.loadPage(url)
      cleaner = CustomCleaner.CustomedCleaner_HTML()
      self.extractor = ExtractorHTML(t,cleaner)

class IMDBExtractor_Film(IMDBExtractor):

   def __init__(self,film_id):
      logger.debug("Création d'un Extracteur pour un type page de Film")
      IMDBExtractor.__init__(self,film_id)

      self.createExtractorEngine(page_prefixe+film_page_default+film_id)

      self.english_title = self.extractTitle()
      self.original_title = self.extractOriginalTitle()
      self.release_date = self.extractReleaseDate()
      self.runtime = self.extractRuntime()
      self.budget = self.extractBudget()
      self.box_office = self.extractBoxOffice()
      self.imdb_user_rating = self.extractRatingValue()
      self.imdb_nb_raters = self.extractRatingCount()
      self.imdb_nb_user_review,self.imdb_nb_reviews = self.extractReviewCount() 
      self.imdb_summary = self.extractSummary()
      self.imdb_storyline = self.extractStoryLine()
      #TODO metacritic_score = IntegerField(null=True,blank=True)
      #TODO self.image_url = 
      #TODO language = models.ForeignKey(Language, blank=True, null=True, on_delete=models.SET_NULL)
      #TODO country = models.ManyToManyField(Country, related_name="films")
      #TODO genres = models.ManyToManyField(Genre, related_name="films")
      #TODO keywords = models.ManyToManyField(Keyword, related_name="films")
      #TODO production_company = models.ManyToManyField(ProductionCompany, related_name="films")
      self.directors = self.extractDirectors() #models.ManyToManyField(Person, related_name='films') #TODO : check with Django
      #TODO writers = models.ManyToManyField(Person, related_name='films')
      self.actors =  self.extractActors()
      
   def extractTitle(self):
      logger.debug("Extract Title : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/h1[@class="header"]/span[@class="itemprop" and @itemprop="name"]')

   def extractOriginalTitle(self):
      #TODO : s'assurer du user agent
      logger.debug("Extract Original Title : ")
      a=self.extractor.extractXpathText('//td[@id="overview-top"]/h1[@class="header"]/span[@class="title-extra" and @itemprop="name"]') 
      return self.english_title if not a else a

   def extractPoster(self):
      #TODO extraire en local
      logger.debug("Extract Poster : ")
      return self.extractor.extractXpathElement('//td[@id="img_primary"]/*/a/img/@src')

   def extractYear(self):
      logger.debug("Extract Year : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/h1[@class="header"]/span[@class="nobr"]/a')

   def extractReleaseDate(self):
      logger.debug("Extract Release Date : ")
      return self.extractor.extractXpathElement('//td[@id="overview-top"]/div[@class="infobar"]/span[@class="nobr"]/a/meta[@itemprop="datePublished"]/@content')

   def extractRuntime(self):
      logger.debug("Extract Runtime : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/div[@class="infobar"]/time[@itemprop="duration"]')

   def extractGenre(self):
      logger.debug("Extract Genre : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/div[@class="infobar"]/a/span[@itemprop="genre"]')

   def extractSummary(self):
      logger.debug("Extract Synopsis : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/p[@itemprop="description"]')

   def extractStoryLine(self):
      logger.debug("Extract StoryLine  : ")
      return self.extractor.extractXpathText('//div[@class="inline canwrap" and @itemprop="description"]/p')

   def extractWriter(self):
      logger.debug("Extract Writers : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/div[@itemprop="creator"]/a/span[@itemprop="name"]')

   def extractCountry(self):
      logger.debug("Extract country : ")
      return self.extractor.extractXpathText('//div[@id="titleDetails"]/div/a[contains(@href,"country")]')

   def extractBudget(self):
      logger.debug("Extract Budget : ")
      return self.extractor.extractXpathText('//h4[contains(text(),"Budget")]/parent::*')

   def extractBoxOffice(self):
      logger.debug("Extract BoxOffice : ")
      return self.extractor.extractXpathText('//h4[contains(text(),"Gross")]/parent::*')

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

   def extractActors(self):
      #TODO : charge la page des acteurs (1 en local, 2 avecurllib) // extrait les id des acteurs. Pour chaque acteurs on crée un objet IMDBExtract_Person
      logger.debug("Extract Actors : ")
      actor_url_list = self.extractor.extractXpathElement('//td[@itemprop="actor"]/a/@href')
      return self.createPersonList(director_url_tab )

   def createPersonList(self,p_url_list):
      p_id_list = [re.match("/name/(nm[0-9]+)/", x).group(1) for x in p_url_list]
      logger.debug(p_id_list)
      person_list=[]
      for person_id in p_id_list:
         person_list.append(IMDBExtractor_Person(person_id))
      return person_list

   def extractDirectors(self):
      #renvoie une liste de personne
      logger.debug("Extract Directors : ")
      director_url_tab = self.extractor.extractXpathElement('//td[@id="overview-top"]/div[@itemprop="director"]/a/@href')
      return self.createPersonList(director_url_tab )

   def extractProducers(self):
      logger.debug("Extract Producers : ")
      # Principal producers sur la main page
      #return self.extractor.extractXpathText('//span[contains(@itemtype,"Organization") and @itemprop="creator"]/a/span[@itemprop="name"]')
      #TODO : on charge la page du producteur (1- vérif en local; 2 : urllib) pour récupérer les info sur les producteurs
      return self.extractor.extractXpathText('//div[@class="article listo"]/div[@id="company_credits_content"]/ul[@class="simpleList"][1]/li/a')


class IMDBExtractor_Keywords(IMDBExtractor):
   def __init__(self,url):
      #TODO : on charge la page de keyword (1 en local 2 avec urllib) et on crée des objets Keywors
      pass
 
   def extractKeywords(self):
      #TODO : on charge la page de keyword (1 en local 2 avec urllib) et on crée des objets Keywors
      logger.debug("Extract Keywords : ")
      return self.extractor.extractXpathText('//td/a')

class IMDBExtractor_Awards(IMDBExtractor):
   def __init__(self,url):
      #TODO : on charge la page des awards  (1 en local 2 avec urllib) et on remplit les champs de Award 
      pass

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

class IMDBExtractor_Person(IMDBExtractor):

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Person")
      IMDBExtractor.__init__(self,id_)
      self.createExtractorEngine(page_prefixe+actor_page_default+id_)

      self.birthDate = self.extractBirthDate()
      self.birthCountry = self.extractBirthCountry()

   def extractBirthDate(self):
      #Extrait le nombre de personne ayant commenté le film
      logger.debug("Extract Person Birth Date : ")      
      return self.extractor.extractXpathElement('//time[@itemprop="birthDate"]/@datetime')

   def extractBirthCountry(self):
      #Extrait le nombre de personne ayant commenté le film
      logger.debug("Extract Person Birth Country : ")      
      return self.extractor.extractXpathText('//a[contains(@href,"?birth_place=")]')



obj = IMDBExtractor_Film(film_id_)
