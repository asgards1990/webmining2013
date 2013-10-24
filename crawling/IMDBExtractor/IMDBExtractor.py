# /usr/bin/env python
# -*- coding: latin-1 -*-



####################################################################


#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import IMDBExtractor_config as IMDBExtractorConfig

import Extractor.superExtractor
from Extractor.extractorHTML import ExtractorHTML

import Extractor.customisedCleaner as CustomCleaner
from cinema.models import *

import re
import urllib

logger = initLogger.getLogger(IMDBExtractorConfig.IMDB_EXTRACTOR_LOGGER_NAME)

###################################################################

awards_suffixe = '/awards'
fullcredits_suffixe = '/fullcredits'
companycredits_suffixe = '/companycredits'
review_suffixe = '/criticreviews'
keywords_suffixe = '/keywords'
film_page_default = '/title/'
actor_page_default= '/name/'
company_page_default = '/company/'
page_prefixe = 'http://www.imdb.com'
#film_id_ = 'tt1675434'
film_id_='tt2278871'
the_artist_id="tt1655442"

#################################################################


class IMDBExtractor:

   """
      Chaque page nécessite un extractor qui lui est propre : 
          Film 
          Personne (la structure de Actor/Writer/Director est identique) 
          Company 
          Keyword 
          Awards 
          Casting (fullcredits) 
          Producteurs (companycredits / review / )
   """

   #TODO le load page et le create extractor engine ne doivent pas faire partie de IMDB Extractor. IMDB Extractor doit vérifier si la page existe, dans le cas contraire mettre dans le spider qu'il faut télécharger la page! Rien de plus 
   def __init__(self,id_):
      logger.debug("Création de IMDB Extracteur")
      self.id_=id_
      self.url = None

   def loadPage(self,url):
      #TODO : vérifie si la page est déjà en local, sinon charge l'url
      #TODO DOIT DEGAGER!
      logger.info("La page n'existe pas en locale, chargement de la page {}".format(url))
      page = urllib.urlopen(url)
      self.t = page.read()
      return self.t

   def createExtractorEngine(self):
      #TODO DOIT DEGAGER
      t=self.loadPage(self.url)
      cleaner = CustomCleaner.CustomedCleaner_HTML()
      self.extractor = ExtractorHTML(t,cleaner)

