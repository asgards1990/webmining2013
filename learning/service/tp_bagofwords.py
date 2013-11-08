# -*- coding: utf-8 -*-

import vocabulary
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def test():
    print "Hello"

def get_bagofwords(app, predicted_score, genre_numbers):

    N = 6.

    print 'Chose genres :'

    for k in genre_numbers:
        print app.genres_names[k]

    # préparation du corpus

    corpus = []

    nb_films = len(app.films)

    total_number_reviewers = len(app.reviews_names)

    for i in range(nb_films):
        # on ajoute le film au corpus si 

        # calcul de la note moyenne

        s = 0
        number_reviewers = 0

        for j in range(total_number_reviewers):

            if app.reviews_matrix[i,j] > 0:
                number_reviewers += 1
                s += app.reviews_matrix[i,j]

        if abs(predicted_score - s / number_reviewers) < 1/N:

            for genre in genre_numbers:

                if app.genres_matrix[i,genre] == 1:

                    corpus.append(i)
                    print app.films[i]
                    break

    # comptage des mots

    v = CountVectorizer(ngram_range=(1,1))

    v.vocabulary_ = vocabulary.get_vocabulary()

    X = v.transform([app.reviews_content[k] for k in corpus]).toarray()

    y = [sum(X[:,k]) for k in range(len(v.vocabulary_))]

    top_indexes = sorted(range(len(y)), key = lambda i: y[i])[-20:]
    
    print top_indexes

    return [key for key, value in v.vocabulary_.items() if value in top_indexes]
