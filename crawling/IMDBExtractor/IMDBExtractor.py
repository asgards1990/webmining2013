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

import md5

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
      logger.info("La page n'existe pas en local, chargement de la page {}".format(url))
      page = urllib.urlopen(url)
      charset = page.headers.getparam('charset')
      self.t = unicode(page.read(),charset)
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
      self.url = page_prefixe+film_page_default+self.id_
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

   def extractProducers(self):
      logger.debug("Extract Producers from main page: ")
      # Principal producers sur la main page
      p_url_list= self.extractor.extractXpathElement('//span[contains(@itemtype,"Organization") and @itemprop="creator"]/a/@href')
      
      try:
         p_id_list = [re.match("/company/(co[0-9]+)?", x).group(1) for x in p_url_list if re.match("/company/(co[0-9]+)?",x)]
         logger.debug(p_id_list)
         p_list=[]
      
         for p_id in p_id_list:
            p_list.append(IMDBExtractor_Producer(p_id))

      except Exception as e:
         logger.error("Problème lors de l'extraction des producteurs : {}".format(e))

      return p_list

   def extractLanguage(self):
      logger.debug('Extract Language')
      return self.extractor.extractXpathText('//a[contains(@href,"language")]')

   def extractContent(self):

      self.english_title = (lambda x : x[0] if len(x)>0 else None)(self.extractTitle()) 
      self.original_title = (lambda x : x[0] if len(x)>0 else self.english_title)(self.extractOriginalTitle()) 
      self.release_date = (lambda x : x[0] if len(x)>0 else None)(self.extractReleaseDate())
      self.runtime =(lambda x : x[0].split(' ')[0] if len(x)>0 else None)(self.extractRuntime())
      self.budget =(lambda x : x[0] if len(x)>0 else None)(self.extractBudget())
      self.box_office =(lambda x : x[0] if len(x)>0 else None)(self.extractBoxOffice())
      self.imdb_user_rating =(lambda x : x[0] if len(x)>0 else None)(self.extractRatingValue())
      self.imdb_nb_raters =(lambda x : x[0] if len(x)>0 else None)(self.extractRatingCount())
      self.imdb_nb_user_review,imdb_nb_reviews = self.extractReviewCount() 
      self.imdb_summary = (lambda x : x[0] if len(x)>0 else None)(self.extractSummary())
      self.imdb_storyline = (lambda x : x[0] if len(x)>0 else None)(self.extractStoryLine())
      self.metacritic_score=(lambda x : int(x[0].split('/')[0]) if len(x)>0 else None)(self.extractMetacriticScore())

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
          
            for c in self.country:
               cc = defineCountry(name=c)
               if cc:
                  f.country.add(cc)  
            for genre in self.genres:
               g = defineGenre(name=genre)
               if g:
                  f.genres.add(g)
            ll = defineLanguage(name=language)
            if ll:
               f.language = ll

            logger.debug("Save")
            f.save()

         except Exception as e:
            logger.error("-> The film couldn't be updated:")
            logger.error("-> Error: {}".format(e))

class IMDBExtractor_companyCredits(IMDBExtractor):
   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type companyCredits")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+film_page_default+id_+companycredits_suffixe
      self.createExtractorEngine()

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


class IMDBExtractor_Producer(IMDBExtractor):
   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Producer")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+company_page_default+id_
      
      self.createExtractorEngine()

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

class IMDBExtractor_fullCredits(IMDBExtractor):

   """Extracteur pour la page Full Credits"""

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Full credits")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+film_page_default+id_+fullcredits_suffixe
      self.createExtractorEngine()

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
            for a in self.actors:
              actor = definePerson(a.id_)
              if actor:
                 pass
                 #f.actors.add(actor)
                 #TODO
            logger.info('Mise à jour de la DB pour le film {} : extraction des Directors / Writers / Actors'.format(self.id_))
         except Exception as e:
            logger.error('La mise à jour de la DB pour le film {} : extraction des Directors / Writers / Actors a échoué'.format(self.id_))
            logger.error("-> Error: {}".format(e))
   

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
  

class IMDBExtractor_Awards(IMDBExtractor):

   """Extracteur pour la page Awards"""

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Awards")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+film_page_default+id_+awards_suffixe
      self.createExtractorEngine()

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


