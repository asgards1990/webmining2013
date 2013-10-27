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

from Connector.IMDBStatusConnector import *

from FilmExtractor_utils.define_entities import *

import re
import urllib

logger = initLogger.getLogger(IMDBExtractorConfig.IMDB_EXTRACTOR_LOGGER_NAME)

###################################################################

import md5
"""
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
"""

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

   def openFile(self,path):
      try:
         with open(path, 'r') as page:
            logger.debug (" Ouverture du fichier {} réussi " .format(path))
            return page.read()
      except:
         logger.error("Le fichier {} n'existe pas".format(path))
         return None

   def loadPage(self):
      try:
         page = self.openFile(self.path)
         #TODO Travailler l'encodage
         #charset = page.headers.getparam('charset')
         #self.t = unicode(page.read(),charset)
         self.t = page
         return self.t
      except Exception as e:
         logger.error("Le fichier {} ne peut pas être loadé. Error {} : ".format(self.path,e))

   def extractIfExist(self):

      if self.conn.id_exists(self.id_) == 1 :
         return self.conn.getIsDownloaded(self.id_)
      else:
         self.conn.insert(self.id_)
         return False


   def createExtractorEngine(self,boolean):
      if boolean:
         t=self.loadPage()
         cleaner = CustomCleaner.CustomedCleaner_HTML()
         self.extractor = ExtractorHTML(t,cleaner)
      else:
         return False


class IMDBFilmExtractor(IMDBExtractor):

   def __init__(self,film_id):
      IMDBExtractor.__init__(self,film_id)
      self.conn = IMDBFilmStatusConnector()
      boolean = self.extractIfExist()
      self.createExtractorEngine(boolean)
      

class IMDBPersonExtractor(IMDBExtractor):

   def __init__(self,id_):
      IMDBExtractor.__init__(self,id_)
      self.conn = IMDBPersonStatusConnector()
      boolean = self.extractIfExist()
      self.createExtractorEngine(boolean)

class IMDBCompanyExtractor(IMDBExtractor):

   def __init__(self,film_id):
      IMDBExtractor.__init__(self,film_id)
      self.conn = IMDBCompanyStatusConnector()
      boolean = self.extractIfExist()
      self.createExtractorEngine(boolean)

