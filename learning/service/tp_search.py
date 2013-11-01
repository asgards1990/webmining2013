import filmsfilter as flt
from vectorizers import *
from sklearn.feature_extraction import DictVectorizer

films = flt.filter2(10)
n_clusters = 3

filters = None
criteria = {'actor_director':False,
          'budget':True,
          'review':True,
          'genre':True}
nb_results = 5
film_index = 0
closest_films = getClosestFilms(films,film_index,nb_results,criteria,filters)

def getClosestFilms(index, nb_results, criteria, filters=None):
    # Features (relevant to criteria)
    X_people = [] if criteria['actor_director'] else None #TODO
    X_budget = DictVectorizer(dtype=int).fit_transform(genBudget(films.iterator())) if criteria['budget'] else None
    X_review = DictVectorizer(dtype=np.float32).fit_transform(genReviews(films.iterator())) if criteria['review'] else None
    X_genre = DictVectorizer(dtype=int).fit_transform(genGenres(films.iterator())) if criteria['genre'] else None
    print X_people, X_budget, X_review, X_genre
    # Clustering
    (labels,centroids) = performClustering(n_clusters,criteria) # perform clustering according to criteria
    current_cluster = labels[index] # get cluster of the film we're studying
    for centroid in centroids:
        cluster_distances.append(distance(centroid, centroids[current_cluster]))
    closest_clusters = cluster_distances.argsort() #order cluster labels according to distance
    # Apply filters
    if filters!=None:
        indexes = applyFilter(filters)
    else:
        indexes = range(films.size)
    # For each cluster
    # returns a list of (film,value)
    
def applyFilter(filters): #returns indexes of films that respect our filters
    #TODO
    return []

def performClustering(n_clusters, criteria): # performs clustering on the films and returns labels
    #TODO
    labels = []
    centroids = []
    return (labels,centroids) #centroids contains indexes of other centroids in the order of labels

def distance(index1, index2, criteria):
    # index1 is the index of film1
    # index2 is the index of film2 in films
    # criteria = {'actor_director':True, 'budget':True, 'review':True, 'genre:True}
    return

def findClosestFilms(indexes, nb_results):
    #indexes is the indexes of films to search in films
    #nb_results is the number of results to return
    return []