class IMDBExtractor_Keyword(IMDBExtractor):

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Keyword")
      IMDBExtractor.__init__(self,id_)
      self.url = page_prefixe+film_page_default+id_+keywords_suffixe
      self.createExtractorEngine()

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
      

class IMDBExtractor_Person(IMDBExtractor):

   def __init__(self,id_):
      logger.debug("Création d'un Extracteur pour un type Person")
      IMDBExtractor.__init__(self,id_)
      self.url =  page_prefixe+actor_page_default+id_
      self.createExtractorEngine()

      self.birthDate = (lambda x : x[0] if len(x)>0 else None)(self.extractBirthDate())
      self.birthCountry = (lambda x : x[-1].split(',')[-1].strip() if len(x)>0 else None)(self.extractBirthCountry())
      self.name = (lambda x : x[0] if len(x)>0 else None)(self.extractName())

   def extractPerson_DB(self):

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


##########################################################
#
#                    DEFINE FAMILY
#
##########################################################

"""Crée/Renvoie les objects pour intéragir avec la base de données Django."""

def defineFilm(film_id):
    try :
      f = Film.objects.get(imdb_id=film_id)
      return f
    except Film.DoesNotExist :
      logger.info("Création du film avec l'id {} dans la base de données".format(film_id))
      f = Film.objects.create(imdb_id=film_id)
      return f
    except Exception as e:
      logger.error('Impossible de retrouver le film {} a cause de l erreur {}'.format(film_id,e))
      return False

def defineKeyword(keyword):
    try :
      w = Keyword.objects.get(word=keyword)
      return w
    except Keyword.DoesNotExist :
      logger.info("Création du keyword {} dans la base de données".format(keyword))
      w = Keyword.objects.create(word=keyword)
      return w
    except Exception as e:
      logger.error('Impossible de retrouver le keyword {} a cause de l erreur {}'.format(keyword,e))
      return False
 
def defineReview(reviewer,journal,film):
   try :
      r = Review.objects.get(reviewer=reviewer,journal=journal,film=film)
      return False 
   except Review.DoesNotExist :
      logger.info("Création de la review dans la base de données")
      r = Review.objects.create(reviewer=reviewer,journal=journal,film=film)
      return r
   except Exception as e:
      logger.error('Impossible de retrouver la review a cause de l erreur {}'.format(e))
      return False

def definePerson(p_id):
   try :
      p = Person.objects.get(imdb_id=p_id)
      return p 
   except Person.DoesNotExist :
      logger.info("Création de la personne {} dans la base de données".format(p_id))
      p = Person.objects.create(imdb_id=p_id)
      return p
   except Exception as e:
      logger.error('Impossible de retrouver la personne {} a cause de l erreur {}'.format(p_id,e))
      return False

def defineJournal(j_name):
   try :
      j = Journal.objects.get(name=j_name)
      return j
   except Journal.DoesNotExist :
      logger.info("Création du journal {} dans la base de données".format(j_name))
      j = Journal.objects.create(name=j_name)
      return j
   except Exception as e:
      logger.error('Impossible de retrouver le journal {} a cause de l erreur {}'.format(j_name,e))
      return False

def defineProducer(p_id):
   try :
      p = ProductionCompany.objects.get(imdb_id=p_id)
      return p
   except ProductionCompany.DoesNotExist :
      logger.info("Création du producteur {} dans la base de données".format(p_id))
      p = ProductionCompany.objects.create(imdb_id=p_id)
      return p
   except Exception as e:
      logger.error('Impossible de retrouver le producteur {} a cause de l erreur {}'.format(p_id,e))
      return False

def defineReviewer(name):
   try :
      r = Reviewer.objects.get(name=name)
      return r
   except Reviewer.DoesNotExist :
      logger.info("Création du reviewer {} dans la base de données".format(name))
      r = Reviewer.objects.create(name=name)
      return r
   except Exception as e:
      logger.error('Impossible de retrouver le reviewer {} a cause de l erreur {}'.format(name,e))
      return False

def defineInstitution(name):
   try :
      i = Institution.objects.get(name=name)
      return i
   except Institution.DoesNotExist :
      logger.info("Création de l'institution {} dans la base de données".format(name))
      i = Institution.objects.create(name=name)
      return i
   except Exception as e:
      logger.error('Impossible de retrouver l institution {} a cause de l erreur {}'.format(name,e))
      return False

