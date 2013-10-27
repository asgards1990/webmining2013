# /usr/bin/env python
# -*- coding: latin-1 -*-



####################################################################


#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import FilmExtractor_utils_config as FilmExtractorUtilsConfig

from cinema.models import *


logger = initLogger.getLogger(FilmExtractorUtilsConfig.UTILS_EXTRACTOR_LOGGER_NAME)

###################################################################

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

def defineActorWeight(actor,film):
   try :
      actor_weight = ActorWeight.objects.get(actor=actor,film=film)
      return actor_weight 
   except ActorWeight.DoesNotExist :
      logger.info("Création de l'Actor weight dans la base de données")
      actor_weight = ActorWeight.objects.create(actor=actor,film=film)
      actor_weight.star = False
      return actor_weight 
   except Exception as e:
      logger.error('Impossible de retrouver la personne {} a cause de l erreur {}'.format(e))
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



