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

films = Film.objects.order_by('-release_date')[:100]

#FEATURES

X0 = []

for film in films:
    data = {
        'budget_of_film':film.budget
    }
    if getSeason(film.release_date) != None:
        data['_' + getSeason(film.release_date)] = 1
    for c in film.country.all():
        data[c.name] = 1
    for genre in film.genres.all():
        data[genre.name] = 1
    for keyword in film.keywords.all():
        data[keyword.word] = 1
    for production_company in film.production_companies.all():
        data[production_company.imdb_id] = 1
    for director in film.directors.all():
        data['director_' + director.imdb_id] = 1
    for writer in film.writers.all():
        data['writer_' + writer.imdb_id] = 1
    for aw in ActorWeight.objects.filter(film=film):
        data['actor_' + str(aw.rank) + '_' + aw.actor.imdb_id] = 1
    for review in Review.objects.filter(film=film).all():
        data['review_' + review.journal.name] = review.grade
    X0.append(data)

vecX = DictVectorizer()
X = vecX.fit_transform(X0).toarray()

#LABELS

Y0=[]
for film in films:
    data = {
        'box_office':film.box_office
    }
    for prize in Prize.objects.filter(film=film).all():
        s='win'
        if not prize.win:
            s='nomination'
        data['prize_' + prize.institution.name + '_' + s] = 1
    Y0.append(data)

vecY = DictVectorizer()
Y = vecY.fit_transform(Y0).toarray()

y = Y[:,0]
# avoir une meilleure strategie, par cluster de genre
y[isnan(y)] = np.mean(y[-isnan(y)])
h = y > np.median(y)

# renormaliser les donnees, gerer les donnees manquantes
# faire des histogrammes
# classification binaire sur le box office
# LDA dans un premier temps, régression logistique puis SVM et Boosting

# construire des classifieurs par cluster (ex: annees 2000, genre...)
# Stochastic Gradient Descent