class IMDBExtractor_Film(IMDBFilmExtractor):

   """ Objet qui va récupérer la page HTML principale pour le film en question (une fois que toutes les pages relatives au film sont déjà chargées (Except Personnes/Companies)). Une fois récupérée, les méthodes de l'extracteur récupèrent toutes les infos pour remplir la base
   """

   def __init__(self,film_id):
      logger.debug("Création d'un Extracteur pour un type page de Film")
      self.path = IMDBExtractorConfig.FILM_URL.format(film_id)
      IMDBFilmExtractor.__init__(self,film_id)

      
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

   def extractMetacriticScore(self):
      #Extrait le nombre de personne ayant commenté le film
      logger.debug("Extract metacritic score : ")      
      return self.extractor.extractXpathText('//a[contains(@href,"criticreviews")]')

   def extractStars(self):
      logger.debug("Extract Stars) : ")      
      actor_url_list = self.extractor.extractXpathElement('//a[contains(@href,"tt_ov_st")]/@href')
      return createPersonList(actor_url_list)

   def extractDirectors(self):
      #renvoie une liste de personne
      logger.debug("Extract Directors from main page : ")
      director_url_tab = self.extractor.extractXpathElement('//td[@id="overview-top"]/div[@itemprop="director"]/a/@href')
      return createPersonList(director_url_tab )

   def extractProducerIdFromURLList(p_url_list):
      try:
         p_id_list = [re.match("/company/(co[0-9]+)?", x).group(1) for x in p_url_list if re.match("/company/(co[0-9]+)?",x)]
         logger.debug(p_id_list)
         p_list=[]
      
         for p_id in p_id_list:
            p_list.append(IMDBExtractor_Producer(p_id))

      except Exception as e:
         logger.error("Problème lors de l'extraction des producteurs : {}".format(e))

      return p_list

   def extractProducers(self):

      """renvoie une liste d'objets Producers"""

      logger.debug("Extract Producers from main page: ")
      # Principal producers sur la main page
      p_url_list= self.extractor.extractXpathElement('//span[contains(@itemtype,"Organization") and @itemprop="creator"]/a/@href')
 
      return self.extractProducerIdFromURLList(p_url_list)
      

   def extractLanguage(self):
      logger.debug('Extract Language')
      return self.extractor.extractXpathText('//a[contains(@href,"language")]')

   def extractContent(self):

      self.english_title = (lambda x : x[0] if len(x)>0 else None)(self.extractTitle()) 
      self.original_title = (lambda x : x[0] if len(x)>0 else self.english_title)(self.extractOriginalTitle()) 
      self.release_date = (lambda x : x[0] if len(x)>0 else None)(self.extractReleaseDate())
      self.runtime =(lambda x : x[0].split(' ')[0] if len(x)>0 else None)(self.extractRuntime())
      try:
         self.budget =(lambda x : x[0] if len(x)>0 else None)(self.extractBudget())
      except:
         logger.warning("Pas de Budget décelé pour le film {}".format(self.id_))
         self.budget=None
      try:
         self.box_office =(lambda x : x[0] if len(x)>0 else None)(self.extractBoxOffice())
      except:
         logger.warning("Pas de Box office décelé pour le film {}".format(self.id_))
         self.box_office=None
      try:
         self.imdb_user_rating =(lambda x : x[0] if len(x)>0 else None)(self.extractRatingValue())
      except:
         logger.warning("Pas de User rating décelé pour le film {}".format(self.id_))
         self.imdb_user_rating=None
      try:
         self.imdb_nb_raters =(lambda x : x[0] if len(x)>0 else None)(self.extractRatingCount())
      except:
         logger.warning("Pas de nb rater décelé pour le film {}".format(self.id_))
         self.imdb_user_raters=None
      try: 
         self.imdb_nb_user_review,self.imdb_nb_reviews = self.extractReviewCount() 
      except:
         logger.warning("Pas de nb_user / imdb_nb_review décelé pour le film {}".format(self.id_))
         self.imdb_nb_user_review=None
         self.imdb_nb_reviews = None
      self.imdb_summary = (lambda x : x[0] if len(x)>0 else None)(self.extractSummary())
      self.imdb_storyline = (lambda x : x[0] if len(x)>0 else None)(self.extractStoryLine())
      try :
         self.metacritic_score=(lambda x : int(x[0].split('/')[0]) if len(x)>0 else None)(self.extractMetacriticScore())
      except:
         logger.warning("Pas de score metacritic décelé pour le film {}".format(self.id_))
         self.metacritic_score=None

      #Arrays
      self.country =(self.extractCountry())
      self.genres =(self.extractGenres())
      self.stars =(self.extractStars())
      self.language =(lambda x : x[0] if len(x)>0 else None)(self.extractLanguage())

   def extractFilmPage_DB(self):

      self.extractContent()

      f=defineFilm(self.id_)
      if f:
         try:
            logger.info('Mise à jour de la DB pour le film {} : extraction des données de base du film'.format(self.id_))
            f.original_title=self.original_title
            f.english_title=self.english_title
            f.release_date=self.release_date
            f.runtime=self.runtime
            f.budget=self.budget
            f.box_office=self.box_office
            f.imdb_user_rating=self.imdb_user_rating
            f.imdb_nb_user_ratings = self.imdb_nb_raters.replace(',','')
            f.imdb_nb_user_reviews=self.imdb_nb_user_review.split(' ')[0].replace(',','')
            f.imdb_nb_reviews=self.imdb_nb_reviews.split(' ')[0].replace(',','')
            f.imdb_summary=self.imdb_summary
            f.imdb_storyline=self.imdb_storyline
            f.metacritic_score=self.metacritic_score
            logger.debug("Save")
            f.save()


            for a in self.stars:
              actor = definePerson(a.id_)
              if actor:
                 actor_weight = defineActorWeight(actor,f)
                 if actor_weight:
                    actor_weight.star = True
                    actor_weight.save()

            for c in self.country:
               cc = defineCountry(name=c)
               if cc:
                  f.country.add(cc)  
            for genre in self.genres:
               g = defineGenre(name=genre)
               if g:
                  f.genres.add(g)
            ll = defineLanguage(name=self.language)
            if ll:
               f.language = ll

            logger.debug("Save")
            f.save()

         except Exception as e:
            logger.error("-> The film couldn't be updated:")
            logger.error("-> Error: {}".format(e))

