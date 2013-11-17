import service.prodbox as sp
import numpy as np
from cinema.models import *


def printClustersShort(labels,names,n_sample):
    for i in np.unique(labels):
        elements_of_cluster = np.where(labels==i)[0]
        print 'Cluster '+str(i)+' : '+str(elements_of_cluster.size)+' elements'

def printClusters(labels,names,n_sample):
    for i in np.unique(labels):
        elements_of_cluster = np.where(labels==i)[0]
        print 'Cluster '+str(i)+' : '+str(elements_of_cluster.size)+' elements'
        print 'Sample : ',
        j=0
        while j<n_sample and j<elements_of_cluster.size:
            try: 
                print Person.objects.get(imdb_id = names[elements_of_cluster[j]]).name+', ',
            except:
                pass
            j=j+1
        print '\n'

def printClustersFilms(labels,names,n_sample):
    for i in np.unique(labels):
        elements_of_cluster = np.where(labels==i)[0]
        print 'Cluster '+str(i)+' : '+str(elements_of_cluster.size)+' elements'
        print 'Sample : ',
        j=0
        while j<n_sample and j<elements_of_cluster.size:
            try: 
                #print Film.objects.get(imdb_id = names[elements_of_cluster[j]]).english_title+', ',
                print names[j]+' ,',
            except:
                pass
            j=j+1
        print '\n'

def printClustersKeywords(labels,names,n_sample):
    for i in np.unique(labels):
        elements_of_cluster = np.where(labels==i)[0]
        print 'Cluster '+str(i)+' : '+str(elements_of_cluster.size)+' elements'
        print 'Sample : ',
        j=0
        while j<n_sample and j<elements_of_cluster.size:
            try: 
                print names[elements_of_cluster[j]]+', ',
            except:
                pass
            j=j+1
        print '\n'


app = sp.CinemaService()
app.loadFilms()
#app.loadData()
app.loadRanks()
app.loadActors()
app.loadActorsReduced()
app.loadDirectors()
app.loadDirectorsReduced()
app.loadKeywords()
app.loadKeywordsReduced()
#app.loadWriters()
#app.loadWritersReduced()
#app.loadSearchClustering()

labels_actors_KM = np.where(app.proj_actors_KM.toarray() != 0)[1]
labels_actors_BOC = np.where(app.proj_actors_BOC.toarray() != 0)[1]
labels_directors_KM = np.where(app.proj_directors_KM.toarray() != 0)[1]
#labels_writers_KM = np.where(app.proj_writers_KM.toarray() != 0)[1]
labels_keywords_KM = np.where(app.proj_keywords_KM.toarray() != 0)[1]
#labels_searchclustering_KM = app.search_clustering_KM[1]['labels']

n_sample = 30

app.save_cache()

def printClustersActorsSVD():
    for l in range(app.dim_actors):
        compo = []
        for i in np.argsort(-np.abs(app.proj_actors_SVD[:,l]))[:10]:
            try:
                compo.append((app.proj_actors_SVD[i][l], Person.objects.get(imdb_id=app.actor_names[i]).name))
            except:
                pass
        print compo

def printClustersDirectorsSVD():
    for l in range(app.dim_directors):
        compo = []
        for i in np.argsort(-np.abs(app.proj_directors_SVD[:,l]))[:10]:
            try:
                compo.append((app.proj_directors_SVD[i][l], Person.objects.get(imdb_id=app.director_names[i]).name))
            except:
                pass
        print compo

#printClustersShort(labels_actors_KM, app.actor_names,n_sample)
#printClusters(labels_actors_BOC, app.actor_names,n_sample)
#printClusters(labels_directors_KM, app.director_names,n_sample)
#printClusters(labels_writers_KM, app.writer_names,n_sample)
printClustersKeywords(labels_keywords_KM, app.keyword_names,n_sample)
#printClustersFilms(labels_searchclustering_KM, app.film_names,n_sample)
#printClustersActorsSVD()
#printClustersDirectorsSVD()

#app.quit()

