import filmsfilter as flt
from dimreduce import *

films = flt.filter2(200)
n_clusters = 3
print_clusters = False
X_actors_reduced = getReducedActorsFeature(films,n_clusters,print_clusters)
print(X_actors_reduced[:10,:]) # print reduced actors features for first 10 films
X_directors_reduced = getReducedDirectorsFeature(films, X_actors_reduced)
print(X_directors_reduced[:10,:]) # print reduced directors features for first 10 films