def defineCountry(name):
   try :
      r = Country.objects.get(name=name)
      return r
   except Country.DoesNotExist :
      logger.warning("Le pays {} n'a pas été trouvé dans la base de données".format(name))
      return None
   except Exception as e:
      logger.error('Impossible de retrouver le pays {} a cause de l erreur {}'.format(name,e))
      return False

def defineCountryByCode(code):
   try :
      r = Country.objects.get(identifier=code)
      return r
   except Country.DoesNotExist :
      logger.warning("Le pays dont le code est {} n'a pas été trouvé dans la base de données".format(code))
      return None
   except Exception as e:
      logger.error('Impossible de retrouver le pays {} a cause de l erreur {}'.format(code,e))
      return False

def defineGenre(name):
   try :
      r = Genre.objects.get(name=name)
      return r
   except Genre.DoesNotExist :
      logger.warning("Le genre {} n'a pas été trouvé dans la base de données".format(name))
      return None
   except Exception as e:
      logger.error('Impossible de retrouver le genre {} a cause de l erreur {}'.format(name,e))
      return False

def defineLanguage(name):
   try :
      r = Language.objects.get(name=name)
      return r
   except Language.DoesNotExist :
      logger.warning("Le langage {} n'a pas été trouvé dans la base de données".format(name))
      return None
   except Exception as e:
      logger.error('Impossible de retrouver le langage {} a cause de l erreur {}'.format(name,e))
      return False



################################################################
#
#                        IMDB_*Extract Family
#
##################################################################

""" Fonctions appelées depuis l'exterieur du module. Créent les objets nécessaires à l'extraction et remplissent la DB. Il existe une fonction par type de page"""

def IMDB_filmExtract(film_id):
   logger.debug("Lancement de l'extraction de la Page film pour le film {}".format(film_id))
   filmPage = IMDBExtractor_Film(film_id)      # Sur la main page directement

   filmPage.extractFilmPage_DB()


def IMDB_awardsExtract(film_id):
   #sur la page awards
   logger.debug("Lancement de l'extraction des awards pour le film {}".format(film_id))
   awardsPage = IMDBExtractor_Awards(film_id)

   awardsPage.extractAwardsPage_DB()


def hasWon(status):
   return True if status.upper()=="WON" else False

def IMDB_reviewsExtract(film_id):
   logger.debug("Lancement de l'extraction des reviews pour le film {}".format(film_id))
   reviewPage = IMDBExtractor_Reviews(film_id)

   reviewPage.extractReviewsPage_DB()
   

   #TODO extraire le FullReviewURL

def IMDB_keywordsExtract(film_id):
   #sur la page keywords
   logger.debug("Lancement de l'extraction des keywords pour le film {}".format(film_id))
   keywordsPage = IMDBExtractor_Keyword(film_id)

   keywordsPage.extractKeywordsPage_DB()


def IMDB_companyCreditsExtractor(film_id):
   #sur la page companycredits
   logger.debug("Lancement de l'extraction des de la page Company Credits pour le film {}".format(film_id))
   companyCreditsPage = IMDBExtractor_companyCredits(film_id)

   companyCreditsPage.extractCompanyCreditsPage_DB()


def IMDB_fullCreditsExtractor(film_id):
   logger.debug("Lancement de l'extraction des de la page full credits pour le film {}".format(film_id))
   fullCreditsPage = IMDBExtractor_fullCredits(film_id)

   fullCreditsPage.extractFullCreditsPage_DB()


def IMDB_personExtractor(person_id):
   logger.debug("Lancement de l'extraction de la page person pour {}".format(person_id))
   personPage = IMDBExtractor_Person(person_id)

   personPage.extractPerson_DB()

def IMDB_SuperExtractor(film_id):
   IMDB_filmExtract(film_id) 
   IMDB_awardsExtract(film_id)
   IMDB_keywordsExtract(film_id)
   IMDB_reviewsExtract(film_id) #TODO
   IMDB_companyCreditsExtractor(film_id)
   IMDB_fullCreditsExtractor(film_id)


###############################################
#                MAIN
###############################################


IMDB_SuperExtractor(film_id_)
