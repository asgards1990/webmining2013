# -*- coding: utf-8 -*-

from dictionary_bagofwords import get_dictionary
from sklearn.feature_extraction.text import CountVectorizer
import prodbox

def get_bagofwords(predicted_score, genre_numbers):

    # predicted_score : la note moyenne prédite pour le film virtuel (nombre)
    # genre_numbers : la liste du (des) indice(s) donnant le(s) genre(s) du film virtuel

    app = prodbox.CinemaService()
    app.loadFilms()
    app.loadGenres()
    app.loadReviews()
    app.loadReviewsContent()

    accuracy = 4.
    # le niveau de précision qui détermine quelles notes on considère comme proches de la note du film virtuel

    # On sélectionne d'abord les critiques pertinentes pour élaborer le bag of words :

    corpus = []

    for i in range(len(app.films)):

        # on retient le film n° i s'il est de l'un des genres voulus...

        if max([app.genres_matrix[i, genre] == 1 for genre in genre_numbers]):

               # ... et on retient alors les critiques de ce film dont la note est proche de predicted_score :
               
            for journal in app.reviews_content[i].keys():
                   
                journal_index = app.reviews_names.index(journal)

                if abs(predicted_score - app.reviews_matrix[i, journal_index]) < .5/accuracy:
                    
                    print "Note : " + str(app.reviews_matrix[i, journal_index]) + ", critique : " + app.reviews_content[i][journal]
                    corpus.append(app.reviews_content[i][journal])

    # Une fois le corpus de critiques construit, on procède au comptage automatique des mots du dictionnaire

    v = CountVectorizer()

    dic = get_dictionary()
    # le dictionnaire d'adjectifs

    # On retire du dictionnaire certains mots positifs qui pourraient apparaître artificiellement, sans être pertinents pour un film mal noté :

    positive_adjectives = {'perfect' : .6, 'great' : .6, 'epic' : .6, 'artful' : .6}

    for adj, adj_positivity in positive_adjectives.items():
        
        if predicted_score < adj_positivity:

            del dic[adj]

    # Puis on procède au comptage :

    v.vocabulary_ = dic

    X = v.transform(corpus).toarray()

    y = [sum(X[:,i]) for i in range(len(v.vocabulary_))]
    # on s'intéresse aux adjectifs qui apparaissent le plus souvent dans l'ensemble du corpus

    top_indexes = sorted(range(len(y)), key = lambda i: y[i])[-10:]

    inv_dic = {adj : key for key, adj in dic.items()}

    return {inv_dic[i]: y[i] for i in top_indexes if y[i] > 1}
# on sélectionne les 10 adjectifs les plus utilisés et on les retourne avec un poids égal à leur nombre d'occurences
