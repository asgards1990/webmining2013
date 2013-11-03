from cinema.models import Film, Genre
from service.objects import CachedObject
from service.vectorizers import *
import service.filmsfilter as flt
from sklearn.feature_extraction import DictVectorizer

import re

filtered_films = flt.filter1()
indexes = hashIndexes(filtered_films.iterator())

cDict = CachedObject('keywords')
if cDict.checksum != str(hash(''.join(indexes.keys()))):
    print("Computing the keywords sparse matrix ...")

    gkey = genKeywords(filtered_films.iterator())
    indexes = hashIndexes(filtered_films.iterator())
    v = DictVectorizer(dtype=int)
    X0 = v.fit_transform(gkey)
    feature_names = v.get_feature_names()

    cDict.set_content((feature_names, X0))
    cDict.checksum = str(hash(''.join(indexes.keys())))
    cDict.save()
else:
    feature_names, X0 = cDict.get_content()

filmsbygenre = {}
keywordsbygenre = {}
for genre in Genre.objects.all():
    filmsbygenre[genre.name] = map(lambda e : indexes[e], map(lambda e: e.imdb_id, filtered_films.filter(genres = genre)))
    if filmsbygenre[genre.name] == []:
        keywordsbygenre[genre.name] = np.zeros(X0.shape[1])
    else:
        keywordsbygenre[genre.name] = np.sum(X0[filmsbygenre[genre.name]].toarray(), axis=0)

rex = re.compile('male')
[m for m in feature_names if rex.search(m)]
np.array(feature_names)[np.argsort(-keywordsbygenre['Action'])]

from sklearn.feature_extraction.text import TfidfTransformer
X = TfidfTransformer().fit_transform(X0)

k = 40 # wanted number of topics


### SVD DECOMPOSITION (LSA) ##
### USING GENSIM #############
ans = raw_input("Start Latent Semantic Analysis with Gensim ? ")
if ans != "y":
    exit()

from gensim.models.lsimodel import LsiModel
from gensim.matutils import Sparse2Corpus, corpus2dense

co = Sparse2Corpus(X, documents_columns = False)

lsi = LsiModel(corpus=co, num_topics=k)
list_topics = lsi.show_topics(formatted=False)
topics = map(lambda li : [(value, feature_names[int(key)]) for (value, key) in li] ,list_topics)
print(topics)

genreMat = []

for genre in Genre.objects.all():
    index = filmsbygenre[genre.name]
    if index != []:
        obj = lsi[Sparse2Corpus(X[index, :], documents_columns = False)]
        E = corpus2dense(obj, k).transpose()
        genreMat.append( np.hstack([ [genre.name] , np.mean(E, axis = 0)]) )
    else:
        genreMat.append( np.hstack([ [genre.name] , np.zeros(k) ] ))
genreMat = np.vstack(genreMat)
print genreMat


### USING SCIKIT-LEARN #######
ans = raw_input("Start Latent Semantic Analysis with Scikit-Learn ? ")
if ans != "y":
    exit()

from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components = k, n_iterations = 100)
y = svd.fit_transform(X)

topics2 = [[(svd.components_[l][i], feature_names[i]) for i in np.argsort(-np.abs(svd.components_[l]))[:10]] for l in range(k)]
print topics2

genreMat2 = []
for genre in Genre.objects.all():
    index = filmsbygenre[genre.name]
    if index != []:
        E = y[index, :]
        genreMat2.append( np.hstack([ [genre.name] , np.mean(E, axis = 0)]) )
    else:
        genreMat2.append( np.hstack([ [genre.name] , np.zeros(k) ] ))
genreMat2 = np.vstack(genreMat2)
print genreMat2

index = filmsbygenre['Action']
E = y[index, :]

### PCA ######################
ans = raw_input("Start PCA with Scikit ? ")
if ans != "y":
    exit()

from sklearn.decomposition import PCA
pca = PCA(n_components = k, whiten=True)
y = pca.fit_transform(X.todense())

topics3 = [[(pca.components_[l][i], feature_names[i]) for i in np.argsort(-np.abs(pca.components_[l]))[:10]] for l in range(k)]
print topics3

genreMat3 = []
for genre in Genre.objects.all():
    index = filmsbygenre[genre.name]
    if index != []:
        E = y[index, :]
        genreMat3.append( np.hstack([ [genre.name] , np.mean(E, axis = 0)]) )
    else:
        genreMat3.append( np.hstack([ [genre.name] , np.zeros(k) ] ))
genreMat3 = np.vstack(genreMat3)
print genreMat3

index = filmsbygenre['Action']
E = y[index, :]

### FASTICA ###################
ans = raw_input("Start FastICA with Scikit ? ")
if ans != "y":
    exit()

from sklearn.decomposition import FastICA
ica = FastICA(n_components = k, whiten=True)
y = ica.fit_transform(X.todense())

topics4 = [[(ica.components_[l][i], feature_names[i]) for i in np.argsort(-np.abs(ica.components_[l]))[:10]] for l in range(k)]
print topics4

genreMat4 = []
for genre in Genre.objects.all():
    index = filmsbygenre[genre.name]
    if index != []:
        E = y[index, :]
        genreMat4.append( np.hstack([ [genre.name] , np.mean(E, axis = 0)]) )
    else:
        genreMat4.append( np.hstack([ [genre.name] , np.zeros(k) ] ))
genreMat4 = np.vstack(genreMat4)
print genreMat4

index = filmsbygenre['Action']
E = y[index, :]

### K-Means ###################
ans = raw_input("Start K-Means with Scikit ? ")
if ans != "y":
    exit()

from sklearn.cluster import MiniBatchKMeans, KMeans
km = MiniBatchKMeans(n_clusters=k, init='k-means++', n_init=1, init_size=1000, batch_size=1000, verbose=1)
km2 = KMeans(n_clusters = k, init='k-means++', verbose=1)
y2 = km2.fit_transform(X)

topics5 = [[(km.cluster_centers_[l][i], feature_names[i]) for i in np.argsort(-np.abs(km.cluster_centers_[l]))[:10]] for l in range(k)]
print topics5


### NMF #######################
ans = raw_input("Start NMF with Scikit ? ")
if ans != "y":
    exit()

from sklearn.decomposition import ProjectedGradientNMF
# BEWARE : THIS IS COMPUTATIONNALY INTENSIVE
nmf = ProjectedGradientNMF(n_components=k, max_iter = 10, nls_max_iter=100)
nmf.fit(X)

topics6 = [[(nmf.components_[l][i], feature_names[i]) for i in np.argsort(-np.abs(nmf.components_[l]))[:10]] for l in range(k)]