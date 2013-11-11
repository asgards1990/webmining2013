# -*- coding: utf-8 -*-

from objects import *
from vectorizers import *
from cinema.models import Film, Person, Genre, Keyword, Journal, Institution
import filmsfilter as flt

import numpy as np
import scipy

from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors.kde import KernelDensity
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import SpectralClustering
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from dictionary_bagofwords import get_dictionary

import dateutil.parser
import re

import exceptions

class CinemaService(LearningService):
    def __init__(self):
        super(CinemaService, self).__init__()
        self.films = flt.getFilms(withnanbo = True)
        # TODO: also try log of budget for testing search requests
        self.budget_bandwidth = 1000.0 # TODO : optimize this parameter
        # Define parameters # TODO : optimize all these parameters
        self.dim_writers = 20
        self.dim_directors = 10
        self.dim_actors = 20
        self.dim_keywords = 30
        self.n_clusters_search = 20
        self.p_norm = 2 # p-norm used for distances
        self.high_weight = 1.2 # for the distance definition
        self.low_weight = 0.2 # for the distance definition
        self.actors_theta_BOC = 0.8
        self.n_neighbors_SC_actors = 8 # spectral clustering parameter
        self.n_neighbors_SC_writers = 8 # spectral clustering parameter
        self.n_neighbors_SC_directors = 8 # spectral clustering parameter
        self.actor_reduction_rank_threshold = 10

        self.reduction_actors_in_predictfeatures = 'KM' 
        self.reduction_directors_in_predictfeatures = 'KM' 

        self.reduction_actors_in_directoractormatrix = 'KM' # useful only for spectral clustering

        self.reduction_actors_in_searchclustering = 'KM'
        self.reduction_directors_in_searchclustering = 'KM'

        self.clustering_type_in_searchclustering = 'KM'

        self.search_latent_vars = False
        self.min_nb_of_films_to_use_clusters_in_search = 100 # optimize this to make search faster
        
        self.min_awards = 100
        
    def loadData(self):
        assert self.dim_keywords >= self.dim_writers, 'dim_writers should be lower than dim_keywords' 
        assert self.dim_actors >= self.dim_directors, 'dim_directors should be lower than dim_actors' 
        # Load films data
        self.loadFilms()
        self.loadImdb()
        self.loadLanguages()
        self.loadGenres()
        self.loadBoxOffice() # Need nb_user_ratings, user_rating, genres, languages
        # Load prediction features
        self.loadActors() # Need box office
        self.loadStars()
        self.loadRanks()
        self.loadActorsReduced()
        self.loadDirectors()
        self.loadDirectorsReduced()
        self.loadSeason()
        self.loadBudget()
        self.loadKeywords()        
        self.loadKeywordsReduced()
        # Load prediction labels
        self.loadPrizes()
        self.loadReviews()
        self.loadReviewsContent()
        # Load other features
        self.loadStats()
        self.loadWriters()
        self.loadWritersReduced()
        self.loadRuntime()
        self.loadMetacriticScore()
        self.loadReleaseDate()
        self.loadProductionCompanies()
        self.loadCountries()
    
    def loadFilms(self):
        if not self.is_loaded('films'):
            self.fromPktoIndex, self.fromIndextoPk, self.film_names = hashIndexes(self.films.iterator())
            self.create_cobject('films', (self.fromPktoIndex, self.fromIndextoPk, self.film_names))
        else:
            self.fromPktoIndex, self.fromIndextoPk, self.film_names = self.get_cobject('films').get_content()
        self.nb_films = len(self.fromPktoIndex)
    
    def loadImdb(self):
        if not self.is_loaded('imdb'):
            # imdb_user_rating
            g_user_rating = genImdbUserRating(self.films.iterator())
            v_user_rating = DictVectorizer(dtype=np.float32)
            self.imdb_user_rating_matrix = v_user_rating.fit_transform(g_user_rating)
            # imdb_nb_user_ratings
            g_nb_user_ratings = genImdbNbUserRatings(self.films.iterator())
            v_nb_user_ratings = DictVectorizer(dtype=int)
            self.imdb_nb_user_ratings_matrix = v_nb_user_ratings.fit_transform(g_nb_user_ratings)
            # imdb_nb_user_reviews
            g_nb_user_reviews = genImdbNbUserReviews(self.films.iterator())
            v_nb_user_reviews = DictVectorizer(dtype=np.float32)
            self.imdb_nb_user_reviews_matrix = v_nb_user_reviews.fit_transform(g_nb_user_reviews)
            for i in range(self.imdb_nb_user_reviews_matrix.shape[0]):
                if np.isnan(self.imdb_nb_user_reviews_matrix[i,0]):
                    self.imdb_nb_user_reviews_matrix[i,0]=0
            # imdb_nb_reviews
            g_nb_reviews = genImdbNbReviews(self.films.iterator())
            v_nb_reviews = DictVectorizer(dtype=np.float32)
            self.imdb_nb_reviews_matrix = v_nb_reviews.fit_transform(g_nb_reviews)
            for i in range(self.imdb_nb_reviews_matrix.shape[0]):
                if np.isnan(self.imdb_nb_reviews_matrix[i,0]):
                    self.imdb_nb_reviews_matrix[i,0]=0
            # Save object in cache
            self.create_cobject('imdb', (self.imdb_user_rating_matrix, self.imdb_nb_user_ratings_matrix, self.imdb_nb_user_reviews_matrix,self.imdb_nb_reviews_matrix))
        else:
            self.imdb_user_rating_matrix, self.imdb_nb_user_ratings_matrix, self.imdb_nb_user_reviews_matrix,self.imdb_nb_reviews_matrix = self.get_cobject('imdb').get_content()
   
    def loadBudget(self):
        if not self.is_loaded('budget'):
            gkey = genBudget(self.films.iterator())
            v =  DictVectorizer(dtype=np.float32)
            self.budget_matrix = v.fit_transform(gkey)

            budget_data = self.budget_matrix.data[-np.isnan(self.budget_matrix.data)]
            budget_data = budget_data.reshape( [budget_data.shape[0], 1])
            kde = KernelDensity(kernel='gaussian', bandwidth=self.budget_bandwidth).fit(budget_data)

            for i in range(self.budget_matrix.shape[0]):
                if np.isnan(self.budget_matrix[i,0]):
                    self.budget_matrix[i,0]= max(1, kde.sample(1))

            # Save object in cache
            self.create_cobject('budget', self.budget_matrix)
        else:
            self.budget_matrix = self.get_cobject('budget').get_content()
    
    def loadReleaseDate(self):
        if not self.is_loaded('release_date'):
            gkey = genReleaseDate(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.release_date_matrix = v.fit_transform(gkey)
            self.release_date_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('release_date', (self.release_date_matrix,self.release_date_names))
        else:
            self.release_date_matrix,self.release_date_names = self.get_cobject('release_date').get_content()
    
    def loadRuntime(self):
        if not self.is_loaded('runtime'):
            gkey = genRuntime(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.runtime_matrix = v.fit_transform(gkey)
            # Save object in cache
            self.create_cobject('runtime', self.runtime_matrix)
        else:
            self.runtime_matrix = self.get_cobject('runtime').get_content()
    
    def loadBoxOffice(self):
        if not self.is_loaded('box_office'):
            gkey = genBoxOffice(self.films.iterator())
            v =  DictVectorizer(dtype=np.float32)
            self.box_office_matrix = v.fit_transform(gkey)

            y = self.box_office_matrix.toarray()[:,0]
            nan_indexes = np.isnan(y)
            if np.sum(nan_indexes)>0:
                X = scipy.sparse.hstack([
                        self.imdb_user_rating_matrix,
                        self.imdb_nb_user_ratings_matrix,
                        self.languages_matrix,
                        self.genres_matrix]).toarray()
                reg = GradientBoostingRegressor()
                reg.fit(X[-nan_indexes, :], y[-nan_indexes])
                y[nan_indexes] = reg.predict(X[nan_indexes, :])
                y[y < 0] = 1
                self.box_office_matrix = scipy.sparse.csc_matrix(y).transpose()

            # Save object in cache
            self.create_cobject('box_office', self.box_office_matrix)
        else:
            self.box_office_matrix = self.get_cobject('box_office').get_content()
    
    def loadGenres(self):
        if not self.is_loaded('genres'):
            gkey = genGenres(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.genres_matrix = v.fit_transform(gkey)
            self.genres_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('genres', (self.genres_names, self.genres_matrix))
        else:
            self.genres_names, self.genres_matrix = self.get_cobject('genres').get_content()
        self.nb_genres = self.genres_matrix.shape[1]

    def loadPrizes(self):
        if not self.is_loaded('prizes'):
            gkey = genPrizes(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.prizes_matrix = v.fit_transform(gkey)
            self.prizes_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('prizes', (self.prizes_names, self.prizes_matrix))
        else:
            self.prizes_names, self.prizes_matrix = self.get_cobject('prizes').get_content()
        self.nb_prizes = self.prizes_matrix.shape[1]

    def loadCountries(self):
        if not self.is_loaded('countries'):
            gkey = genCountries(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.countries_matrix = v.fit_transform(gkey)
            self.countries_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('countries', (self.countries_names, self.countries_matrix))
        else:
            self.countries_names, self.countries_matrix = self.get_cobject('countries').get_content()
    
    def loadLanguages(self):
        if not self.is_loaded('languages'):
            gkey = genLanguages(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.languages_matrix = v.fit_transform(gkey)
            self.languages_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('languages', (self.languages_names, self.languages_matrix))
        else:
            self.languages_names, self.languages_matrix = self.get_cobject('languages').get_content()
    
    def loadMetacriticScore(self):
        if not self.is_loaded('metacritic_score'):
            gkey = genMetacriticScore(self.films.iterator())
            v =  DictVectorizer(dtype=np.float32)
            self.metacritic_score_matrix = v.fit_transform(gkey)
            # Save object in cache
            self.create_cobject('metacritic_score', self.metacritic_score_matrix)
        else:
            self.metacritic_score_matrix = self.get_cobject('metacritic_score').get_content()
    
    def loadProductionCompanies(self):
        if not self.is_loaded('production_companies'):
            gkey = genProductionCompanies(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.production_companies_matrix = v.fit_transform(gkey)
            self.production_companies_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('production_companies', (self.production_companies_names, self.production_companies_matrix))
        else:
            self.production_companies_names, self.production_companies_matrix = self.get_cobject('production_companies').get_content()
    
    def loadReviews(self):
        if not self.is_loaded('reviews'):
            gkey = genReviews(self.films.iterator())
            v =  DictVectorizer(dtype=np.float32)
            self.reviews_matrix = v.fit_transform(gkey)
            self.reviews_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('reviews', (self.reviews_names, self.reviews_matrix))
        else:
            self.reviews_names, self.reviews_matrix = self.get_cobject('reviews').get_content()
        self.nb_journals = self.reviews_matrix.shape[1]

    def loadReviewsContent(self):
        if not self.is_loaded('reviews_content'):
            gkey = genReviewsContent(self.films.iterator())
            self.reviews_content = []
            for d in gkey:
                self.reviews_content.append(d)
            self.create_cobject('reviews_content', self.reviews_content)
        else:
            self.reviews_content = self.get_cobject('reviews_content').get_content()

    def loadSeason(self):
        if not self.is_loaded('season'):
            gkey = genSeason(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.season_matrix = v.fit_transform(gkey)
            self.season_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('season', (self.season_names, self.season_matrix))
        else:
            self.season_names, self.season_matrix = self.get_cobject('season').get_content()
    
    def loadStats(self):
        if not self.is_loaded('genre_stats'):
            self.keywordsbygenre = self.genres_matrix.transpose() * self.keyword_matrix
            # Save object in cache
            self.create_cobject('genre_stats', self.keywordsbygenre)
        else:
            self.keywordsbygenre = self.get_cobject('genre_stats').get_content()
    
    def loadKeywords(self):
        if not self.is_loaded('keywords'):
            gkey = genKeywords(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.keyword_matrix = v.fit_transform(gkey)
            self.keyword_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('keywords', (self.keyword_names, self.keyword_matrix))
        else:
            self.keyword_names, self.keyword_matrix = self.get_cobject('keywords').get_content()
        self.nb_keywords = self.keyword_matrix.shape[1]

    def loadKeywordsReduced(self):
        if not self.is_loaded('keywords_reduced'):
            keywords_KM = KMeans(n_clusters = self.dim_keywords, init='k-means++')
            keyword_labels_KM = keywords_KM.fit_predict(TfidfTransformer().fit_transform(self.keyword_matrix).transpose())
            self.proj_keywords_KM = scipy.sparse.csc_matrix(keyword_labels_KM==0, dtype=int).transpose()
            for i in range(1, self.dim_keywords):
                self.proj_keywords_KM = scipy.sparse.hstack([self.proj_keywords_KM, scipy.sparse.csc_matrix(keyword_labels_KM==i, dtype=int).transpose()])
            self.proj_keywords_KM=normalize(self.proj_keywords_KM.astype(np.double),axis=0, norm='l1')
            self.keywords_reduced_KM = self.keyword_matrix * self.proj_keywords_KM
            # Save object in cache
            self.create_cobject('keywords_reduced', (self.keywords_reduced_KM, self.proj_keywords_KM))
        else:
            self.keywords_reduced_KM, self.proj_keywords_KM = self.get_cobject('keywords_reduced').get_content()
    
    def loadRanks(self):
        if not self.is_loaded('ranks'):
            v = DictVectorizer(dtype=int)
            self.rank_matrix = v.fit_transform(genRanks(self.films.iterator())) 
            self.rank_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('ranks', (self.rank_matrix,self.rank_names))
        else:
            self.rank_matrix, self.rank_names = self.get_cobject('ranks').get_content()

    def loadStars(self):
        if not self.is_loaded('stars'):
            v = DictVectorizer(dtype=int)
            self.star_matrix = v.fit_transform(genStars(self.films.iterator())) 
            self.star_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('stars', (self.star_matrix,self.star_names))
        else:
            self.star_matrix, self.star_names = self.get_cobject('stars').get_content()

    def loadActors(self):
        if not self.is_loaded('actors'):
            v = DictVectorizer(dtype=int)
            self.actor_matrix = v.fit_transform(genActors(self.films.iterator()))
            self.actor_names = v.get_feature_names()
            # Save object in cache
            self.create_cobject('actors', (self.actor_matrix,self.actor_names))
        else:
            self.actor_matrix, self.actor_names = self.get_cobject('actors').get_content()
        self.nb_actors = self.actor_matrix.shape[1]

    def loadActorsReduced(self):
        if not self.is_loaded('actors_reduced'):
            # First clustering method: Spectral Clustering
            # First we filter the actor_matrix IOT keep only high rank relationships 
            #actor_matrix = scipy.sparse.csr_matrix(self.actor_matrix.toarray() * (self.rank_matrix.toarray()>=self.actor_reduction_rank_threshold))
            #try:
            #    actors_SC = SpectralClustering(n_clusters=self.dim_actors,eigen_solver='arpack',affinity="nearest_neighbors",n_neighbors=self.n_neighbors_SC_actors)
            #    actor_labels_SC = actors_SC.fit_predict(actor_matrix.transpose())
            #    self.proj_actors_SC = scipy.sparse.csc_matrix(actor_labels_SC==0, dtype=int).transpose()
            #    for i in range(1, self.dim_actors):
            #        self.proj_actors_SC = scipy.sparse.hstack([self.proj_actors_SC, scipy.sparse.csc_matrix(actor_labels_SC==i, dtype=int).transpose()])
            #    self.proj_actors_SC=normalize(self.proj_actors_SC.astype(np.double), norm='l1', axis=0)
            #    self.actor_reduced_SC = actor_matrix * self.proj_actors_SC
            #except MemoryError:
            #    self.actor_reduced_SC = None
            #    print('Spectral clustering failed for actors due to memory error')
            # Second clustering method: KMeans clustering with tf-idf
            actors_KM = KMeans(n_clusters = self.dim_actors, init='k-means++')
            actor_labels_KM = actors_KM.fit_predict(TfidfTransformer().fit_transform(self.actor_matrix).transpose())
            self.proj_actors_KM = scipy.sparse.csc_matrix(actor_labels_KM==0, dtype=int).transpose()
            for i in range(1, self.dim_actors):
                self.proj_actors_KM = scipy.sparse.hstack([self.proj_actors_KM, scipy.sparse.csc_matrix(actor_labels_KM==i, dtype=int).transpose()])
            self.proj_actors_KM=normalize(self.proj_actors_KM.astype(np.double),axis=0, norm='l1')
            self.actor_reduced_KM = self.actor_matrix * self.proj_actors_KM
            # Third method : box office clustering
            actor_weight_matrix = self.rank_matrix
            rv = scipy.stats.poisson(self.actors_theta_BOC)
            actor_weight_matrix.data = rv.pmf(actor_weight_matrix.data).astype(np.float32)
            self.actor_share_bo = normalize(actor_weight_matrix.todense(), axis=1, norm='l1').T * self.box_office_matrix
            sorted_actors = np.argsort(self.actor_share_bo[:,0])
            index = 0
            for k in range(self.dim_actors):
                r = 1 if k < self.nb_actors % self.dim_actors else 0
                row = sorted_actors[index: (index + r + self.nb_actors/self.dim_actors-1)]
                index += r + self.nb_actors/self.dim_actors
                col, data = np.zeros(row.shape[0]), np.ones(row.shape[0])
                if k>0:
                    self.proj_actors_BOC = scipy.sparse.hstack([self.proj_actors_BOC,  scipy.sparse.csr_matrix((data, (row, col)), shape=(self.nb_actors, 1) )])
                else:
                    self.proj_actors_BOC = scipy.sparse.csr_matrix((data, (row, col)), shape=(self.nb_actors, 1))
            self.actor_reduced_BOC = self.actor_matrix * self.proj_actors_BOC
            self.actor_reduced_BOC = normalize(self.actor_reduced_BOC.astype(np.double), norm='l1', axis=1)
            # Save object in cache
            self.create_cobject('actors_reduced', (self.actor_reduced_KM, self.proj_actors_KM, self.actor_reduced_BOC, self.proj_actors_BOC))
        else:
            self.actor_reduced_KM, self.proj_actors_KM, self.actor_reduced_BOC, self.proj_actors_BOC = self.get_cobject('actors_reduced').get_content()
  
    def loadWriters(self):
        keywords_reduced = self.keywords_reduced_KM
        if not self.is_loaded('writers'):
            v=DictVectorizer(dtype=int)
            self.writer_matrix = v.fit_transform(genWriters(self.films.iterator()))
            self.writer_names = v.get_feature_names()
            self.writer_keyword_matrix = normalize(self.writer_matrix.transpose().astype(np.double), norm='l1', axis=1).astype(np.double) * keywords_reduced
            # Save object in cache
            self.create_cobject('writers', (self.writer_matrix, self.writer_names, self.writer_keyword_matrix))
        else:
            self.writer_matrix, self.writer_names, self.writer_keyword_matrix = self.get_cobject('writers').get_content()
        self.nb_writers = self.writer_matrix.shape[1]
    
    def loadWritersReduced(self):
        if not self.is_loaded('writers_reduced'):
            # First clustering method: Spectral Clustering
            #try:
            #    writer_SC = SpectralClustering(n_clusters=self.dim_writers,eigen_solver='arpack',affinity="nearest_neighbors",n_neighbors=self.n_neighbors_SC_writers)
            #    writer_labels_SC = writer_SC.fit_predict(self.writer_keyword_matrix)
            #    self.proj_writers_SC = scipy.sparse.csc_matrix(writer_labels_SC==0, dtype=int).transpose()
            #    for i in range(1, self.dim_writers):
            #        self.proj_writers_SC = scipy.sparse.hstack([self.proj_writers_SC, scipy.sparse.csc_matrix(writer_labels_SC==i, dtype=int).transpose()])
            #    self.proj_writers_SC=normalize(self.proj_writers_SC.astype(np.double),axis=0, norm='l1')
            #    self.writer_reduced_SC = self.writer_matrix * self.proj_writers_SC
            #except MemoryError:
            #    self.writer_reduced_SC = None
            #    print('Spectral clustering failed for writers due to memory error')
            # Second clustering method: Average of keywords features
            self.writer_reduced_avg =  normalize(self.writer_matrix.astype(np.double), norm='l1', axis=1) * self.writer_keyword_matrix
            # Third clustering method: KMeans clustering with tf-idf
            writers_KM = KMeans(n_clusters = self.dim_writers, init='k-means++')
            writer_labels_KM = writers_KM.fit_predict(TfidfTransformer().fit_transform(self.writer_matrix).transpose())
            self.proj_writers_KM = scipy.sparse.csc_matrix(writer_labels_KM==0, dtype=int).transpose()
            for i in range(1, self.dim_writers):
                self.proj_writers_KM = scipy.sparse.hstack([self.proj_writers_KM, scipy.sparse.csc_matrix(writer_labels_KM==i, dtype=int).transpose()])
            self.proj_writers_KM=normalize(self.proj_writers_KM.astype(np.double),axis=0, norm='l1')
            self.writer_reduced_KM = self.writer_matrix * self.proj_writers_KM
            # Save object in cache
            self.create_cobject('writers_reduced', (self.writer_reduced_avg, self.writer_reduced_KM))
        else:
            self.writer_reduced_avg, self.writer_reduced_KM = self.get_cobject('writers_reduced').get_content()

    def loadDirectors(self):
        if self.reduction_actors_in_directoractormatrix == 'KM':
            actor_reduced = self.actor_reduced_KM
        if self.reduction_actors_in_directoractormatrix == 'SC':
            actor_reduced = self.actor_reduced_SC
        if self.reduction_actors_in_directoractormatrix == 'BOC':
            actor_reduced = self.actor_reduced_BOC
        if not self.is_loaded('directors'):
            v=DictVectorizer(dtype=int)
            self.director_matrix = v.fit_transform(genDirectors(self.films.iterator()))
            self.director_names = v.get_feature_names()
            self.director_actor_matrix = normalize(self.director_matrix.transpose().astype(np.double), norm='l1', axis=1) * actor_reduced
            # Save object in cache
            self.create_cobject('directors', (self.director_matrix, self.director_names, self.director_actor_matrix))
        else:
            self.director_matrix, self.director_names, self.director_actor_matrix = self.get_cobject('directors').get_content()
        self.nb_directors = self.director_matrix.shape[1]
    
    def loadDirectorsReduced(self):
        if not self.is_loaded('directors_reduced'):
            # First clustering method: Spectral Clustering
            #try:
            #    director_SC = SpectralClustering(n_clusters=self.dim_directors,eigen_solver='arpack',affinity="nearest_neighbors",n_neighbors=self.n_neighbors_SC_directors)
            #    director_labels_SC = director_SC.fit_predict(self.director_actor_matrix)
            #    self.proj_directors_SC = scipy.sparse.csc_matrix(director_labels_SC==0, dtype=int).transpose()
            #    for i in range(1, self.dim_directors):
            #        self.proj_directors_SC = scipy.sparse.hstack([self.proj_directors_SC, scipy.sparse.csc_matrix(director_labels_SC==i, dtype=int).transpose()])
            #    self.proj_directors_SC=normalize(self.proj_directors_SC.astype(np.double),axis=0, norm='l1')
            #    self.director_reduced_SC = self.director_matrix * self.proj_directors_SC
            #except MemoryError:
            #    self.director_reduced_SC = None
            #    print('Spectral clustering failed for directors due to memory error')
            # Second clustering method: Average of actors features
            self.director_reduced_avg =  normalize(self.director_matrix.astype(np.double), norm='l1', axis=1) * self.director_actor_matrix
            # Third clustering method: KMeans clustering with tf-idf
            directors_KM = KMeans(n_clusters = self.dim_directors, init='k-means++')
            director_labels_KM = directors_KM.fit_predict(TfidfTransformer().fit_transform(self.director_matrix).transpose())
            self.proj_directors_KM = scipy.sparse.csc_matrix(director_labels_KM==0, dtype=int).transpose()
            for i in range(1, self.dim_directors):
                self.proj_directors_KM = scipy.sparse.hstack([self.proj_directors_KM, scipy.sparse.csc_matrix(director_labels_KM==i, dtype=int).transpose()])
            self.proj_directors_KM=normalize(self.proj_directors_KM.astype(np.double),axis=0, norm='l1')
            self.director_reduced_KM = self.director_matrix * self.proj_directors_KM
            # Save object in cache
            self.create_cobject('directors_reduced', (self.director_reduced_avg, self.director_reduced_KM, self.proj_directors_KM))
        else:
            self.director_reduced_avg, self.director_reduced_KM, self.proj_directors_KM = self.get_cobject('directors_reduced').get_content()

    def getWeightedSearchFeatures(self, k):
        if self.reduction_actors_in_searchclustering == 'SC':
            actor_reduced=self.actor_reduced_SC
        if self.reduction_actors_in_searchclustering == 'KM':
            actor_reduced=self.actor_reduced_KM
        if self.reduction_actors_in_searchclustering == 'BOC':
            actor_reduced=self.actor_reduced_BOC
        if self.reduction_directors_in_searchclustering == 'SC':
            director_reduced=self.director_reduced_SC
        if self.reduction_directors_in_searchclustering == 'KM':
            director_reduced=self.director_reduced_KM
        X_people = scipy.sparse.hstack([normalize(actor_reduced.astype(np.double),norm='l1',axis=1),normalize(director_reduced.astype(np.double),norm='l1',axis=1)])
        X_budget = self.budget_matrix
        X_review = self.reviews_matrix
        X_genre =  self.genres_matrix
        X_budget = scipy.sparse.csr_matrix(np.log(X_budget.toarray()))
        X_budget = X_budget/max(X_budget.data)
        X_review = X_review # because grades should be in [0,1]
        X_genre = normalize(X_genre.astype(np.double),norm='l1',axis=1) #normalize
        X_people = X_people/2 #normalize
        people_weight = self.high_weight if (k>>0)%2 else self.low_weight
        budget_weight = self.high_weight if (k>>1)%2 else self.low_weight
        review_weight = self.high_weight if (k>>2)%2 else self.low_weight
        genre_weight = self.high_weight if (k>>3)%2 else self.low_weight
        res = scipy.sparse.hstack([people_weight*X_people, budget_weight*X_budget, review_weight*X_review, genre_weight*X_genre])
        if self.search_latent_vars:
            res = scipy.sparse.hstack([res, self.low_weight * self.keywords_reduced_KM])
        return res

    def loadSearchClustering(self, verbose=False):
        if not self.is_loaded('search_clustering'):
            self.search_clustering_KM = {}
            self.search_clustering_SC = {}
            for k in range(1, 16): # 0 is not a correct value
                print('Doing search clustering number '+str(k)+'/15')
                X = self.getWeightedSearchFeatures(k)
                # First method
                KM = KMeans(n_clusters=self.n_clusters_search, verbose=verbose)
                KM.fit(X)
                self.search_clustering_KM[k] = {'labels' : KM.labels_, 'cluster_centers' : KM.cluster_centers_}
                # Second method
                #SC = SpectralClustering(n_clusters=self.n_clusters_search)
                #SC.fit_predict(X)
                #cluster_centers = []
                #for i in range(self.n_clusters_search):
                #    cluster_center = np.mean(X.toarray()[SC.labels_ == i,:], axis=0)
                #    cluster_centers.append(cluster_center)
                #self.search_clustering_SC[k] = {'labels' : SC.labels_, 'cluster_centers' : cluster_centers}
                self.search_clustering_SC = None #TODO : remove this and uncomment above
            # Save object in cache
            self.create_cobject('search_clustering',(self.search_clustering_SC, self.search_clustering_KM))
        else:
            self.search_clustering_SC, self.search_clustering_KM = self.get_cobject('search_clustering').get_content()

    def loadPredict(self):
        # Load features and labels
        self.loadPredictFeatures()
        self.loadPredictLabels()
        # Init predict classifiers
        self.loadLogBoxOfficeRandomForestRegressor()
        self.loadLogBoxOfficeGradientBoostingRegressor()
        self.loadReviewRandomForestRegressors()
        self.loadReviewGradientBoostingRegressors()
        self.loadPrizeRandomForestRegressors()
        self.loadPrizeLogisticRegression()

    def loadPredictFeatures(self):
        if self.reduction_actors_in_predictfeatures == 'KM':
            actor_reduced = self.actor_reduced_KM
        if self.reduction_actors_in_predictfeatures == 'SC':
            actor_reduced = self.actor_reduced_SC
        if self.reduction_actors_in_predictfeatures == 'BOC':
            actor_reduced = self.actor_reduced_BOC
        
        if self.reduction_directors_in_predictfeatures == 'KM':
            director_reduced = self.director_reduced_KM
        if self.reduction_directors_in_predictfeatures == 'SC':
            director_reduced = self.director_reduced_SC

        keyword_reduced = self.keywords_reduced_KM
        
        self.predict_features = scipy.sparse.hstack([
            actor_reduced,
            director_reduced,
            keyword_reduced,
            self.budget_matrix,
            self.season_matrix,
            self.genres_matrix]).toarray()
        self.predict_features_names = np.concatenate([
            ['actor_feat_' + str(i) for i in range(actor_reduced.shape[1])],
            ['director_feat_' + str(i) for i in range(director_reduced.shape[1])],
            ['keyword_feat_' + str(i) for i in range(keyword_reduced.shape[1])],
            ['budget'],
            self.season_names,
            self.genres_names])

    def loadPredictLabels(self):
        self.predict_labels_log_box_office = np.log(self.box_office_matrix.toarray())
        self.predict_labels_log_box_office_names = ['log_box_office'] # a priori inutile
        self.predict_labels_reviews = self.reviews_matrix.toarray()
        self.predict_labels_reviews_names = ['review_' + s for s in self.reviews_names] # a priori inutile
        self.predict_labels_prizes = self.prizes_matrix.toarray()
        awards_per_institution = np.sum(self.predict_labels_prizes, axis=0)
        considered = awards_per_institution > self.min_awards
        self.nb_considered_prizes = sum(considered)
        self.predict_labels_prizes = self.predict_labels_prizes[:, considered]
        self.predict_labels_prizes_names = ['prize_' + self.prizes_names[k] for k in range(self.nb_prizes) if considered[k] ] # a priori inutile

    def loadLogBoxOfficeRandomForestRegressor(self):
        s = 'log_box_office_random_forest_reg'
        try:
            self.log_box_office_random_forest_reg = self.loadJoblibObject(s)
            print s+' object has been loaded'
        except IOError as e:
            print "Error {}".format(e)
            print s+' object not found. Creating it...'
            self.log_box_office_random_forest_reg = RandomForestRegressor()
            self.log_box_office_random_forest_reg.fit(self.predict_features, self.predict_labels_log_box_office.ravel())
            self.dumpJoblibObject(self.log_box_office_random_forest_reg, s)

    def loadLogBoxOfficeGradientBoostingRegressor(self):
        s = 'log_box_office_gradient_boosting_reg'
        try:
            self.log_box_office_gradient_boosting_reg = self.loadJoblibObject(s)
            print s+' object has been loaded'
        except IOError as e:
            print "Error {}".format(e)
            print s+' object not found. Creating it...'
            self.log_box_office_gradient_boosting_reg = GradientBoostingRegressor()
            self.log_box_office_gradient_boosting_reg.fit(self.predict_features, self.predict_labels_log_box_office.ravel())
            self.dumpJoblibObject(self.log_box_office_gradient_boosting_reg, s)

    def loadReviewRandomForestRegressors(self):
        s = 'review_random_forest_reg'
        try:
            self.review_random_forest_reg = self.loadJoblibObject(s)
            print s+' object has been loaded'
        except IOError:
            print s+' object not found. Creating it...'
            self.review_random_forest_reg = []
            for i in range(self.nb_journals):
                self.review_random_forest_reg.append(RandomForestRegressor())
                self.review_random_forest_reg[i].fit(self.predict_features, self.predict_labels_reviews[:,i])
            self.dumpJoblibObject(self.review_random_forest_reg, s)

    def loadReviewGradientBoostingRegressors(self):
        s = 'review_gradient_boosting_reg'
        try:
            self.review_gradient_boosting_reg = self.loadJoblibObject(s)
            print s+' object has been loaded'
        except IOError:
            print s+' object not found. Creating it...'
            self.review_gradient_boosting_reg = []
            for i in range(self.nb_journals): 
                self.review_gradient_boosting_reg.append(GradientBoostingRegressor())
                self.review_gradient_boosting_reg[i].fit(self.predict_features, self.predict_labels_reviews[:,i])
            self.dumpJoblibObject(self.review_gradient_boosting_reg, s)

    def loadPrizeRandomForestRegressors(self):
        s = 'prize_random_forest_reg'
        try:
            self.prize_random_forest_reg = self.loadJoblibObject(s)
            print s+' object has been loaded'
        except IOError:
            print s+' object not found. Creating it...'
            self.prize_random_forest_reg = []
            for i in range(self.nb_considered_prizes):
                self.prize_random_forest_reg.append(RandomForestRegressor())
                self.prize_random_forest_reg[i].fit(self.predict_features, self.predict_labels_prizes[:,i])
            self.dumpJoblibObject(self.prize_random_forest_reg, s)

    def loadPrizeLogisticRegression(self):
        s = 'prize_logistic_reg'
        try:
            self.prize_logistic_reg = self.loadJoblibObject(s)
            print s+' object has been loaded'
        except IOError:
            print s+' object not found. Creating it...'
            self.prize_logistic_reg = []
            for i in range(self.nb_considered_prizes): 
                self.prize_logistic_reg.append(LogisticRegression())
                self.prize_logistic_reg[i].fit(self.predict_features, self.predict_labels_prizes[:,i])
            self.dumpJoblibObject(self.prize_logistic_reg, s)


### SEARCH ###    
    def search_request(self, args):
        if args.has_key('id') and args.has_key('nbresults') and args.has_key('criteria'):
            if (args['nbresults'].__class__==int) and (args['criteria'].__class__==dict):
                nbresults = args['nbresults']
                crit = args['criteria']
                try:
                    crit_act_dir = crit['actor_director']
                    crit_genre = crit['genre']
                    crit_budget = crit['budget']
                    crit_review = crit['review']
                    if (crit_act_dir.__class__ == bool) and (crit_genre.__class__==bool) and (crit_budget.__class__==bool) and (crit_review.__class__==bool):
                        if not (crit_act_dir or crit_genre or crit_budget or crit_review):
                            raise ParsingError('All criteria are equal to false. Please select at least one criterion.')
                        try:
                            film = Film.objects.get(imdb_id=args['id'])
                            if args.has_key('filter'):
                                results = self.compute_search(film, nbresults, crit, filters = self.parse_search_filter(args['filter']) )
                            else:
                                results = self.compute_search(film, nbresults, crit)
                            query_results = {'nbresults' : nbresults, 'results' : [], 'img' : film.image_url if film.image_url else "poster/"+f.imdb_id}
                            for (v, f) in results:
                                query_results['results'].append(
                                    {'id': f.imdb_id,
                                     'orignal_title': f.original_title,
                                     'title' : f.english_title,
                                     'img' : f.image_url if f.image_url else "poster/"+f.imdb_id,
                                     'value' : v}
                                    )
                            return query_results
                        except Film.DoesNotExist:
                            raise ParsingError('No film with imdb_id ' + args['id'] + '.')
                    else:
                        raise ParsingError('Criteria must be boolean.')
                except KeyError:
                    raise ParsingError('Missing criterium.')
            else:
                raise ParsingError('Wrong format for nbresults or criteria.')
        else:
            raise ParsingError('Please define the IMDb identfier, the number of expected results and search criteria.')
   
    def applySearchFilter(self,filters): #returns indexes of films that respect our filters 
        # Filter budget
        if filters.has_key('budget'):
            indexes_fitting_filters = self.budget_matrix.toarray() >= filters['budget']['min']
            indexes_fitting_filters = indexes_fitting_filters * (self.budget_matrix.toarray() <= filters['budget']['max'])
        # Filter release_date
        if filters.has_key('release_period'):
            years=self.release_date_matrix[:,self.release_date_names.index('year')].toarray()
            aux_max_release_date = years <= filters['release_period']['end']
            aux_min_release_date = years >= filters['release_period']['begin']
            indexes_fitting_filters = indexes_fitting_filters * aux_max_release_date 
            indexes_fitting_filters = indexes_fitting_filters * aux_min_release_date
        # Filter reviews
        if filters.has_key('reviews'):
            indexes_fitting_filters = indexes_fitting_filters * (self.metacritic_score_matrix.toarray() >= filters['reviews']['min'])
        # Filter genres
        if filters.has_key('genres'):
            if filters['genres']!=[]:
                aux_genres = np.zeros(indexes_fitting_filters.shape)
                for genre in filters['genres']:
                    aux_genres = aux_genres + (self.genres_matrix[:,self.genres_names.index(genre.name)].toarray())
                indexes_fitting_filters = indexes_fitting_filters * (aux_genres != 0)
        # Filter directors
        if filters.has_key('directors'):
            if filters['directors']!=[]:
                aux_directors = np.zeros(indexes_fitting_filters.shape)
                for director in filters['directors']:
                    aux_directors = aux_directors + (self.director_matrix[:,self.director_names.index(director.imdb_id)].toarray())
                indexes_fitting_filters = indexes_fitting_filters * (aux_directors != 0)
        # Filter actors
        if filters.has_key('actors'):
            if filters['actors']!=[]:
                aux_actors = np.zeros(indexes_fitting_filters.shape)
                for actor in filters['actors']:
                    aux_actors = aux_actors + (self.actor_matrix[:,self.actor_names.index(actor.imdb_id)].toarray())
                indexes_fitting_filters = indexes_fitting_filters * (aux_actors != 0)
        # Return results
        indexes_fitting_filters = indexes_fitting_filters.reshape(1,indexes_fitting_filters.shape[0])[0]
        indexes_fitting_filters = np.where(indexes_fitting_filters==1)[0]
        return list(indexes_fitting_filters)

    def compute_search(self, film, nb_results, criteria, filters=None):
        try:
            film_index = self.fromPktoIndex[film.pk]
        except KeyError:
            raise ParsingError("Film not found.")
        # Select cluster information according to criteria
        if self.clustering_type_in_searchclustering == 'SC':
            self.search_clustering = self.search_clustering_SC
        if self.clustering_type_in_searchclustering == 'KM':
            self.search_clustering = self.search_clustering_KM
        criteria_binary = criteria['actor_director'] + 2*criteria['budget'] + 4*criteria['review'] + 8*criteria['genre']
        search_clustering = self.search_clustering[criteria_binary]
        labels = search_clustering['labels']
        cluster_centers = search_clustering['cluster_centers']
        # Apply filters
        #print('--> Applying filters...')
        if filters!=None:
            indexes_fitting_filters = self.applySearchFilter(filters)
        else:
            indexes_fitting_filters = range(self.nb_films)
        indexes_fitting_filters = np.array(indexes_fitting_filters)
        #print('--> Start looking for neighbors...')
        # Find neighbors
        # 30 % time can be saved here with cache
        X = self.getWeightedSearchFeatures(criteria_binary).toarray()
        nb_results_found=0
        distances=[]
        neighbors_indexes=[]
        if len(indexes_fitting_filters) >= self.min_nb_of_films_to_use_clusters_in_search:
            distance_to_each_cluster = []
            distance_to_each_cluster = np.array([np.linalg.norm(X[film_index]-cluster_center,self.p_norm) for cluster_center in cluster_centers])
            clusters_by_distance = distance_to_each_cluster.argsort()
            for cluster in clusters_by_distance:
                if nb_results_found < nb_results +1:
                    #print('--> Looking in cluster '+str(cluster)+' ('+str(nb_results_found)+' results found yet)')
                    indexes_of_cluster = np.where(labels == cluster)[0]
                    indexes = np.intersect1d(indexes_of_cluster, indexes_fitting_filters)
                    if len(indexes)>0:
                        samples = X[list(indexes),:]
                        neigh = NearestNeighbors(n_neighbors=(nb_results-nb_results_found)+1, p=self.p_norm)
                        neigh.fit(samples)
                        (loc_distances,loc_neighbors_indexes) = neigh.kneighbors(X[film_index])
                        local_nb_results_found = loc_distances[0].shape[0]
                        #print('--> Found '+str(local_nb_results_found)+' results in this cluster')
                        nb_results_found = nb_results_found + local_nb_results_found
                        distances.append(loc_distances[0])
                        neighbors_indexes.append(indexes[loc_neighbors_indexes[0]])
        else: # no need to use clusters
            indexes = indexes_fitting_filters
            samples = X[list(indexes),:]
            neigh = NearestNeighbors(n_neighbors=nb_results+1, p=self.p_norm)
            neigh.fit(samples)
            (loc_distances,loc_neighbors_indexes) = neigh.kneighbors(X[film_index])
            distances.append(loc_distances[0])
            neighbors_indexes.append(indexes[loc_neighbors_indexes[0]])
        if len(neighbors_indexes)>0:
            neighbors_indexes = np.concatenate(neighbors_indexes)
            distances = np.concatenate(distances)
            distances = distances[1:] # because the film being studied is the closest neighbor...
            neighbors_indexes = neighbors_indexes[1:]
            #Now we reorder items because they may be unordered if there are filters
            new_order = distances.argsort()
            distances = distances[new_order]
            neighbors_indexes = neighbors_indexes[new_order]
        #Return results
        res = []
        for i in range(len(distances)):
            res.append( (distances[i], Film.objects.get(pk = self.fromIndextoPk[ neighbors_indexes[i]])) ) 
        return res

    def parse_search_filter(self, filt_in):
        if filt_in.__class__ != dict:
            return None
        
        filt_out = {}
        
        if filt_in.has_key('actors'):
            if filt_in['actors'].__class__ == list:
                filt_out['actors'] = []
                for person_id in filt_in['actors']:
                    try:
                        filt_out['actors'].append( Person.objects.get(imdb_id=str(person_id)) )
                    except Person.DoesNotExist:
                        continue
        
        if filt_in.has_key('directors'):
            if filt_in['directors'].__class__ == list:
                filt_out['directors'] =[]
                for person_id in filt_in['directors']:
                    try:
                        filt_out['directors'].append( Person.objects.get(imdb_id=str(person_id)) )
                    except Person.DoesNotExist:
                        pass
        
        if filt_in.has_key('genres'):
            if filt_in['genres'].__class__ == list:
                filt_out['genres'] =[]
                for person_id in filt_in['genres']:
                    try:
                        filt_out['genres'].append( Genre.objects.get(name=str(person_id)) )
                    except Person.DoesNotExist:
                        pass
        try:
            if (filt_in['budget']['min'].__class__==int) and (filt_in['budget']['max'].__class__ == int):
                filt_out['budget'] = {}
                filt_out['budget']['min'] = 1000000.*filt_in['budget']['min']
                filt_out['budget']['max'] = 1000000.*filt_in['budget']['max']
        except exceptions.KeyError:
            pass
        
        try:
            if (filt_in['reviews']['min'].__class__ == float or filt_in['reviews']['min'].__class__ == int):
                filt_out['reviews'] =  {}
                filt_out['reviews']['min'] = 100*float(filt_in['reviews']['min'])
        except exceptions.KeyError:
            pass
        
        filt_out['release_period'] = {'begin' :1901, 'end': 2020}
        try:
            filt_out['release_period']['begin'] = filt_in['release_period']['begin']
        except exceptions.ValueError, exceptions.KeyError:
            pass
        try:
            filt_out['release_period']['end'] = filt_in['release_period']['end']
        except exceptons.ValueError, exceptions.KeyError:
            pass
        
        return filt_out


### PREDICTION ###
    def get_bagofwords(predicted_score, input_genres):
        accuracy = 4.
        # le niveau de précision qui détermine quelles notes on considère comme proches de la note du film virtuel
        # On sélectionne d'abord les critiques pertinentes pour élaborer le bag of words :
        corpus = []
        for i in range(self.nb_films):
            # on retient le film n° i s'il est de l'un des genres voulus...
            if max([self.genres_matrix[i, genre] == input_genres[genre] == 1 for genre in range(self.nb_genres)]):
               # ... et on retient alors les critiques de ce film dont la note est proche de predicted_score :
                for journal in self.reviews_content[i].keys():
                    journal_index = self.reviews_names.index(journal)
                    if abs(predicted_score - self.reviews_matrix[i, journal_index]) < .5/accuracy:
                        corpus.append(self.reviews_content[i][journal])
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
        return [{'keyword' : inv_dic[i], 'value': y[i]} for i in top_indexes if y[i] > 1]
# on sélectionne les 10 adjectifs les plus utilisés et on les retourne avec un poids égal à leur nombre d'occurences

    def compute_predict(self, x_vector):
        '''
        Return {'prizes' : list of {'institution' : Institution name,
                                    'win' : boolean,
                                    'value' : probability
                                   },
                'box_office' : int,
                'reviews' : list of {'journal': Journal name,
                                     'grade' : float,
                                    },
                'bag_of_words' : list of {'keyword' : Keyword name,
                                          'value' : float dans [0,1]
                                         }
               }
        '''
        
        # Box office
        predicted_box_office = np.exp(self.log_box_office_gradient_boosting_reg.predict(x_vector)[0])
       
        # Reviews
        journals = []
        predicted_grades = []
        for i in range(self.nb_journals):
            journals.append(self.reviews_names[i])
            predicted_grades.append(self.review_gradient_boosting_reg[i].predict(x_vector)[0])

        # Prizes
        institutions = []
        wins = []
        predicted_probabilities = []
        for i in range(self.nb_considered_prizes):
            institutions.append(self.predict_labels_prizes_names[i].split('_')[1])
            if self.predict_labels_prizes_names[i].split('_')[2] == 'True':
                wins.append(True)
            else:
                wins.append(False)
            predicted_probabilities.append(
                self.prize_logistic_reg[i].predict_proba(x_vector)[0,1]
            )

        # Bag of words
        x_genres_vector = x_vector[-self.nb_genres:]
        bagofwords = self.get_bagofwords(np.mean(predicted_grades), x_genres_vector)
        
        results = {'prizes_win' : [{'institution' : institutions[i],
                                    'value' : predicted_probabilities[i]} 
                                   for i in range(len(institutions)) if wins[i]],
                   'prizes_nomination' : [{'institution' : institutions[i],
                                           'value' : predicted_probabilities[i]}
                                          for i in range(len(institutions)) if not wins[i]],
                   'box_office' : predicted_box_office,
                   'reviews' : [{'journal' : journals[i],
                                 'grade' : predicted_grades[i]} 
                                for i in range(self.nb_journals)],
                   'bag_of_words' : []
                    }

        return results

    def predict_request(self, args):
        # Get results
        results = self.compute_predict(self.vectorize_predict_user_input(args))
        # Build query_results
        query_results = {}
        
        # Fill query_results['prizes']
        query_results['prizes_win'] = results['prizes_win']
        query_results['prizes_nomination'] = results['prizes_nomination']
        query_results['prizes_win'] = sorted(query_results['prizes_win'], key=lambda k: -k['value'])
        query_results['prizes_win'] = query_results['prizes_win'][:10]
        query_results['prizes_nomination'] = sorted(query_results['prizes_nomination'], key=lambda k: -k['value'])
        query_results['prizes_nomination'] = query_results['prizes_nomination'][:10]

        # Fill query_results['general_box_office'] 
        
        bo = self.box_office_matrix.toarray().ravel()
        sorted_bo = np.sort(bo)
        sorted_bo_indices = np.argsort(bo)
        invrank = np.searchsorted(sorted_bo, results['box_office'])

        rank = (self.nb_films+1) - invrank

        neighbors = []
        
        if rank<self.nb_films+1:
            k = sorted_bo_indices[invrank - 1]
            lower_neighbor = {'english_title': self.film_names[k],
                              'rank' : rank + 1,
                              'value' : bo[k]}
        else: #our film is last
            lower_neighbor = {'english_title': '-',
                              'rank' : rank + 1,
                              'value' : 0}       
        
        if rank>1:
            k = sorted_bo_indices[invrank]
            upper_neighbor = {'english_title': self.film_names[k],
                              'rank' : rank - 1,
                              'value' : bo[k]}
        else: # our film is first
            upper_neighbor = {'english_title': '-',
                              'rank' : rank - 1,
                              'value' : 0}
        
        neighbors.append(lower_neighbor)
        neighbors.append(upper_neighbor)
        neighbors = sorted(neighbors, key=lambda k: k['rank'])

        general_box_office = {'rank': rank,
                              'value': results['box_office'],
                              'neighbors': neighbors}
                              #'upper_neighbor': upper_neighbor,
                              #'lower_neighbor': lower_neighbor}
        
        query_results['general_box_office'] = general_box_office
        
        # Fill query_results['genre_box_office']
       
        if args.has_key('genres'):
            if args['genres'].__class__ == list:
                genres_list = np.zeros(self.nb_genres)
                for genre in args['genres']:
                    try:
                        genres_list[self.genres_names.index(genre)] = 1
                    except IndexError:
                        continue
                useful_indexes = np.where(self.genres_matrix * genres_list > 0)
                bo_genre = bo[useful_indexes]
                sorted_bo_genre = np.sort(bo_genre)
                sorted_bo_indices_genre = np.argsort(bo_genre)
                invrank_genre = np.searchsorted(sorted_bo_genre, results['box_office'])

                rank_genre = (self.nb_films +1 )- invrank_genre

                neighbors_genre = []
        
                if rank_genre < self.nb_films+1:
                    k = sorted_bo_indices_genre[invrank_genre - 1]
                    lower_neighbor_genre = {
                        'english_title': self.film_names[k],
                        'rank' : rank_genre + 1,
                        'value' : bo[k]}
                else: #our film is last
                    lower_neighbor_genre = {
                        'english_title': '',
                        'rank' : rank_genre + 1,
                        'value' : 0}

                if rank_genre>1:
                    k = sorted_bo_indices_genre[invrank_genre]
                    upper_neighbor_genre = {'english_title': self.film_names[k],
                                            'rank' : rank_genre - 1,
                                            'value' : bo[k]}
                else:
                    upper_neighbor_genre = {'english_title': '',
                                           'rank' : rank_genre - 1,
                                           'value' : 0}
                
                neighbors_genre.append(lower_neighbor_genre)
                neighbors_genre.append(upper_neighbor_genre)
                neighbors_genre = sorted(neighbors_genre, key=lambda k: k['rank'])

                genre_box_office = {'rank': rank_genre,
                                    'value': results['box_office'],
                                    'neighbors': neighbors_genre}
                                    #'upper_neighbor': upper_neighbor_genre,
                                    #'lower_neighbor': lower_neighbor_genre}
        
                query_results['genre_box_office'] = genre_box_office

        # Fill query_results['critics']
        critics = {}
        
        reviews = results['reviews']
        grades = map(lambda k: k['grade'], reviews)
        reviews = sorted(reviews, key=lambda k: -k['grade'])
        n_reviews = len(reviews)
        selected_reviews = []
        selected_reviews.append(reviews[0])
        selected_reviews.append(reviews[1*n_reviews/4])
        selected_reviews.append(reviews[2*n_reviews/4])
        selected_reviews.append(reviews[3*n_reviews/4])
        selected_reviews.append(reviews[-1])

        critics['reviews'] = selected_reviews
        critics['average'] = np.mean(grades)
        query_results['critics'] = critics
        
        # Fill query_results['bag_of_words']
        bag_of_words = []
        for item in results['bag_of_words']:
            bag_of_words.append({'word' : item['keyword'],
                                 'value' : item['value']})
        query_results['bag_of_words'] = bag_of_words
        
        # Return data
        return query_results

    def vectorize_predict_user_input(self, user_input):
        x_actor_vector = np.zeros([1,self.nb_actors])
        if user_input.has_key('actors'):
            if user_input['actors'].__class__ == list:
                for actor_id in user_input['actors']:
                    try:
                        x_actor_vector[0,self.actor_names.index(actor_id)]=1
                    except ValueError:
                        pass

        if self.reduction_actors_in_predictfeatures == 'KM':
            x_actor_reduced = x_actor_vector * self.proj_actors_KM
        if self.reduction_actors_in_predictfeatures == 'SC':
            x_actor_reduced = x_actor_vector * self.proj_actors_SC
        if self.reduction_actors_in_predictfeatures == 'BOC':
            x_actor_reduced = x_actor_vector * self.proj_actors_BOC

        x_genres_vector = np.zeros([1, self.nb_genres])
        if user_input.has_key('genres'):
            if user_input['genres'].__class__ == list:
                for genre in user_input['genres']:
                    try:
                        x_genres_vector[0,self.genres_names.index(genre)]=1
                    except ValueError:
                        pass
 
        x_director_vector = np.zeros([1, self.nb_directors])
        if user_input.has_key('directors'):
            if user_input['directors'].__class__ == list:
                for director_id in user_input['directors']:
                    try:
                        x_director_vector[0,self.director_names.index(director_id)]=1
                    except ValueError:
                        pass

        if self.reduction_directors_in_predictfeatures == 'KM':
            x_director_reduced = x_director_vector * self.proj_directors_KM
        if self.reduction_directors_in_predictfeatures == 'SC':
            x_director_reduced = x_director_vector * self.proj_directors_SC

        x_keyword_vector = np.zeros([1, self.nb_keywords])
        if user_input.has_key('keywords'):
            if user_input['keywords'].__class__ == list:
                for keyword in user_input['keywords']:
                    try:
                        x_keyword_vector[0,self.keyword_names.index(keyword)]=1
                    except ValueError:
                        pass

        x_keyword_reduced = x_keyword_vector * self.proj_keywords_KM

        x_budget_vector = np.zeros([1,1])
        if user_input.has_key('budget'):
            if user_input['budget'].__class__ == int:
                x_budget_vector[0,0] = float(user_input['budget'])

        x_season_vector = np.zeros([1, len(self.season_names)]) # Default Season?
        try:
            for feat in self.season_names:
                i = 0
                if re.findall(user_input['release_period']['season'], feat):
                    x_season_vector[0,i] = 1
                i += 1
        except exceptions.KeyError:
            pass

        x_vector = np.hstack([
            x_actor_reduced,
            x_director_reduced,
            x_keyword_reduced,
            x_budget_vector,
            x_season_vector,
            x_genres_vector,])
        return x_vector
        
### KEYWORDS SUGGESTION ###
    def suggest_keywords(self, args):
        if args.has_key('str') and args.has_key('nbresults'):
            if args['nbresults'].__class__ == int and args['nbresults'] >= 0:
                tot = np.zeros(self.nb_keywords)
                rex = re.compile(args['str'].lower())
                found = [(rex.search(m)!=None) for m in self.keyword_names]
                if args.has_key('filter') and args['filter'].__class__ == list:
                    for element in args['filter']:
                        try:
                            value, genre = element
                            tot += found * (value * self.keywordsbygenre[self.genres_names.index(genre)].toarray()[0,:])
                        except ValueError:
                            raise ParsingError('Unfound genre ' + genre + '.')
                else:
                    tot = found * np.sum(self.keyword_matrix.toarray(), axis=0)
                ind = list(np.argsort(-tot)[:min(args['nbresults'], self.nb_films)])
                results = []
                for i in ind:
                    if np.abs(tot[i]) > 0:
                        results.append( (tot[i], self.keyword_names[i] ) )
                return {'results' : results}
            else:
                raise ParsingError('Wrong format for nbresults.')
        else:
            raise ParsingError('Please define a string and the expected number of results.')
