from cinema.models import Film
from vectorizers import *
import filmsfilter as flt
import completer as cplt
import regression as rgrs
import classification as clsf
import pylab as pl

### SCIKITLEARN ###########

# Filter films from database
    
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

# Data treatment

y = y.ravel() # make it a vector
X = np.concatenate(X,axis=1)
X[np.isnan(X)] = -1 # replace NaN with -1 for missing values
# hist(log(y),20) # print log(y) distribution
y_log = np.log(y)

### CLASSIFICATION #######################################
thresh = np.median(y_log)
y_bin = y_log > thresh
scores_class = clsf.getRandomForestClassifierCVScore(X,y_bin)
print scores_class.mean()

### REGRESSION ###########################################
scores = rgrs.getRandomForestRegressorCVScore(X,y_log)
print scores.mean(), 'chance level : %s' % y_bin.mean()

#yy = pipeline.fit(X, y_log).predict(X[1::2])

# pl.plot(y_log[1::2], yy, 'x')

## FEATURES IMPORTANCE

#clf.fit(X, y_log)

# pl.stem(range(X.shape[1]), clf.feature_importances_)

#fi = clf.feature_importances_

#print (fi.argsort()[-5:]) # The 5 most important features

#imdb_nb_user_ratings=getImdbNbUserRatingsFeatures(filterFilms())
#pl.plot(imdb_nb_user_ratings,y_log,'+')
#pl.plot(np.log(imdb_nb_user_ratings),y_log,'+')