class IMDBExtractor_companyCredits(IMDBFilmExtractor):
   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type companyCredits")
      self.path = IMDBExtractorConfig.COMPANY_CREDITS_URL
      IMDBFilmExtractor.__init__(self,film_id)

   def extractContent(self):
      self.producers = self.extractProducers()

   def extractProducers(self):
      logger.debug("Extract Producers : ")
      p_url_list= self.extractor.extractXpathElement('//a[contains(@href,"ttco_co")]/@href')

      try:
         p_id_list = [re.match("/company/(co[0-9]+)?", x).group(1) for x in p_url_list if re.match("/company/(co[0-9]+)?",x)]
         logger.debug(p_id_list)
         p_list=[]

         for p_id in p_id_list:
            prod = IMDBExtractor_Producer(p_id)
            logger.debug('Extract Producer debug entry id : {} ; name : {} ; country : {}'.format(prod.id_,prod.name,prod.country))
            p_list.append(prod)

      except Exception as e:
         logger.error("Problème lors de l'extraction des producteurs : {}".format(e))

      return p_list

   def extractCompanyCreditsPage_DB(self):
      self.extractContent()
      f = defineFilm(self.id_)
      if f:
         try:
            logger.info('Mise à jour de la DB pour le film {} : extraction des Producteurs'.format(self.id_))
            for p in self.producers:
               producer = defineProducer(p.id_)
               if producer:
                  logger.debug("Producer Name : {} Producer country : {}".format(p.name,p.country))
                  producer.name=p.name
                  c = defineCountryByCode(p.country)
                  if c:
                     producer.country=c

                  f.production_companies.add(producer)
                  producer.save()
            f.save()

         except Exception as e:
            logger.error('La mise à jour de la DB pour le film {} : extraction des Producteurs a échoué'.format(self.id_))
            logger.error("-> Error: {}".format(e))


class IMDBExtractor_Producer(IMDBCompanyExtractor):
   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Producer")
      self.path = IMDBExtractorConfig.PRODUCER_CREDITS_URL
      IMDBCompanyExtractor.__init__(self,id_)
      
   def extractContent(self):
      self.name=self.extractName()
      self.extractCountry()

   def extractName(self):
      try:
         name = self.extractor.extractXpathText('//strong[@class="title"]')[0].split("[")[0][:-1]
         return str(name)
      except:
         logger.error("La page du Producteur n'a pas le format attendu")
         return md5.new("{}".format(self.id_)).hexdigest() 

   def extractCountry(self):
      try:
         self.country = self.extractor.extractXpathText('//strong[@class="title"]')[0].split("[")[1][:-1]
         logger.debug(self.country)
      except:
         logger.error("La page du Producteur n'a pas le format attendu")

class IMDBExtractor_fullCredits(IMDBFilmExtractor):

   """Extracteur pour la page Full Credits"""

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Full credits")
      self.path = IMDBExtractorConfig.FULL_CREDITS_URL
      IMDBFilmExtractor.__init__(self,film_id)

   def extractContent(self):
      self.directors = self.extractDirectors() 
      self.writers = self.extractWriters()
      self.actors =  self.extractActors()


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

 
   def extractFullCreditsPage_DB(self):

      self.extractContent()

      f = defineFilm(self.id_)
      if f:
         try:
            for d in self.directors:
               director = definePerson(d.id_)
               if director:
                  f.directors.add(director)
                  f.save()
            for w in self.writers:
               writer = definePerson(w.id_)
               if writer:
                  f.writers.add(writer)
                  f.save()
            actor_index=1
            for a in self.actors:
              actor = definePerson(a.id_)
              if actor:
                 actor_weight = defineActorWeight(actor,f)
                 if actor_weight:
                    actor_weight.rank = actor_index
                    actor_weight.film = f
                    actor_weight.save()
                    actor_index +=1
            logger.info('Mise à jour de la DB pour le film {} : extraction des Directors / Writers / Actors'.format(self.id_))
         except Exception as e:
            logger.error('La mise à jour de la DB pour le film {} : extraction des Directors / Writers / Actors a échoué'.format(self.id_))
            logger.error("-> Error: {}".format(e))
   

class IMDBExtractor_Reviews(IMDBFilmExtractor):

   """Extracteur pour la page Reviews"""

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Reviews")
      self.path = IMDBExtractorConfig.REVIEWS_URL
      IMDBFilmExtractor.__init__(self,film_id)
      
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

   def extractContent(self):
      self.grade=(self.extractGrade())
      self.summary=(self.extractSummary())
      self.reviewer=(self.extractReviewer())
      self.journal=(self.extractJournal())
      self.fullReviewURL=(self.extractFullReviewURL())

   def extractReviewsPage_DB(self):
      self.extractContent()
      f = defineFilm(self.id_)   
   
      for index in range(len(self.grade)):
        try:
         r = defineReviewer(self.reviewer[index])
         j = defineJournal(self.journal[index])
   
         if r:
            if j:
               if f:
                  re = defineReview(r,j,f)
         if re:
            try:
               logger.info('Mise à jour de la DB pour le film {} : extraction des critiques du film'.format(self.id_))
               re.summary=self.summary[index]
               re.grade=self.grade[index]
               #re.fullReviewURL = self.fullReviewURL[index]
               re.save()
   
            except Exception as e:
               logger.error("-> The rewiew couldn't be updated:")
               logger.error("-> Error: {}".format(e))
        except :
         logger.warning("Problème d'homogénéité dans les tableaux de reviews")
  

