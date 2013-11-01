from cinema.models import Film, Genre
from vectorizers import *
import filmsfilter as flt
from sklearn.feature_extraction import DictVectorizer

filtered_films = flt.filter1()

gkey = genKeywords(filtered_films.iterator())
ids = hashIds(filtered_films.iterator())
v = DictVectorizer(dtype=int)
X = v.fit_transform(gkey)
feature_names = v.get_feature_names()

from sklearn.feature_extraction.text import TfidfTransformer
idf = TfidfTransformer()
X = idf.fit_transform(X)

k = 10 # wanted number of topics

### SVD DECOMPOSITION (LSA) ##
### USING GENSIM #############

from gensim.models.lsimodel import LsiModel
from gensim.matutils import Sparse2Corpus, corpus2dense

co = Sparse2Corpus(X, documents_columns = False)

lsi = LsiModel(corpus=co, num_topics=k)
list_topics = lsi.show_topics(formatted=False)
topics = map(lambda li : [(value, feature_names[int(key)]) for (value, key) in li] ,list_topics)
print(topics)

genreMat = []
for genre in Genre.objects.all():
    imdb_ids = map(lambda e: e.imdb_id, filtered_films.filter(genres = genre))
    index = map(lambda e : ids[e], imdb_ids)
    if index != []:
        obj = lsi[Sparse2Corpus(X[index, :], documents_columns = False)]
        E = corpus2dense(obj, k).transpose()
        genreMat.append( np.hstack([ [genre.name] , np.mean(E, axis = 0)]) )
    else:
        genreMat.append( np.hstack([ [genre.name] , np.zeros(k) ] ))
genreMat = np.vstack(genreMat)
print genreMat


### USING SCIKIT-LEARN #######
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components = k, n_iterations = 100)
svd.fit(X)

topics2 = [[(svd.components_[l][i], feature_names[i]) for i in np.argsort(-np.abs(svd.components_[l]))[:10]] for l in range(k)]
print topics2

genreMat2 = []
for genre in Genre.objects.all():
    imdb_ids = map(lambda e: e.imdb_id, filtered_films.filter(genres = genre))
    index = map(lambda e : ids[e], imdb_ids)
    if index != []:
        E = svd.transform(X[index, :])
        genreMat2.append( np.hstack([ [genre.name] , np.mean(E, axis = 0)]) )
    else:
        genreMat2.append( np.hstack([ [genre.name] , np.zeros(k) ] ))
genreMat2 = np.vstack(genreMat2)
print genreMat2

genre = Genre.objects.get(name = 'Action')
imdb_ids = map(lambda e: e.imdb_id, filtered_films.filter(genres = genre))
index = map(lambda e : ids[e], imdb_ids)
E = svd.transform(X[index, :])

### PCA ######################
from sklearn.decomposition import PCA
pca = PCA(n_components = k, whiten=True)
pca.fit(X.todense())

topics3 = [[(pca.components_[l][i], feature_names[i]) for i in np.argsort(-np.abs(pca.components_[l]))[:10]] for l in range(k)]
print topics3

genreMat3 = []
for genre in Genre.objects.all():
    imdb_ids = map(lambda e: e.imdb_id, filtered_films.filter(genres = genre))
    index = map(lambda e : ids[e], imdb_ids)
    if index != []:
        E = pca.transform(X[index, :].todense())
        genreMat3.append( np.hstack([ [genre.name] , np.mean(E, axis = 0)]) )
    else:
        genreMat3.append( np.hstack([ [genre.name] , np.zeros(k) ] ))
genreMat3 = np.vstack(genreMat3)
print genreMat3

genre = Genre.objects.get(name = 'Action')
imdb_ids = map(lambda e: e.imdb_id, filtered_films.filter(genres = genre))
index = map(lambda e : ids[e], imdb_ids)
E = pca.transform(X[index, :].todense())

### FASTICA ###################
from sklearn.decomposition import FastICA
ica = FastICA(n_components = k, whiten=True)
ica.fit(X.todense())

topics4 = [[(ica.components_[l][i], feature_names[i]) for i in np.argsort(-np.abs(ica.components_[l]))[:10]] for l in range(k)]
print topics4

genreMat4 = []
for genre in Genre.objects.all():
    imdb_ids = map(lambda e: e.imdb_id, filtered_films.filter(genres = genre))
    index = map(lambda e : ids[e], imdb_ids)
    if index != []:
        E = pca.transform(X[index, :].todense())
        genreMat4.append( np.hstack([ [genre.name] , np.mean(E, axis = 0)]) )
    else:
        genreMat4.append( np.hstack([ [genre.name] , np.zeros(k) ] ))
genreMat3 = np.vstack(genreMat3)
print genreMat4

genre = Genre.objects.get(name = 'Action')
imdb_ids = map(lambda e: e.imdb_id, filtered_films.filter(genres = genre))
index = map(lambda e : ids[e], imdb_ids)
E = ica.transform(X[index, :].todense())