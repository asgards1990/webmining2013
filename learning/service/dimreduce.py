from sklearn.feature_extraction import DictVectorizer
import numpy as np
import scipy
from sklearn.cluster import SpectralClustering
from vectorizers import *

def getReducedActorsFeature(films, n_clusters, print_clusters=False):  #returns reduced actors features by spectral clustering
	vec = DictVectorizer(dtype=int)
	generator = genActorsTuples(films.iterator()) 
	X = vec.fit_transform(generator)
	return reduceDimBySpectralClustering(X,vec.get_feature_names(), n_clusters, print_clusters)

def getReducedDirectorsFeature(films, X_actors_reduced):  #returns reduced directors features by averaging directors' casts features over all their films
	films_list = list(films)
	X_directors_reduced = np.zeros(X_actors_reduced.shape)
	for film in films:
		casts = np.zeros(X_actors_reduced[0].shape)
		count_casts=0
		for director in film.directors.all():
			director_films = director.films_from_director.all()
			for film_of_director in director_films:
				if film_of_director in films:
					casts = casts + X_actors_reduced[films_list.index(film_of_director),:]
					count_casts = count_casts+1
		X_directors_reduced[films_list.index(film),:] = casts/count_casts
	return X_directors_reduced

def reduceDimBySpectralClustering(X, feature_names, n_clusters, print_clusters=False): #returns X_reduced
	# Perform spectral clustering
	labels = spectralClustering(X,n_clusters) # labels = cluster number of each feature
	# Print clusters if asked
	if print_clusters:
		printClusters(feature_names,labels, n_clusters)
	# Reduce dimension of features
	d = scipy.sparse.diags(labels+1,0,dtype=int) # put labels in a diagonal sparse matrix (+1 IOT start from 1 and not 0)
	Z = (X*d).toarray()
	X_reduced = np.apply_along_axis(lambda x: np.bincount(x, minlength=n_clusters+1), 1, Z)[:,1:]
	aux = X_reduced.sum(axis=1).reshape(X_reduced.shape[0],1) # for normalizing
	return X_reduced.astype(np.float32)/aux

def spectralClustering(X,n_clusters): #returns the labels obtained from spectral clustering
	SC = SpectralClustering(n_clusters = n_clusters, eigen_solver='arpack', affinity="nearest_neighbors")
	SC.fit(X.transpose())
	return SC.labels_.astype(np.int) # contains, for each tuple, the number of its cluster (between 0 and n_clusters-1)

def printClusters(feature_names,labels, n_clusters): #prints 10 features of each cluster
	for cluster in range(n_clusters):
		print('\nCluster '+str(cluster)+' ('+str(np.sum(labels==cluster))+')')
		count=0
		for index,item in enumerate(labels):
		    if item==cluster and count<10:
			s=feature_names[index]
			print(Person.objects.get(imdb_id=s[:9]).name+'('+s[10]+','+s[-5:]+'),'), # for actors with tuples
			#print(Person.objects.get(imdb_id=s).name+','), #for actors without tuples
			count=count+1