class IMDBExtractor_Awards(IMDBFilmExtractor):

   """Extracteur pour la page Awards"""

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Awards")
      self.path = IMDBExtractorConfig.AWARDS_URL
      IMDBFilmExtractor.__init__(self,id_)
      
   def extractAwards(self):
      logger.debug("Extract Awards (à remettre en forme) : ")
      institution_list = self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/h3')#Cannes Film Festival
      #award_list = self.sanitizeList(self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="award_description"]')
      award_category_list=self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="title_award_outcome"]/span[@class="award_category"]')#Palme d'or, oscar...
      award_category_status=self.extractor.extractXpathText('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="title_award_outcome"]/b') #WIN NOMINATED
      award_year_list=self.extractor.extractXpathText('//a[@class="event_year"]')

      logger.debug('Mise en forme des Awards')
      award_tab=[]
      for i in range(1,len(institution_list)+1):
         logger.debug( '########### {}  ##############'.format(institution_list[i-1]) )
         for j in self.extractor.extractXpathElement('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]['+str(i)+']/tr/td[@class="title_award_outcome"]/@rowspan'):
            award_detail = []
            logger.debug(award_category_status[0])
            logger.debug(award_category_list[0])
            logger.debug(award_year_list[i-1])
            logger.debug(j)
           
            award_detail.append(award_category_status[0]) #WIN/NPMINATED
            award_detail.append(award_category_list[0])   #Palme d'or
            award_detail.append(award_year_list[i-1])       #2013
            award_detail.append(institution_list[i-1])     #Cannes Film Festival

	    award_category_status.pop(0)
            award_category_list.pop(0)

         award_tab.append(award_detail)
      return award_tab

   def extractContent(self):
      self.award_tab = self.extractAwards()

   def extractAwardsPage_DB(self):
      self.extractContent()
      f=defineFilm(self.id_)
   
      for award in self.award_tab:
         try:
            win=hasWon(award[0])
            ins = defineInstitution(name=award[3])
            if ins:
               logger.info("Mise à jour du film {}, lien avec un nouvel award pour l'institution {}".format(self.id_,ins))
               Prize.objects.create(win=win, year=int(award[2]), institution=ins, film=f)

         except Exception as e:
            logger.error("-> The film {}  couldn't be updated for the award:".format(self.id_))
            logger.error("-> Error: {}".format(e))


class IMDBExtractor_Keyword(IMDBFilmExtractor):

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Keyword")
      self.path = IMDBExtractorConfig.KEYWORD_URL
      IMDBFilmExtractor.__init__(self,film_id)
      
   def extractContent(self):
      self.keywords = self.extractKeywords() 

   def extractKeywordsPage_DB(self):
      self.extractContent()
      f = defineFilm(self.id_)
      if f:
         try:
            logger.info('Mise à jour de la DB pour le film {} : extraction des keywords'.format(self.id_))
            for word in self.keywords:
               keyword = defineKeyword(word) 
               if keyword:
                  f.keywords.add(keyword)

            f.save()
         except Exception as e:
            logger.error('La mise à jour de la DB pour le film {} : extraction des keywords a échoué'.format(self.id_))
            logger.error("-> Error: {}".format(e))

   def extractKeywords(self):
      return self.extractor.extractXpathText('//td/a')
      

class IMDBExtractor_Person(IMDBPersonExtractor):

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Person")
      self.path = IMDBExtractorConfig.PERSON_URL
      IMDBPersonExtractor.__init__(self,id_)
     

   def extractContent(self):
      self.birthDate = (lambda x : x[0] if len(x)>0 else None)(self.extractBirthDate())
      self.birthCountry = (lambda x : x[-1].split(',')[-1].strip() if len(x)>0 else None)(self.extractBirthCountry())
      self.name = (lambda x : x[0] if len(x)>0 else None)(self.extractName())

   def extractPerson_DB(self):

      self.extractContent()
      p = definePerson(id_)
      if p:
         try: 
            #TODO trouver un moyen pour savoir quand une personne a déjà été updatée pour ne pas l'updater en permanence
            logger.info("Mise à jour de la personne {} dans la base de données".format(id_))
            p.name=self.name
            p.birth_date=self.birthDate
            p.birth_country=defineCountry(self.birthCountry)
            p.save()

         except Exception as e:
            logger.error("-> The actor couldn't be updated:")
            logger.error("-> Error: {}".format(e))


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


