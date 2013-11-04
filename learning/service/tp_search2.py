from sklearn.neighbors import NearestNeighbors
import filmsfilter as flt
from dimreduce import *
from vectorizers import *
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer, normalize
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime

def fitsInFilter(film,filters): #returns True if film respects filters
	fits=True
	actor_weights_qs = ActorWeight.objects.filter(film=film)
	actors = Person.objects.filter(id__in=actor_weights_qs.values('actor_id'))
	for actor in filters['actors']:
		if not actor in actors.all():
			fits=False
	for director in filters['directors']:
		if not director in film.directors.all():
			fits=False
	for genre in filters['genres']:
		if not genre in film.genres.all():
			fits=False
	if not film.budget >= filters['budget']['min']:
		fits=False
	if not film.budget <= filters['budget']['max']:
		fits=False
	if (filters['release_period']['begin']!=None) and (not film.release_date >= filters['release_period']['begin']):
		fits=False
	if (filters['release_period']['end']!=None) and (not film.release_date <= filters['release_period']['end']):
		fits=False
	if not film.metacritic_score >= filters['reviews']['min']:
		fits=False
	return fits

def applyFilter(filters): #returns indexes of films that respect our filters
	index = 0
	indexes = []
	for film in films.all():
		if fitsInFilter(films[index],filters):
			indexes.append(index)
		index = index+1
	return indexes

####### Step 1 :Get films ##########################################

films = flt.filter2(200)

####### Step 2 : Define parameters ###################################

filters = {'actors':[],
	'directors':[],
	'genres':[Genre.objects.get(name='Action')],
	'budget':{'min':0,'max':10000000000000000000000},
	'reviews':{'min':0},
	'release_period':{'begin':None,'end':None}
	}
filters = None
criteria = {'actor_director':True,
          'budget':True,
          'review':True,
          'genre':True}
nb_results = 10 # nb of nearest neighbors returned
film_index = 119 #Avatar 119 #Argo 104 #np.random.random_integers(0,films.count()-1) # randomly pick film for which we look for neighbors
p_norm = 2 # p-norm used for distances
n_clusters_actors = 10 # nb of clusters for actors dimension reduction
n_clusters = 6 # nb of clusters for distance
high_weight = 1 # for the distance definition
low_weight = 0 # for the distance definition

####### Step 3 : Features #########################################

# Build the features
X_people = getReducedActorsFeature(films, n_clusters_actors) if criteria['actor_director'] else None #TODO add director # TAKES WAY TOO MUCH TIME
X_budget = DictVectorizer(dtype=np.float32).fit_transform(genBudget(films.iterator())).toarray() if criteria['budget'] else None
X_review = DictVectorizer(dtype=np.float32).fit_transform(genReviews(films.iterator())) if criteria['review'] else None
X_genre = DictVectorizer(dtype=int).fit_transform(genGenres(films.iterator())) if criteria['genre'] else None
# Reshape features
X_budget[np.isnan(X_budget)] = -1 # replace NaN with -1 for missing values
completer = Imputer(missing_values=-1)
completer.fit(X_budget)
X_budget = completer.transform(X_budget) #use log instead ?
X_budget = X_budget/np.max(X_budget)
X_review = X_review/100 # because grades should be in [0,1]
X_review = X_review/X_review.shape[1] #divide by number of columns
X_genre = X_genre/X_genre.shape[1] #divide by number of columns
X_people = X_people/X_people.shape[1] #divide by number of columns
# Build X
X = []
X.append((high_weight if criteria['actor_director'] else low_weight)*X_people)
X.append((high_weight if criteria['budget'] else low_weight)*X_budget)
X.append((high_weight if criteria['review'] else low_weight)*X_review.toarray())
X.append((high_weight if criteria['genre'] else low_weight)*X_genre.toarray())
X = np.concatenate(X,axis=1)

####### Step 4 : Clustering (specific to criterias) ###################

print('--> Doing clustering...')
KM = KMeans(n_clusters=n_clusters)
KM.fit_predict(X)
labels = KM.labels_

####### Step 5 : Finding neighbors ###################################

# Apply filters
if filters!=None:
	indexes_fitting_filters = applyFilter(filters)
else:
	indexes_fitting_filters = range(films.count())
indexes_fitting_filters = np.array(indexes_fitting_filters)
print('--> Start looking for neighbors...')
# Find neighbors
distance_to_each_cluster = KM.transform(X[film_index])
clusters_by_distance = distance_to_each_cluster.argsort()[0]
nb_results_found=0
distances=[]
neighbors_indexes=[]
for cluster in clusters_by_distance:
	if nb_results_found < nb_results +1:
		print('--> Looking in cluster '+str(cluster)+' ('+str(nb_results_found)+' results found yet)')
		indexes_of_cluster = np.where(labels == cluster)[0]
		indexes = np.intersect1d(indexes_of_cluster, indexes_fitting_filters)
		samples = X[list(indexes),:]
		neigh = NearestNeighbors(n_neighbors=(nb_results-nb_results_found)+1, p=p_norm)
		neigh.fit(samples)
		(loc_distances,loc_neighbors_indexes) = neigh.kneighbors(X[film_index])
		local_nb_results_found = loc_distances[0].shape[0]
		print('--> Found '+str(local_nb_results_found)+' results in this cluster')
		nb_results_found = nb_results_found + local_nb_results_found
		distances.append(loc_distances[0])
		neighbors_indexes.append(indexes[loc_neighbors_indexes[0]])
neighbors_indexes = np.concatenate(neighbors_indexes)
distances = np.concatenate(distances)

distances = distances[1:] # because the film being studied is the closest neighbor...
neighbors_indexes = neighbors_indexes[1:]

####### Step 6 : Print results ######################################

print('Film picked : '+films[film_index].english_title)
for i in range(distances.size):
	print('At distance '+str(distances[i])+', '+films[neighbors_indexes[i]].english_title)