class IMDBExtractor_Film(IMDBExtractor):

   """ Objet qui va récupérer la page HTML principale pour le film en question (une fois que toutes les pages relatives au film sont déjà chargées (Except Personnes/Companies)). Une fois récupérée, les méthodes de l'extracteur récupèrent toutes les infos pour remplir la base
   """

   def __init__(self,film_id):
      logger.debug("Création d'un Extracteur pour un type page de Film")
      IMDBExtractor.__init__(self,film_id)
      self.url = page_prefixe+film_page_default+film_id
      self.createExtractorEngine()

      
   def extractTitle(self):
      logger.debug("Extract Title : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/h1[@class="header"]/span[@class="itemprop" and @itemprop="name"]')

   def extractOriginalTitle(self):
      logger.debug("Extract Original Title : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/h1[@class="header"]/span[@class="title-extra" and @itemprop="name"]') 
       

   def extractPoster(self):
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

   def extractGenres(self):
      logger.debug("Extract Genre : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/div[@class="infobar"]/a/span[@itemprop="genre"]')

   def extractSummary(self):
      logger.debug("Extract Synopsis : ")
      return self.extractor.extractXpathText('//td[@id="overview-top"]/p[@itemprop="description"]')

   def extractStoryLine(self):
      logger.debug("Extract StoryLine  : ")
      return self.extractor.extractXpathText('//div[@class="inline canwrap" and @itemprop="description"]/p')

   def extractWriter(self):
      logger.debug("Extract Writers from the main page : ")
      writer_url_list = self.extractor.extractXpathElement('//td[@id="overview-top"]/div[@itemprop="creator"]/a/@href')
      return createPersonList(writer_url_list)

   def extractCountry(self):
      #TODO A REFAIRE ?!?
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

   def extractStars(self):
      logger.debug("Extract Stars) : ")      
      actor_url_list = self.extractor.extractXpathElement('//a[contains(@href,"tt_ov_st")]/@href')
      return createPersonList(actor_url_list)

   def extractDirectors(self):
      #renvoie une liste de personne
      logger.debug("Extract Directors from main page : ")
      director_url_tab = self.extractor.extractXpathElement('//td[@id="overview-top"]/div[@itemprop="director"]/a/@href')
      return createPersonList(director_url_tab )

   def extractProducers(self):
      logger.debug("Extract Producers from main page: ")
      # Principal producers sur la main page
      p_url_list= self.extractor.extractXpathElement('//span[contains(@itemtype,"Organization") and @itemprop="creator"]/a/@href')
      
      #TODO faire attention sur le cas ou la regex ne fonctionne pas! ça fiat planter le programme
      p_id_list = [re.match("/company/(co[0-9]+)?", x).group(1) for x in p_url_list if re.match("/company/(co[0-9]+)?",x)]
      logger.debug(p_id_list)
      p_list=[]
      for p_id in p_id_list:
         p_list.append(IMDBExtractor_Producer(p_id))
      return p_list

   def extractLanguage(self):
      logger.debug('Extract Language')
      return self.extractor.extractXpathText('//a[contains(@href,"language")]')

class IMDBExtractor_companyCredits(IMDBExtractor):
   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type companyCredits")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+film_page_default+id_+companycredits_suffixe
      self.createExtractorEngine()

   def extractProducers(self):
      logger.debug("Extract Producers : ")
      p_url_list= self.extractor.extractXpathElement('//a[contains(@href,"ttco_co")]/@href')

      #TODO faire attention sur le cas ou la regex ne fonctionne pas! ça fiat planter le programme
      p_id_list = [re.match("/company/(co[0-9]+)?", x).group(1) for x in p_url_list if re.match("/company/(co[0-9]+)?",x)]
      logger.debug(p_id_list)
      p_list=[]
      for p_id in p_id_list:
         p_list.append(IMDBExtractor_Producer(p_id))
      return p_list

class IMDBExtractor_Producer(IMDBExtractor):
   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Producer")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+company_page_default+id_
      #TODO vérifie si la page qui nous intéresse existe. Si oui on travaille, si non on insère dans la base la nécessité de charger la page
      
      self.createExtractorEngine()

      self.extractName()
      self.extractCountry()

   def extractName(self):
      #ATTENTION dans les cas où la regex ne fonctionne pas ça fait planter le programme
      try:
         self.name = self.extractor.extractXpathText('//strong[@class="title"]')[0].split("[")[0][:-1]
         logger.debug(self.name)
      except:
         logger.error("La page du Producteur n'a pas le format attendu")

   def extractCountry(self):
      try:
         self.country = self.extractor.extractXpathText('//strong[@class="title"]')[0].split("[")[1][:-1]
         logger.debug(self.country)
      except:
         logger.error("La page du Producteur n'a pas le format attendu")

class IMDBExtractor_fullCredits(IMDBExtractor):

   """Extracteur pour la page Full Credits"""

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Awards")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+film_page_default+id_+fullcredits_suffixe
      self.createExtractorEngine()

   def extractActors(self):
      logger.debug("Extract Actors : ")
      actor_url_list = self.extractor.extractXpathElement('//td[@itemprop="actor"]/a/@href')
      return createPersonList(actor_url_list)

   def extractDirectors(self):
      logger.debug("Extract Diretors : ")
      director_url_list = self.extractor.extractXpathElement('//a[contains(@href,"ttfc_fc_dr")]/@href')
      return createPersonList(director_url_list)

   def extractWriters(self):
      logger.debug("Extract Writers: ")
      writer_url_list = self.extractor.extractXpathElement('//a[contains(@href,"ttfc_fc_wr")]/@href')
      return createPersonList(writer_url_list)

class IMDBExtractor_Reviews(IMDBExtractor):

   """Extracteur pour la page Reviews"""

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Reviews")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+film_page_default+id_+review_suffixe
      self.createExtractorEngine()

   def extractGrade(self):
      logger.debug("Extract Grades : ")
      return self.extractor.extractXpathText('//span[@itemprop="ratingValue"]')

   def extractSummary(self):
      logger.debug("Extract Summaries : ")
      return self.extractor.extractXpathText('//div[@class="summary"]')

   def extractJournal(self):
      logger.debug("Extract Journals : ")
      return self.extractor.extractXpathText('//b[@itemprop="publisher"]/span[@itemprop="name"]')

   def extractReviewer(self):
      logger.debug("Extract Reviewers : ")
      return self.extractor.extractXpathText('//span[@itemprop="author"]/span[@itemprop="name"]')

   def extractFullReviewURL(self):
      logger.debug("Extract Full review URL : ")
      #TODO ne fonctionne pas!?!
      return self.extractor.extractXpathElement('//span[@itemprop="author"]/../@href')

class IMDBExtractor_Awards(IMDBExtractor):

   """Extracteur pour la page Awards"""

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Awards")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+film_page_default+id_+awards_suffixe
      self.createExtractorEngine()

   def extractAwards(self):
      logger.debug("Extract Awards (à remettre en forme) : ")
      institution_list = self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/h3')
      #award_list = self.sanitizeList(self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="award_description"]')
      award_category_list=self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="title_award_outcome"]/span[@class="award_category"]')
      award_category_status=self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="title_award_outcome"]/b')

      logger.debug('Mise en forme des Awards')

      for i in range(1,len(institution_list)+1):
         logger.debug( '########### {}  ##############'.format(institution_list[i-1]) )
         for j in self.extractor.extractXpathElement('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]['+str(i)+']/tr/td[@class="title_award_outcome"]/@rowspan'):
            logger.debug(award_category_status[0])
            logger.debug(award_category_list[0])
            logger.debug(j)
	    award_category_status.pop(0)
            award_category_list.pop(0)

class IMDBExtractor_Keyword(IMDBExtractor):

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Keyword")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+film_page_default+id_+keywords_suffixe
      self.createExtractorEngine()

      self.extractKeywords()

   def extractKeywords(self):
      self.keywords = self.extractor.extractXpathText('//td/a')
      

class IMDBExtractor_Person(IMDBExtractor):

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Person")
      IMDBExtractor.__init__(self,id_)
      self.url =  page_prefixe+actor_page_default+id_
      self.createExtractorEngine()

      self.birthDate = self.extractBirthDate()
      self.birthCountry = self.extractBirthCountry()
      self.Name = self.extractName()

   def extractName(self):
      logger.debug("Extract Person name")
      return self.extractor.extractXpathText('//h1/span[@itemprop="name"]')


   def extractBirthDate(self):
      #Extrait le nombre de personne ayant commenté le film
      logger.debug("Extract Person Birth Date : ")      
      return self.extractor.extractXpathElement('//time[@itemprop="birthDate"]/@datetime')

   def extractBirthCountry(self):
      #Extrait le nombre de personne ayant commenté le film
      logger.debug("Extract Person Birth Country : ")      
      return self.extractor.extractXpathText('//a[contains(@href,"?birth_place=")]')

def createPersonList(p_url_list):
   p_id_list = [ re.match("/name/(nm[0-9]+)/", x).group(1) for x in p_url_list if re.match("/name/(nm[0-9]+)/", x) ]
   logger.debug(p_id_list)
   person_list=[]
   for person_id in p_id_list:
      person_list.append(IMDBExtractor_Person(person_id))
   return person_list


   

def IMDB_filmExtract(film_id):

   filmPage = IMDBExtractor_Film(film_id)      # Sur la main page directement

   english_title = (lambda x : x[0] if len(x)>0 else None)(filmPage.extractTitle())
   original_title = (lambda x : x[0] if len(x)>0 else english_title)(filmPage.extractOriginalTitle()) 
   release_date = (lambda x : x[0] if len(x)>0 else None)(filmPage.extractReleaseDate())
   runtime =(lambda x : x[0] if len(x)>0 else None)(filmPage.extractRuntime())
   budget =(lambda x : x[0] if len(x)>0 else None)(filmPage.extractBudget())
   box_office =(lambda x : x[0] if len(x)>0 else None)(filmPage.extractBoxOffice())
   imdb_user_rating =(lambda x : x[0] if len(x)>0 else None)(filmPage.extractRatingValue())
   imdb_nb_raters =(lambda x : x[0] if len(x)>0 else None)(filmPage.extractRatingCount())
   imdb_nb_user_review,filmPage.imdb_nb_reviews = filmPage.extractReviewCount() 
   imdb_summary = (lambda x : x[0] if len(x)>0 else None)(filmPage.extractSummary())
   imdb_storyline = (lambda x : x[0] if len(x)>0 else None)(filmPage.extractStoryLine())

   #Arrays
   country =(filmPage.extractCountry())
   genres =(filmPage.extractGenres())
   stars =(filmPage.extractStars())
   language =(filmPage.extractLanguage())

   #f = Film.objects.create(original_title="La vie d'Adèle", imdb_id=film_id, release_date="2013-03-05") 

def IMDB_awardsExtract(film_id):
   #sur la page awards
   logger.debug("Lancement de l'extraction des awards")
   awardsPage = IMDBExtractor_Awards(film_id)
   awardsPage.extractAwards()

def IMDB_reviewsExtract(film_id):
   logger.debug("Lancement de l'extraction des reviews")
   reviewPage = IMDBExtractor_Reviews(film_id)
   reviewPage.extractGrade()
   reviewPage.extractSummary()
   reviewPage.extractReviewer()
   reviewPage.extractJournal()
   reviewPage.extractFullReviewURL()
   #TODO extraire le reste

def IMDB_keywordsExtract(film_id):
   #sur la page keywords
   logger.debug("Lancement de l'extraction des keywords")
   keywordsPage = IMDBExtractor_Keyword(film_id)
   keywordsPage.extractKeywords() 

def IMDB_companyCreditsExtractor(film_id):
   #sur la page companycredits
   logger.debug("Lancement de l'extraction des de la page Company Credits")
   companyCreditsPage = IMDBExtractor_companyCredits(film_id)
   companyCreditsPage.extractProducers() #TODO vérifier avant de transmettre à la DB

def IMDB_fullCreditsExtractor(film_id):
   logger.debug("Lancement de l'extraction des de la page full credits")
   fullCreditsPage = IMDBExtractor_fullCredits(film_id)

   directors = fullCreditsPage.extractDirectors() 
   writers = fullCreditsPage.extractWriters()
   #actors =  fullCreditsPage.extractActors()

def IMDB_SuperExtractor(film_id):
   IMDB_filmExtract(film_id) 
   #IMDB_awardsExtract(film_id)
   #IMDB_keywordsExtract(film_id)
   #IMDB_reviewsExtract(film_id)
   #IMDB_fullCreditsExtractor(film_id)
   #IMDB_companyCreditsExtractor(film_id)

###############################################
#                MAIN
###############################################

if __name__=="__main__":
   IMDB_SuperExtractor(film_id_)

IMDB_SuperExtractor(film_id_)
