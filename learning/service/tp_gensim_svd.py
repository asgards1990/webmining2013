from cinema.models import Film
from vectorizers import *
import filmsfilter as flt
import random
from sklearn.feature_extraction import DictVectorizer
from gensim.models.lsimodel import LsiModel

from gensim.matutils import Dense2Corpus

lf = list(flt.filter1())
random.shuffle(lf)
lf2 = lf[:100]
g = genKeywords(iter(lf2))
v = DictVectorizer(dtype=int)
X = v.fit_transform(g)

co = Dense2Corpus(X)

lsi = LsiModel(corpus=co, num_topics=50)