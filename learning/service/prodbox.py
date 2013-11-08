from objects import *
from vectorizers import *
from status.models import TableUpdateTime
from cinema.models import Film, Person, Genre, Keyword, Journal, Institution
import filmsfilter as flt
from dimreduce import *

import numpy as np
import scipy

from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize, Imputer
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import SpectralClustering
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import cross_val_score
from sklearn.neighbors.kde import KernelDensity

import datetime
from time import time
import dateutil.parser
import re

import exceptions

from scipy.stats import poisson

class TableDependentCachedObject(CachedObject):
    def __init__(self, name, table_name, content = None):
        __init__(self, name, content = content)
        self.table_name = table_name
    
    def update_status(self):
        try:
            field = TableUpdateTime.objects.get(model_name = self.table_name)
            if field.update_time > self.version:
                self.modified = True
        except TableUpdateTime.DoesNotExist:
            print('Table "' + self.table_name + ' not found.')

class CinemaService(LearningService):
    
    def loadFilms(self):
        self.films = flt.getFilms()
        if not self.is_loaded('films'):
            self.fromPktoIndex, self.fromIndextoPk = hashIndexes(self.films.iterator())
            self.create_cobject('films', (self.fromPktoIndex, self.fromIndextoPk))
        else:
            self.fromPktoIndex, self.fromIndextoPk = self.get_cobject('films').get_content()
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

            self.budget_bandwidth = 1000.0 # TODO : optimize this parameter
            budget_data = self.budget_matrix.data[-np.isnan(self.budget_matrix.data)]
            budget_data = budget_data.reshape( [budget_data.shape[0], 1])
            kde = KernelDensity(kernel='gaussian', bandwidth=self.budget_bandwidth).fit(budget_data)
            # 

            for i in range(self.budget_matrix.shape[0]):
                if np.isnan(self.budget_matrix[i,0]):
                    self.budget_matrix[i,0]= kde.sample(1)
            #completer = Imputer(missing_values=-1)
            #completer.fit(self.budget_matrix)
            #self.budget_matrix = completer.transform(self.budget_matrix)
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
    
    def loadReviewsContent(self):
        # TODO : finish implementation
        gkey = genReviewsContent(self.films.iterator())
        self.reviews_content = []
        for d in gkey:
            self.reviews_content.append(d.values())

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

    def loadActorsReduced2(self):
        # Third method : heuristic
        theta = 0.5
        actor_weight_matrix = self.rank_matrix
        rv = poisson(theta)
        actor_weight_matrix.data = rv.pmf(actor_weight_matrix.data).astype(np.float32)
        self.actors_share_bo = normalize(actor_weight_matrix.todense(), axis=1, norm='l1').T * self.box_office_matrix
        

    def loadActorsReduced(self):
        if not self.is_loaded('actors_reduced'):
            # First clustering method: Spectral Clustering
            # First we filter the actor_matrix IOT keep only high rank relationships 
            actor_matrix = scipy.sparse.csr_matrix(self.actor_matrix.toarray() * (self.rank_matrix.toarray()>=self.actor_reduction_rank_threshold))
            try:
                actors_SC = SpectralClustering(n_clusters=self.dim_actors,eigen_solver='arpack',affinity="nearest_neighbors",n_neighbors=self.n_neighbors_SC_actors)
                actor_labels_SC = actors_SC.fit_predict(actor_matrix.transpose())
                self.proj_actors_SC = scipy.sparse.csc_matrix(actor_labels_SC==0, dtype=int).transpose()
                for i in range(1, self.dim_actors):
                    self.proj_actors_SC = scipy.sparse.hstack([self.proj_actors_SC, scipy.sparse.csc_matrix(actor_labels_SC==i, dtype=int).transpose()])
                self.proj_actors_SC=normalize(self.proj_actors_SC.astype(np.double), norm='l1', axis=0)
                self.actor_reduced_SC = actor_matrix * self.proj_actors_SC
            except MemoryError:
                self.actor_reduced_SC = None
                print('Spectral clustering failed for actors due to memory error')
            # Second clustering method: KMeans clustering with tf-idf
            actors_KM = KMeans(n_clusters = self.dim_actors, init='k-means++')
            actor_labels_KM = actors_KM.fit_predict(TfidfTransformer().fit_transform(self.actor_matrix).transpose())
            self.proj_actors_KM = scipy.sparse.csc_matrix(actor_labels_KM==0, dtype=int).transpose()
            for i in range(1, self.dim_actors):
                self.proj_actors_KM = scipy.sparse.hstack([self.proj_actors_KM, scipy.sparse.csc_matrix(actor_labels_KM==i, dtype=int).transpose()])
            self.proj_actors_KM=normalize(self.proj_actors_KM.astype(np.double),axis=0, norm='l1')
            self.actor_reduced_KM = self.actor_matrix * self.proj_actors_KM

            # Save object in cache
            self.create_cobject('actors_reduced', (self.actor_reduced_SC, self.proj_actors_SC, self.actor_reduced_KM, self.proj_actors_KM))
        else:
            self.actor_reduced_SC, self.proj_actors_SC, self.actor_reduced_KM, self.proj_actors_KM = self.get_cobject('actors_reduced').get_content()
  
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
        self.nb_writers = len(self.writer_names)
    
    def loadWritersReduced(self):
        if not self.is_loaded('writers_reduced'):
            # First clustering method: Spectral Clustering
            try:
                writer_SC = SpectralClustering(n_clusters=self.dim_writers,eigen_solver='arpack',affinity="nearest_neighbors",n_neighbors=self.n_neighbors_SC_writers)
                writer_labels_SC = writer_SC.fit_predict(self.writer_keyword_matrix)
                self.proj_writers_SC = scipy.sparse.csc_matrix(writer_labels_SC==0, dtype=int).transpose()
                for i in range(1, self.dim_writers):
                    self.proj_writers_SC = scipy.sparse.hstack([self.proj_writers_SC, scipy.sparse.csc_matrix(writer_labels_SC==i, dtype=int).transpose()])
                self.proj_writers_SC=normalize(self.proj_writers_SC.astype(np.double),axis=0, norm='l1')
                self.writer_reduced_SC = self.writer_matrix * self.proj_writers_SC
            except MemoryError:
                self.writer_reduced_SC = None
                print('Spectral clustering failed for writers due to memory error')
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
            self.create_cobject('writers_reduced', (self.writer_reduced_SC, self.proj_writers_SC, self.writer_reduced_avg, self.writer_reduced_KM))
        else:
            self.writer_reduced_SC, self.proj_writers_SC, self.writer_reduced_avg, self.writer_reduced_KM = self.get_cobject('writers_reduced').get_content()

    def loadDirectors(self):
        if self.reduction_actors_in_directoractormatrix == 'KM':
            actor_reduced = self.actor_reduced_KM
        if self.reduction_actors_in_directoractormatrix == 'SC':
            actor_reduced = self.actor_reduced_SC
        if not self.is_loaded('directors'):
            v=DictVectorizer(dtype=int)
            self.director_matrix = v.fit_transform(genDirectors(self.films.iterator()))
            self.director_names = v.get_feature_names()
            self.director_actor_matrix = normalize(self.director_matrix.transpose().astype(np.double), norm='l1', axis=1) * actor_reduced
            # Save object in cache
            self.create_cobject('directors', (self.director_matrix, self.director_names, self.director_actor_matrix))
        else:
            self.director_matrix, self.director_names, self.director_actor_matrix = self.get_cobject('directors').get_content()
        self.nb_directors = len(self.director_names)
    
    def loadDirectorsReduced(self):
        if not self.is_loaded('directors_reduced'):
            # First clustering method: Spectral Clustering
            try:
                director_SC = SpectralClustering(n_clusters=self.dim_directors,eigen_solver='arpack',affinity="nearest_neighbors",n_neighbors=self.n_neighbors_SC_directors)
                director_labels_SC = director_SC.fit_predict(self.director_actor_matrix)
                self.proj_directors_SC = scipy.sparse.csc_matrix(director_labels_SC==0, dtype=int).transpose()
                for i in range(1, self.dim_directors):
                    self.proj_directors_SC = scipy.sparse.hstack([self.proj_directors_SC, scipy.sparse.csc_matrix(director_labels_SC==i, dtype=int).transpose()])
                self.proj_directors_SC=normalize(self.proj_directors_SC.astype(np.double),axis=0, norm='l1')
                self.director_reduced_SC = self.director_matrix * self.proj_directors_SC
            except MemoryError:
                self.director_reduced_SC = None
                print('Spectral clustering failed for directors due to memory error')
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
            self.create_cobject('directors_reduced', (self.director_reduced_SC, self.proj_directors_SC, self.director_reduced_avg, self.director_reduced_KM, self.proj_directors_KM))
        else:
            self.director_reduced_SC, self.proj_directors_SC, self.director_reduced_avg, self.director_reduced_KM, self.proj_directors_KM = self.get_cobject('directors_reduced').get_content()

    def loadSearchClustering(self):
        if not self.is_loaded('search_clustering'):
            self.search_clustering = {}
            for k in range(16):
                print('Doing search clustering number '+str(k+1)+'/16')
                X = self.getWeightedSearchFeatures(k)
                KM = KMeans(n_clusters=self.n_clusters_search)
                KM.fit_predict(X)
                self.search_clustering[k] = {'labels' : KM.labels_, 'cluster_centers' : KM.cluster_centers_}
            # Save object in cache
            self.create_cobject('search_clustering',self.search_clustering)
        else:
            self.search_clustering = self.get_cobject('search_clustering').get_content()

    def loadPredictFeatures(self):
        if self.reduction_actors_in_predictfeatures == 'KM':
            actor_reduced = self.actor_reduced_KM
        if self.reduction_actors_in_predictfeatures == 'SC':
            actor_reduced = self.actor_reduced_SC
        
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
        self.predict_labels_prizes_names = ['prize_' + s for s in self.prizes_names] # a priori inutile

    def getWeightedSearchFeatures(self,k):
        if self.reduction_actors_in_searchclustering == 'SC':
            actor_reduced=self.actor_reduced_SC
        if self.reduction_actors_in_searchclustering == 'KM':
            actor_reduced=self.actor_reduced_KM
        if self.reduction_directors_in_searchclustering == 'SC':
            director_reduced=self.director_reduced_SC
        if self.reduction_directors_in_searchclustering == 'KM':
            director_reduced=self.director_reduced_KM
        #print actor_reduced.toarray()[0:10,:]
        X_people = scipy.sparse.hstack([normalize(actor_reduced.astype(np.double),norm='l1',axis=1),normalize(director_reduced.astype(np.double),norm='l1',axis=1)])
        #TODO:play on clustering types
        X_budget = self.budget_matrix
        X_review = self.reviews_matrix
        X_genre =  self.genres_matrix
        X_budget = scipy.sparse.csr_matrix(np.log(X_budget.toarray()))
        X_budget = X_budget/max(X_budget.data)
        X_review = X_review/100 # because grades should be in [0,1] #TODO WARNING BDD DAVID OU BENJAMIN
        X_review = normalize(X_review.astype(np.double),norm='l1',axis=1) #normalize
        X_genre = normalize(X_genre.astype(np.double),norm='l1',axis=1) #normalize
        X_people = X_people/2 #normalize
        people_weight = self.high_weight if (k>>0)%2 else self.low_weight
        budget_weight = self.high_weight if (k>>1)%2 else self.low_weight
        review_weight = self.high_weight if (k>>2)%2 else self.low_weight
        genre_weight = self.high_weight if (k>>3)%2 else self.low_weight
        res = scipy.sparse.hstack([people_weight*X_people, budget_weight*X_budget, review_weight*X_review, genre_weight*X_genre])
        return res
        
    def __init__(self):
        super(CinemaService, self).__init__()
        # TODO: also try log of budget for testing search requests
        # TODO manage projectors of each clustering
        # Define parameters # TODO : optimize all these parameters
        self.dim_writers = 20
        self.dim_directors = 10
        self.dim_actors = 20
        self.dim_keywords = 30
        self.n_clusters_search = 20
        self.p_norm = 2 # p-norm used for distances
        self.high_weight = 1 # for the distance definition
        self.low_weight = 0 # for the distance definition
        self.n_neighbors_SC_actors = 8 # soectral clustering parameter
        self.n_neighbors_SC_writers = 8 # soectral clustering parameter
        self.n_neighbors_SC_directors = 8 # soectral clustering parameter
        self.actor_reduction_rank_threshold = 10
        self.reduction_actors_in_predictfeatures = 'SC'
        #self.reduction_keywords_in_predictfeatures = 'KM'
        self.reduction_directors_in_predictfeatures = 'SC'
        self.reduction_actors_in_directoractormatrix = 'SC'
        self.reduction_actors_in_searchclustering = 'SC'
        self.reduction_directors_in_searchclustering = 'SC'
        assert self.dim_keywords >= self.dim_writers, 'dim_writers should be lower than dim_keywords' 
        assert self.dim_actors >= self.dim_directors, 'dim_directors should be lower than dim_actors' 
        # Load films data
        self.loadFilms()
        # Load prediction features
        self.loadActors()
        self.loadStars()
        self.loadRanks()
        self.loadActorsReduced()
        self.loadDirectors()
        self.loadDirectorsReduced()
        self.loadSeason()
        self.loadBudget()
        self.loadKeywords()        
        self.loadKeywordsReduced()
        self.loadGenres()
        # Load prediction labels
        self.loadBoxOffice()
        self.loadPrizes()
        self.loadReviews()
        #self.loadReviewsContent() # TODO : finish implementation
        # Load other features
        self.loadStats()
        self.loadWriters()
        self.loadWritersReduced()
        self.loadRuntime()
        self.loadMetacriticScore()
        self.loadReleaseDate()
        self.loadProductionCompanies()
        self.loadImdb()
        self.loadCountries()
        self.loadLanguages()
        # Load search clusterings
        self.loadSearchClustering()
        # Load predict features
        self.loadPredictFeatures()
        self.loadPredictLabels()
        # Init predict classifier
        self.init_predict()
        print('Loadings finished. Server now running.')
    
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
                            query_results = {'nbresults' : nbresults, 'results' : []}
                            for (v, f) in results:
                                query_results['results'].append(
                                    {'id': f.imdb_id,
                                     'orignal_title': f.original_title,
                                     'title' : f.english_title,
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
   
    def applyFilter(self,filters): #returns indexes of films that respect our filters 
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
        print filters
        try:
            film_index = self.fromPktoIndex[film.pk]
        except KeyError:
            raise ParsingError("Film not found.")
        # Select cluster information according to criteria
        criteria_binary = criteria['actor_director'] + 2*criteria['budget'] + 4*criteria['review'] + 8*criteria['genre']
        search_clustering = self.search_clustering[criteria_binary]
        labels = search_clustering['labels']
        cluster_centers = search_clustering['cluster_centers']
        # Apply filters
        #print('--> Applying filters...')
        if filters!=None:
            indexes_fitting_filters = self.applyFilter(filters)
        else:
            indexes_fitting_filters = range(self.nb_films)
        indexes_fitting_filters = np.array(indexes_fitting_filters)
        #print('--> Start looking for neighbors...')
        # Find neighbors
        # 30 % time can be saved here with cache
        X = self.getWeightedSearchFeatures(criteria_binary).toarray()
        distance_to_each_cluster = []
        distance_to_each_cluster = np.array([np.linalg.norm(X[film_index]-cluster_center,self.p_norm) for cluster_center in cluster_centers])
        clusters_by_distance = distance_to_each_cluster.argsort()
        nb_results_found=0
        distances=[]
        neighbors_indexes=[]
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

    def loadLogBoxOfficeRandomForestRegressor(self):
        s = 'log_box_office_random_forest_reg'
        try:
            self.log_box_office_random_forest_reg = self.loadJoblibObject(s)
        except IOError:
            print s+' object not found. Creating it...'
            self.log_box_office_random_forest_reg = RandomForestRegressor()
            self.log_box_office_random_forest_reg.fit(self.predict_features, self.predict_labels_log_box_office)
            self.dumpJoblibObject(self.log_box_office_random_forest_reg, s)

    def loadReviewRandomForestRegressors(self):
        s = 'review_random_forest_reg'
        try:
            self.review_random_forest_reg = self.loadJoblibObject(s)
        except IOError:
            print s+' object not found. Creating it...'
            self.review_random_forest_reg = []
            for i in range(len(self.reviews_names)): #TODO : stocker un self.nb_journals pour eviter le len()
                self.review_random_forest_reg.append(RandomForestRegressor())
                self.review_random_forest_reg[i].fit(self.predict_features, self.predict_labels_reviews[:,i])
            self.dumpJoblibObject(self.review_random_forest_reg, s)

    def loadPrizeRandomForestRegressors(self):
        s = 'prize_random_forest_reg'
        try:
            self.prize_random_forest_reg = self.loadJoblibObject(s)
        except IOError:
            print s+' object not found. Creating it...'
            self.prize_random_forest_reg = []
            for i in range(len(self.prizes_names)): #TODO : stocker un self.nb_institutions pour eviter le len()
                self.prize_random_forest_reg.append(RandomForestRegressor())
                self.prize_random_forest_reg[i].fit(self.predict_features, self.predict_labels_prizes[:,i])
            self.dumpJoblibObject(self.prize_random_forest_reg, s)

    def init_predict(self):
        self.loadLogBoxOfficeRandomForestRegressor()
        self.loadReviewRandomForestRegressors()
        self.loadPrizeRandomForestRegressors()

    def compute_predict(self, x_vector, language=None):
        '''
        Return {'prizes' : list of {'institution' : Institution Object,
                                    'win' : boolean,
                                    'value' : probability
                                   },
                'general_box_office' : {'rank' : int,
                                        'value' : float (M$),
                                        'neighbors': list of {'film' : Film Object,
                                                              'rank' : int
                                                             }
                                       },
                'genre_box_office' : {'rank' : int,
                                      'value' : float (M$),
                                      'neighbors': list of {'film' : Film Object,
                                                            'rank' : int
                                                           }
                                     },
                'reviews' : list of {'journal': Journal Object,
                                     'grade' : float,
                                    },
                'bag_of_words' : list of {'keyword' : Keyword Object,
                                          'value' : float dans [0,1]
                                         }
               }
        '''
        
        predicted_box_office = np.exp(self.log_box_office_random_forest_reg.predict(x_vector))

        journals = []
        predicted_grades = []
        for i in range(len(self.reviews_names)):
            try:
                journals.append(Journal.objects.get(name=self.reviews_names[i]))
                predicted_grades.append(self.review_random_forest_reg[i].predict(x_vector))
            except:
                pass

        institutions = []
        wins = []
        predicted_probabilities = []
        for i in range(len(self.prizes_names)):
            try:
                institutions.append(Institution.objects.get(name=self.prizes_names[i].split('_')[0]))
                if self.prizes_names[i].split('_')[1] == 'True':
                    wins.append(True)
                else:
                    wins.append(False)
                predicted_probabilities.append(
                    self.prize_random_forest_reg[i].predict(x_vector)
                )
            except:
                pass

        results = {'prizes' : [{'institution' : institutions[i],
                                'win' : wins[i],
                                'value' : predicted_probabilities[i]} 
                               for i in range(len(institutions))],
                   'general_box_office' :
                        {'rank' : 0, # TODO
                         'value' : predicted_box_office,
                         'neighbors' : [] # TODO
                         },
                    'genre_box_office' :
                        {'rank' : 0, # TODO
                         'value' : predicted_box_office,
                         'neighbors' : [] # TODO
                         },
                    'reviews': [{'journal' : journals[i],
                                 'grade' : predicted_grades[i]} 
                                for i in range(len(journals))],
                    'bag_of_words': [] # TODO
                    }                   

        return results

    def predict_request(self, args):
        # Get results
        lang = None
        if args.has_key('language'):
            try:
                lang = Language.objects.get(identifier = str(args['language']))
            except Language.DoesNotExist, exceptions.KeyError :
                pass
        results = self.compute_predict(self.vectorize_predict_user_input(args), language = lang)
        
        # Build query_results
        query_results = {}
        
        # Fill query_results['prizes']
        query_results['prizes'] = []
        for prize in results['prizes']:
            query_results['prizes'].append({'institution' : prize['institution'].name,
                                            'win' : prize['win'],
                                            'value' : prize['value']})
        
        # Fill query_results['general_box_office']
        neighbors = []
        for neighbor in results['general_box_office']['neighbors']:
            neighbors.append({'rank':neighbor['rank'],
                              'original_title':neighbor['film'].original_title,
                              'value':neighbor['film'].box_office})
        
        general_box_office = {'rank':results['general_box_office']['rank'],
                              'value':results['general_box_office']['value'],
                              'neighbors':neighbors
                              }
        
        query_results['general_box_office'] = general_box_office
        
        # Fill query_results['genre_box_office']
        neighbors_genre = []
        for neighbor in results['genre_box_office']['neighbors']:
            neighbors_genre.append({'rank':neighbor['rank'],
                                    'original_title':neighbor['film'].original_title,
                                    'value':neighbor['film'].box_office})
            genre_box_office = {'rank':results['genre_box_office']['rank'],
                                'value':results['genre_box_office']['value'],
                                'neighbors':neighbors_genre
                                }
            query_results['genre_box_office'] = genre_box_office
        
        # Fill query_results['critics']
        critics = {}
        
        reviews = []
        grades = []
        for item in results['reviews']:
            reviews.append({'journal' : item['journal'].name,
                            'grade' : item['grade']
                            })
            grades.append(item['grade'])
        
        critics['reviews'] = reviews
        critics['average'] = np.mean(grades)
        query_results['critics'] = critics
        
        # Fill query_results['bag_of_words']
        bag_of_words = []
        for item in results['bag_of_words']:
            bag_of_words.append({'word' : item['keyword'].word,
                                 'value' : item['value']
                                 })
        query_results['bag_of_words'] = bag_of_words
        
        # Return data
        return query_results

    def vectorize_predict_user_input(self, user_input):

        x_actor_vector = np.zeros([1,len(self.actor_names)])
        if user_input.has_key('actors'):
            if user_input['actors'].__class__ == list:
                for actor_id in user_input['actors']:
                    x_actor_vector[0,self.actor_names.index(actor_id)]=1

        if self.reduction_actors_in_predictfeatures == 'KM':
            x_actor_reduced = x_actor_vector * self.proj_actors_KM
        if self.reduction_actors_in_predictfeatures == 'SC':
            x_actor_reduced = x_actor_vector * self.proj_actors_SC

        x_genres_vector = np.zeros([1, len(self.genres_names)])
        if user_input.has_key('genres'):
            if user_input['genres'].__class__ == list:
                for genre in user_input['genres']:
                    x_genres_vector[0,self.genres_names.index(genre)]=1

        x_director_vector = np.zeros([1, len(self.director_names)])
        if user_input.has_key('directors'):
            if user_input['directors'].__class__ == list:
                for director_id in user_input['directors']:
                    x_director_vector[0,self.director_names.index(director_id)]=1

        if self.reduction_directors_in_predictfeatures == 'KM':
            x_director_reduced = x_director_vector * self.proj_directors_KM
        if self.reduction_directors_in_predictfeatures == 'SC':
            x_director_reduced = x_director_vector * self.proj_directors_SC

        x_keyword_vector = np.zeros([1, len(self.keyword_names)])
        if user_input.has_key('keywords'):
            if user_input['keywords'].__class__ == list:
                for keyword in user_input['keywords']:
                    x_keyword_vector[0,self.keyword_names.index(keyword)]=1

        x_keyword_reduced = x_keyword_vector * self.proj_keywords_KM
        
        x_budget_vector = np.zeros([1,1])
        if user_input.has_key('budget'):
            if user_input['budget'].__class__ == float:
                x_budget_vector[1,1] = user_input['budget']

        x_season_vector = np.zeros([1, len(self.season_names)]) # Default Season?
        try:
            for feat in self.genres_names:
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


# VIEUX CODE BENJAMIN
#        self.dim_actors = 20
#        s = raw_input('Start Spectral Clustering on actors ?')
#        if s=='y':
#            self.firstKM = MiniBatchKMeans(n_clusters=500, init='k-means++', n_init=1, init_size=2000, batch_size=3000, verbose=1)
#            first_reduction = self.firstKM.fit_transform(self.actor_matrix)
#            #first_reduction = np.exp( - first_reduction ** 2 ) # go from distance to similarity matrix
#
#            #self.firstSVD = TruncatedSVD(n_components = 500, n_iterations = 100)
#            #first_reduction = self.firstSVD.fit_transform(self.actor_matrix)
#
#            self.actors_SC = SpectralClustering(n_clusters = self.dim_actors, eigen_solver='arpack', affinity="nearest_neighbors", n_neighbors=10)
#            self.actor_labels = self.actors_SC.fit_predict(first_reduction.transpose())
#            self.proj_actors = scipy.sparse.csc_matrix(self.actor_labels==0, dtype=int).transpose()
#            for i in range(1, self.dim_actors):
#                self.proj_actors = scipy.sparse.hstack([self.proj_actors, scipy.sparse.csc_matrix(self.actor_labels==i, dtype=int).transpose()])
#            self.actor_reduced = first_reduction * self.proj_actors
#            self.actor_reduced = normalize(self.actor_reduced.astype(np.double), norm='l1', axis=1)
#            self.topic_actors = []
#            tot0 = np.asarray( np.sum(self.actor_matrix.todense(), axis=0) )[0, :]
#            for i in range(self.dim_actors):
#                tot = np.sum(self.firstKM.cluster_centers_[self.firstKM.labels_[self.actor_labels == i]], axis=0)
#                 tot = tot0 * (self.actor_labels == i)
#                #tot = self.firstSVD.inverse_transform(self.actor_labels == i)[0,:]
#                persons = []
#                for person in (np.array(self.actor_names)[np.argsort(-tot)[:10]]).tolist():
#                    try:
#                        persons.append( Person.objects.get(imdb_id = person[:9]) )
#                    except:
#                        continue
#                self.topic_actors.append((persons))
