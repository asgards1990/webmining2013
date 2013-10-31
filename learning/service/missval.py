from cinema.models import Film
from vectorizers import *
import filmsfilter as flt
import completer as cplt
import regression as rgrs
import classification as clsf
import pylab as pl
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer

### FILTER FILMS FROM DB ###########################
    
films = flt.filter2() #change to filter1 later (filter2 returns 100 films for tests)

### CREATE FEATURES ###########################

X = []
feature_names = []
for name, fun in [ #TODO : gérer les dtype
	    ('budget', genBudget),
            ('metacritic', genMetacriticScore),
            ('season', genSeason),
            ('runtime', genRuntime),
            ('imdb_user_ratings', genImdbUserRating),
            ('imdb_nb_user_reviews', genImdbNbUserReviews),
            ('imdb_nb_reviews', genImdbNbReviews),
            ('imdb_nb_user_ratings', genImdbNbUserRatings),
            ('genre', genGenres),
            ('countries', genCountries),
            #('keywords', genKeywords),
            #('reviews', genReviews), #(dim)
            #('prizes', genPrizes), #(dim)
            #('actors', genActors), #dim
            #('directors', genDirectors), #dim
            #('writers', genWriters), #dim
            #('production_companies', genProductionCompanies), #dim #DOES NOT WORK YET
		]:
    this_vec = DictVectorizer()
    X0 = fun(films.iterator())
    #feature_names += this_vec.get_feature_names()
    X.append(this_vec.fit_transform(X0).toarray())
X = np.concatenate(X,axis=1)

### CREATE LABELS ###########################

this_vec = DictVectorizer()
X0 = genBoxOffice(films.iterator())
y = this_vec.fit_transform(X0).toarray()
y = y.ravel() # make it a vector
y_log = np.log(y) # log distribution of box-office is better for classification/regression (two bumps in the distribution)

### MISSING VALUES COMPLETION ###########################

X[np.isnan(X)] = -1 # replace NaN with -1 for missing values
completer = Imputer(missing_values=-1)

### CLASSIFICATION #######################################
thresh = np.median(y_log)
y_bin = y_log > thresh
scores_class = clsf.getRandomForestClassifierCVScore(X,y_bin,completer)
print scores_class.mean()

### REGRESSION ###########################################
scores = rgrs.getRandomForestRegressorCVScore(X,y_log,completer)
print scores.mean()

#old code
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
