from cinema.models import Film, Genre
from vectorizers import *
import filmsfilter as flt
from sklearn.feature_extraction import DictVectorizer
from gensim.models.lsimodel import LsiModel
from gensim.matutils import Sparse2Corpus, corpus2dense

filtered_films = flt.filter1()

gkey = genKeywords(filtered_films.iterator())
ids = hashIds(filtered_films.iterator())
v = DictVectorizer(dtype=int)
X = v.fit_transform(gkey)
feature_names = v.get_feature_names()

co = Sparse2Corpus(X, documents_columns = False)

k = 4 # wanted number of topics

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