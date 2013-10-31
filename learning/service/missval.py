from cinema.models import Film
from vectorizers import *
import filmsfilter as flt
import completer as cplt
import pylab as pl

### SCIKITLEARN ###########

import sklearn

#from sklearn.preprocessing import Imputer # manage missing values
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import cross_val_score

############################
    
films = flt.filter1()

# Creation of features and labels

X = []
feature_names = []

for name, fun in [('budget', getBudgetFeatures2),
            ('metacritic', getMetacriticScoreFeatures2),
            ('season', getSeasonFeatures2),
            ('runtime', getRuntimeFeatures2),
            #('countries', getCountriesFeatures),
            ('imdb_user_ratings', getImdbUserRatingFeatures2),
            ('imdb_nb_user_reviews', getImdbNbUserReviewsFeatures2),
            ('imdb_nb_reviews_features', getImdbNbReviewsFeatures2),
            ('imdb_nb_user_ratings', getImdbNbUserRatingsFeatures2),
            ('genre', getGenresFeatures)]:
    this_vec = fun(films)
    feature_names += this_vec.get_feature_names()
    X.append(this_vec.toarray())

y = getBoxOfficeFeatures2(films)
y = y.ravel()

X = np.concatenate(X,axis=1)

# Imputer to complete missing values
imputerX = Imputer(missing_values=-1)
X[np.isnan(X)] = -1

# X = imputer.fit_transform(X) : pour calculer les missing values (mieux en pipeline)
# hist(log(y),20)

y_log = np.log(y)

### CLASSIFICATION #######################################

print clsf.getRandomForestClassifierScores(X,y_log)

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
