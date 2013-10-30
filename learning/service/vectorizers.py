import numpy as np
from sklearn.feature_extraction import DictVectorizer
from cinema.models import *
import datetime

def getSeason(date):
    if not date:
        return None
    if date.month in [12, 1, 2]:
        return 'winter'
    if date.month in [3, 4, 5]:
        return 'spring'
    if date.month in [6, 7, 8]:
        return 'summer'
    if date.month in [9, 10, 11]:
        return 'fall'

def getKeywordsFeatures(films):
    X0 = [({keyword.word:1 for keyword in film.keywords.all() if film.keywords.all().count()!=0} if film.keywords.all().count()!=0 else {'no-keyword':1}) for film in films]
    vecX = DictVectorizer(dtype=int)
    return vecX.fit_transform(X0).toarray()

def getGenresFeatures(films):
    X0 = [({genre.name:1 for genre in film.genres.all()} if film.genres.all().count()!=0 else {'no-genre':1}) for film in films]
    vecX = DictVectorizer(dtype=int)
    return vecX.fit_transform(X0).toarray()

def getProductionCompaniesFeatures(films):
    X0 = [({production_company.imdb_id:1 for production_company in film.production_companies.all()} if film.production_companies.all().count()!=0 else {'no-pcs':1}) for film in films]
    vecX = DictVectorizer(dtype=int)
    return vecX.fit_transform(X0).toarray()

def getCountriesFeatures(films):
    X0 = [({c.name:1 for c in film.country.all()} if film.country.all().count()!=0 else {'no-country':1}) for film in films]
    vecX = DictVectorizer(dtype=int)
    return vecX.fit_transform(X0).toarray()

def getDirectorsFeatures(films):
    X0 = [({director.imdb_id:1 for director in film.directors.all()} if film.directors.all().count()!=0 else {'no-directors':1}) for film in films]
    vecX = DictVectorizer(dtype=int)
    return vecX.fit_transform(X0).toarray()

def getWritersFeatures(films):
    X0 = [({writer.imdb_id:1 for writer in film.writers.all()} if film.writers.all().count()!=0 else {'no-writer':1}) for film in films]
    vecX = DictVectorizer(dtype=int)
    return vecX.fit_transform(X0).toarray()

def getActorsFeatures(films):
    X0 = [({aw.actor.imdb_id+'_'+str(aw.rank):1 for aw in ActorWeight.objects.filter(film=film)} if ActorWeight.objects.filter(film=film).all().count()!=0 else {'no-actor':1}) for film in films]
    vecX = DictVectorizer(dtype=int)
    return vecX.fit_transform(X0).toarray()

def getReviewsFeatures(films): 
    X0 = [({review.journal.name:review.grade for review in Review.objects.filter(film=film).all()} if Review.objects.filter(film=film).all().count()!=0 else {'no-review':1}) for film in films]
    vecX = DictVectorizer(dtype=np.float32)
    return vecX.fit_transform(X0).toarray()

def getPrizesFeatures(films):
    X0 = [({prize.institution.name+'_'+('win' if prize.win else 'nomination'):1 for prize in Prize.objects.filter(film=film).all()} if Prize.objects.filter(film=film).all().all().count()!=0 else {'no-prize':1}) for film in films]
    vecX = DictVectorizer(dtype=int)
    return vecX.fit_transform(X0).toarray()

def getSeasonFeatures(films):
    X0 = []
    for film in films:
        season = getSeason(film.release_date)
        if season != None:
            X0.append({season:1})
        else:
            X0.append({'no-season':1})
    vecX = DictVectorizer(dtype=int)
    return vecX.fit_transform(X0).toarray()

def getBudgetFeatures(films):
    X0 = []
    for film in films:
        budget = film.budget
        if budget != None:
            X0.append({'budget':budget})
        else:
            X0.append({'no-budget':1})
    vecX = DictVectorizer(dtype=np.float32)
    return vecX.fit_transform(X0).toarray()

def getBoxOfficeFeatures(films):
    X0 = []
    for film in films:
        box_office = film.box_office
        #if box_office != None:
        X0.append({'box_office':box_office})
        #else:
            #X0.append({'no_box_office':1})
    vecX = DictVectorizer(dtype=np.float32)
    return vecX.fit_transform(X0).toarray()


#films = Film.objects.order_by('-release_date').all()

#FEATURES
#X_budget = getBudgetFeatures(films)
#X_season = getSeasonFeatures(films)
#X_countries = getCountriesFeatures(films)
#X_genres = getGenresFeatures(films)
#X_keywords = getKeywordsFeatures(films)
#X_pcs = getProductionCompaniesFeatures(films)
#X_actors = getActorsFeatures(films)
#X_directors = getDirectorsFeatures(films)
#X_writers = getWritersFeatures(films)
#X_reviews = getReviewsFeatures(films)
#LABELS
#Y_box_office = getBoxOfficeFeatures(films)
#Y_prizes = getPrizesFeatures(films)

#y = Y_box_office
#y[isnan(y)] = np.mean(y[-isnan(y)])
#matplotlib.pyplot.hist(y)

#y = Y[:,0]
# avoir une meilleure strategie, par cluster de genre
#y[isnan(y)] = np.mean(y[-isnan(y)])
#h = y > np.median(y)
# renormaliser les donnees, gerer les donnees manquantes
# faire des histogrammes
# classification binaire sur le box office
# LDA dans un premier temps, regression logistique puis SVM et Boosting
# construire des classifieurs par cluster (ex: annees 2000, genre...)
# Stochastic Gradient Descent


#X0 = []
#for film in films:
#    data = {
#        'budget_of_film':film.budget
#    }
#    if getSeason(film.release_date) != None:
#        data['_' + getSeason(film.release_date)] = 1
#    for c in film.country.all():
#        data[c.name] = 1
#    for genre in film.genres.all():
#        data[genre.name] = 1
#    for keyword in film.keywords.all():
#        data[keyword.word] = 1
#    for production_company in film.production_companies.all():
#        data[production_company.imdb_id] = 1
#    for director in film.directors.all():
#        data['director_' + director.imdb_id] = 1
#    for writer in film.writers.all():
#        data['writer_' + writer.imdb_id] = 1
#    for aw in ActorWeight.objects.filter(film=film):
#        data['actor_' + str(aw.rank) + '_' + aw.actor.imdb_id] = 1
#    for review in Review.objects.filter(film=film).all():
#        data['review_' + review.journal.name] = review.grade
#    X0.append(data)
#vecX = DictVectorizer()
#X = vecX.fit_transform(X0).toarray()
#LABELS
#Y0=[]
#for film in films:
#    data = {
#        'box_office':film.box_office
#    }
#    for prize in Prize.objects.filter(film=film).all():
#        s='win'
#        if not prize.win:
#            s='nomination'
#        data['prize_' + prize.institution.name + '_' + s] = 1
#    Y0.append(data)
#vecY = DictVectorizer()
#Y = vecY.fit_transform(Y0).toarray()
