from sklearn.feature_extraction import DictVectorizer
from vectorizers import *
import filmsfilter as flt
import numpy as np
import scipy
from sklearn.cluster import SpectralClustering

films = flt.filter2(100)
#films = flt.filter1()

# Create adjacency matrix
print('Creating film-actor features...')
vec = DictVectorizer(dtype=int)
generator_actors = genActorsTuples(films.iterator()) #tuples
X = vec.fit_transform(generator_actors)
print('Doing spectral clustering...')
n_clusters = 5 # number of clusters
SC = SpectralClustering(n_clusters = n_clusters, eigen_solver='arpack', affinity="nearest_neighbors")
SC.fit(X.transpose())
y = SC.labels_.astype(np.int) # labels : contains, for each tuple, the number of its cluster (between 0 and n_clusters-1)

def printClusters():
	actors_ids = vec.get_feature_names()
	for cluster in range(n_clusters):
		print('\nCluster '+str(cluster)+' ('+str(np.sum(y==cluster))+')')
		count=0
		for index,item in enumerate(y):
		    if item==cluster and count<10:
			s=actors_ids[index]
			print(Person.objects.get(imdb_id=s[:9]).name+'('+s[10]+','+s[-5:]+'),'), # for actors with tuples
			#print(Person.objects.get(imdb_id=s).name+','), #for actors without tuples
			count=count+1

def reduceDim(feature,labels, n_clusters):
	print('Reducing feature dimensions...')
	d = scipy.sparse.diags(labels+1,0,dtype=int)
	Z = (feature*d).toarray()
	feature_reduced = np.apply_along_axis(lambda x: np.bincount(x, minlength=n_clusters+1), 1, Z)[:,1:]
	aux = feature_reduced.sum(axis=1).reshape(feature_reduced.shape[0],1)
	return feature_reduced.astype(np.float32)/aux

printClusters()
X_reduced = reduceDim(X,y,n_clusters) # reduced feature of size (nb films,nb clusters)
