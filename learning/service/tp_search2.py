from sklearn.neighbors import NearestNeighbors
import filmsfilter as flt
from dimreduce import *
from vectorizers import *
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer, normalize
import numpy as np
from sklearn.cluster import KMeans

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

films = flt.filter2(50)

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
nb_results = 10
film_index = np.random.random_integers(0,films.count()-1)
p_norm=2
nb_clusters_actors=10
n_clusters = 6 #clusters for distance
high_weight = 1
low_weight = 0

# Build the features
X_people = getReducedActorsFeature(films, nb_clusters_actors) if criteria['actor_director'] else None #TODO add director
X_budget = DictVectorizer(dtype=np.float32).fit_transform(genBudget(films.iterator())).toarray() if criteria['budget'] else None
X_review = DictVectorizer(dtype=np.float32).fit_transform(genReviews(films.iterator())).toarray() if criteria['review'] else None
X_genre = DictVectorizer(dtype=int).fit_transform(genGenres(films.iterator())).toarray() if criteria['genre'] else None

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
X.append((high_weight if criteria['review'] else low_weight)*X_review)
X.append((high_weight if criteria['genre'] else low_weight)*X_genre)
X = np.concatenate(X,axis=1)

# Clustering (specific to criterias)

KM = KMeans(n_clusters=n_clusters)
KM.fit_predict(X)
cluster_centers = KM.cluster_centers_
labels = KM.labels_

# Apply filters
if filters!=None:
	indexes_fitting_filters = applyFilter(filters)
else:
	indexes_fitting_filters = range(films.count())
#samples = X[indexes,:]

# Find neighbors
distance_to_each_cluster = KM.transform(X[film_index])
clusters_by_distance = distance_to_each_cluster.argsort()
nb_results_found=0
for cluster in cluster_by_distance:
	#indexes = filter
	#indexes = intersection of indexes_fitting_filters and labels.index(cluster)
	samples_in_current_cluster = samples[]
	neigh = NearestNeighbors(n_neighbors=nb_results+1, p=p_norm)
	neigh.fit(samples)
	(distances,neighbors_indexes) = neigh.kneighbors(X[film_index])

# TODO : work on each cluster separately


# Print results
print('Film choosed : '+films[film_index].english_title)
for i in range(neighbors_indexes.size)[1:]:
	print('At distance '+str(distances[0,i])+', '+films[indexes[neighbors_indexes[0,i]]].english_title)

