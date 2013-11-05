from cinema.models import Film
from vectorizers import *
import filmsfilter as flt
import completer as cplt
import regression as rgrs
import classification as clsf
import pylab as pl
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer
import dimreduce as dr

### FILTER FILMS FROM DB ###########################
    
films = flt.filter2(400) # (filter2 returns 100 films for tests)

### CREATE FEATURES ###########################

print('Creating features and labels...')

X = []
feature_names = []
for content_type, fun in [
        (np.float32, genBudget),
            (np.float32, genMetacriticScore),
            (np.int, genSeason),
            (np.float32, genRuntime),
            #(np.float32, genImdbUserRating),
            #(np.float32, genImdbNbUserReviews),
            #(np.float32, genImdbNbReviews),
            #(np.float32, genImdbNbUserRatings),
            (np.int, genGenres),
            (np.int, genCountries),
            #(int, genKeywords),
            #(np.float32, genReviews), #(dim)
            #(int, genPrizes), #(dim)
            #(int, genActors), #dim
            #(int, genDirectors), #dim
            #(int, genWriters), #dim
            #(int, genProductionCompanies), #dim #DOES NOT WORK YET
        ]:
    this_vec = DictVectorizer(dtype=content_type)
    X0 = fun(films.iterator())
    X.append(this_vec.fit_transform(X0).toarray())
    feature_names += this_vec.get_feature_names()

X.append(dr.getReducedActorsFeature(films, 20))
for i in range(20):
    feature_names += ['actor_' + str(i), ]

X = np.concatenate(X,axis=1)

### CREATE LABELS ###########################

this_vec = DictVectorizer()
X0 = genBoxOffice(films.iterator())
y = this_vec.fit_transform(X0).toarray()
y = y.ravel() # make it a vector
y_log = np.log(y) # log distribution of box-office is better for classification/regression (two bumps in the distribution)

### MISSING VALUES COMPLETION ###########################

print('Completing missing values...')

X[np.isnan(X)] = -1 # replace NaN with -1 for missing values
completer = Imputer(missing_values=-1)

### CLASSIFICATION #######################################

def classify():
    print('\nClassification...')
    thresh = np.median(y_log)
    y_bin = y_log > thresh
    (scores, fi) = clsf.getRandomForestClassifierCVScore(X,y_bin,completer)
    fi_indexes = fi.argsort()[-5:] # The 5 most important features
    i=1
    print 'Classification score : ', scores.mean()
    for index in reversed(fi_indexes):
        print(str(i)+'th component : '+feature_names[index]+' with weight '+str(fi[index]))
        i=i+1

classify()

### REGRESSION ###########################################

def regress():
    print('\nRegression...')
    (scores, fi) = rgrs.getRandomForestRegressorCVScore(X,y_log,completer)
    fi_indexes = fi.argsort()[-5:] # The 5 most important features
    i=1
    print 'Regression error : ', scores.mean()
    for index in reversed(fi_indexes):
        print(str(i)+'th component : '+feature_names[index]+' with weight '+str(fi[index]))
        i=i+1

regress()
