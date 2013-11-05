import filmsfilter as flt
from dimreduce import *
from vectorizers import *
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer
import numpy as np
from sklearn.cluster import KMeans

def distance(index1, index2, criteria, X_people, X_budget, X_review, X_genre):
	res = 0
	low_weight = 0
	high_weight = 1
	return (high_weight if criteria['actor_director'] else low_weight)*distancePeople(index1,index2,X_people) + (high_weight if criteria['budget'] else low_weight)*distanceBudget(index1,index2,X_budget) + (high_weight if criteria['review'] else low_weight)*distanceReview(index1,index2,X_review) + (high_weight if criteria['genre'] else low_weight)*distanceGenre(index1,index2,X_genre)

def distancePeople(index1, index2, X_people):
	#TODO define this
	return 0

def distanceBudget(index1, index2, X_budget):
	aux=X_budget/np.max(X_budget)
	return np.linalg.norm(aux[index1,:]-aux[index2,:],p_norm)

def distanceReview(index1, index2, X_review):
	#TODO define this
	return 0

def distanceGenre(index1, index2, X_genre):
	aux = X_genre/X_genre.shape[1]
	return np.linalg.norm(aux[index1,:]-aux[index2,:],p_norm)

###### Step 1 : Get films #################################

films = flt.filter2(50)

###### Step 2 : Define parameters #########################

n_clusters = 3 # nb of clusters preprocessed for finding nearest neighbors quickly
nb_clusters_actors = 6 # for reducing dimension of actors features
filters = None #TODO allow for filters
criteria = {'actor_director':False, #TODO allow for True
          'budget':True,
          'review':False, #TODO allow for True
          'genre':True}
nb_results = 2 # nb of nearest neighbors returned
film_index = np.random.random_integers(0,films.count()-1) # index of film picked for tests
p_norm = 2

###### Step 3 : Features ###################################

# Get raw features
X_people = getReducedActorsFeature(films, nb_clusters_actors) #TODO include directors
X_budget = DictVectorizer(dtype=np.float32).fit_transform(genBudget(films.iterator())).toarray()
X_review = DictVectorizer(dtype=np.float32).fit_transform(genReviews(films.iterator())).toarray()
X_genre = DictVectorizer(dtype=int).fit_transform(genGenres(films.iterator())).toarray()
# Complete budget missing values
X_budget[np.isnan(X_budget)] = -1 # replace NaN with -1 for missing values
completer = Imputer(missing_values=-1)
completer.fit(X_budget)
X_budget = completer.transform(X_budget)

###### Step 3 : Clusterization ###################################

#KM = KMeans(n_clusters)

###### Step 3 : Find nearest neighbors  naively ###################

def findNearestNeighborsIn(indexes,film_index,films,nb_results, criteria, X_people, X_budget, X_review, X_genre):
	distances = [distance(film_index, index, criteria, X_people, X_budget, X_review, X_genre) for index in indexes]
	sorted_dist_indexes = np.array(distances).argsort()[:nb_results]
	return (sorted_dist_indexes, np.array(distances)[list(sorted_dist_indexes)])

indexes = range(films.count())
if film_index in indexes:
	del indexes[film_index]
# TODO filter indexes according to filters
(neighbors_indexes,neighbors_dist) = findNearestNeighborsIn(indexes,film_index,films,nb_results, criteria, X_people, X_budget, X_review, X_genre)

#Print results#
print('Film choosed : '+films[film_index].english_title)
print('Neighbors :'),
for neighbors_index in neighbors_indexes:
	print films.all()[indexes[neighbors_index]].english_title+'(distance '+str(neighbors_dist[neighbors_index])+'),',
