from cinema.models import Film
from vectorizers import *

import pylab as pl

### SCIKITLEARN ###########

import sklearn

from sklearn.preprocessing import Imputer # manage missing values
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

from sklearn.cross_validation import cross_val_score

############################

def filterFilms():
    print('Nb of films in DB : ' + str(Film.objects.count()))
    films = Film.objects.exclude(runtime=None).exclude(genres=None).exclude(country=None).exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).exclude(box_office=None)
    for film in films:
        if film.imdb_nb_user_reviews==None:
            film.imdb_nb_user_reviews=0
        if film.imdb_nb_reviews==None:
            film.imdb_nb_reviews=0
    print('Nb of films after cleaning : ' + str(films.count()) + '. Selected ' + str(float(films.count())/Film.objects.count()) + ' %.')
    return films
    
films = filterFilms()

# Creation of features

X = []
features_names = []

for name, fun in [('budget', getBudgetFeatures),
            ('metacritic', getMetacriticScoreFeatures),
            ('season', getSeasonFeatures),
            ('runtime', getRuntimeFeatures),
            ('countries', getCountriesFeatures),
            ('imdb_user_ratings', getImdbUserRatingFeatures),
            ('imdb_nb_user_reviews', getImdbNbUserReviewsFeatures),
            ('imdb_nb_reviews_features', getImdbNbReviewsFeatures),
            ('imdb_nb_user_ratings', getImdbNbUserRatingsFeatures),
            ('genre', getGenresFeatures)]:
    this_X = fun(films)
    features_names += ['%s%d' % (name, k) for k in range(this_X.shape[1])]
    X.append(this_X)

y = getBoxOfficeFeatures(films)
y = y.ravel()

X = np.concatenate(X,axis=1)

# Imputer to complete missing values
imputer = Imputer(missing_values=-1)

X[np.isnan(X)] = -1

# X = imputer.fit_transform(X) : pour calculer les missing values (mieux en pipeline)

# hist(log(y),20)

y_log = np.log(y)

### CLASSIFICATION #######################################

thresh = np.median(y_log)

y_bin = y_log > thresh

y_bin.mean()

clf_class = RandomForestClassifier()

pipeline_class = Pipeline([('imputer', imputer), ('clf', clf_class)])

scores_class = cross_val_score(pipeline_class, X, y_bin, cv=3)

print scores_class.mean(), 'chance level : %s' % y_bin.mean()

###########################################################

### REGRESSION ###########################################

clf = RandomForestRegressor()  #RandomForestClassifier()

pipeline = Pipeline([('imputer', imputer), ('clf', clf)])

scores = cross_val_score(pipeline, X, y_log, cv=3) # y_bin for Classification

print scores.mean(), 'chance level : %s' % y_bin.mean()

yy = pipeline.fit(X, y_log).predict(X[1::2])

# pl.plot(y_log[1::2], yy, 'x')

## FEATURES IMPORTANCE

clf.fit(X, y_log)

# pl.stem(range(X.shape[1]), clf.feature_importances_)

fi = clf.feature_importances_

print (fi.argsort()[-5:]) # The 5 most important features

imdb_nb_user_ratings=getImdbNbUserRatingsFeatures(filterFilms())
pl.plot(imdb_nb_user_ratings,y_log,'+')
pl.plot(np.log(imdb_nb_user_ratings),y_log,'+')
