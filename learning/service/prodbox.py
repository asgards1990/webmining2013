from objects import *
from vectorizers import *
from status.models import TableUpdateTime
from cinema.models import Film, Person, Genre, Keyword
import filmsfilter as flt
import numpy as np
import scipy
from dimreduce import *

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize, Imputer
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import SpectralClustering

import re

import exceptions

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
        self.films = flt.filter1()
        if not self.is_loaded('films'):
            self.indexes = hashIndexes(self.films.iterator())
            self.create_cobject('films', self.indexes)
        else:
            self.indexes = self.get_cobject('films').get_content()
        self.nb_films = len(self.indexes)
    
    def loadImdb(self):
        if not self.is_loaded('imdb'):
            g_user_rating = genImdbUserRating(self.films.iterator())
            v_user_rating = DictVectorizer(dtype=np.float32)
            self.imdb_user_rating_matrix = v_user_rating.fit_transform(g_user_rating)
            g_nb_user_ratings = genImdbNbUserRatings(self.films.iterator())
            v_nb_user_ratings = DictVectorizer(dtype=int)
            self.imdb_nb_user_ratings_matrix = v_nb_user_ratings.fit_transform(g_nb_user_ratings)
            g_nb_user_reviews = genImdbNbUserReviews(self.films.iterator())
            v_nb_user_reviews = DictVectorizer(dtype=int)
            self.imdb_nb_user_reviews_matrix = v_nb_user_reviews.fit_transform(g_nb_user_reviews)
            g_nb_reviews = genImdbNbReviews(self.films.iterator())
            v_nb_reviews = DictVectorizer(dtype=int)
            self.imdb_nb_reviews_matrix = v_nb_reviews.fit_transform(g_nb_reviews)
            self.create_cobject('imdb', (self.imdb_user_rating_matrix, self.imdb_nb_user_ratings_matrix, self.imdb_nb_user_reviews_matrix,self.imdb_nb_reviews_matrix))
        else:
                self.imdb_user_rating_matrix, self.imdb_nb_user_ratings_matrix, self.imdb_nb_user_reviews_matrix,self.imdb_nb_reviews_matrix = self.get_cobject('imdb').get_content()
    
    def loadReleaseDate(self):
        if not self.is_loaded('release_date'):
            gkey = genReleaseDate(self.films.iterator())
            v =  DictVectorizer(dtype=date) # TODO : WARNING : THIS IS NOT CORRECT
            self.release_date_matrix = v.fit_transform(gkey)
            self.create_cobject('release_date', self.release_date_matrix)
        else:
            self.release_date_matrix = self.get_cobject('release_date').get_content()
    
    def loadRuntime(self):
        if not self.is_loaded('runtime'):
            gkey = genRuntime(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.runtime_matrix = v.fit_transform(gkey)
            self.create_cobject('runtime', self.runtime_matrix)
        else:
            self.runtime_matrix = self.get_cobject('runtime').get_content()
    
    def loadBoxOffice(self):
        if not self.is_loaded('box_office'):
            gkey = genBoxOffice(self.films.iterator())
            v =  DictVectorizer(dtype=np.float32)
            self.box_office_matrix = v.fit_transform(gkey)
            self.create_cobject('box_office', self.box_office_matrix)
        else:
            self.box_office_matrix = self.get_cobject('box_office').get_content()
    
    def loadGenres(self):
        if not self.is_loaded('genres'):
            gkey = genGenres(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.genres_matrix = v.fit_transform(gkey)
            self.genres_names = v.get_feature_names()
            self.create_cobject('genres', (self.genres_names, self.genres_matrix))
        else:
            self.genres_names, self.genres_matrix = self.get_cobject('genres').get_content()
    
    def loadBudget(self):
        if not self.is_loaded('budget'):
            gkey = genBudget(self.films.iterator())
            v =  DictVectorizer(dtype=np.float32)
            self.budget_matrix = v.fit_transform(gkey)
            self.create_cobject('budget', self.budget_matrix)
        else:
            self.budget_matrix = self.get_cobject('budget').get_content()
    
    def loadPrizes(self):
        if not self.is_loaded('prizes'):
            gkey = genPrizes(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.prizes_matrix = v.fit_transform(gkey)
            self.prizes_names = v.get_feature_names()
            self.create_cobject('prizes', (self.prizes_names, self.prizes_matrix))
        else:
            self.prizes_names, self.prizes_matrix = self.get_cobject('prizes').get_content()
    
    def loadCountries(self):
        if not self.is_loaded('countries'):
            gkey = genCountries(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.countries_matrix = v.fit_transform(gkey)
            self.countries_names = v.get_feature_names()
            self.create_cobject('countries', (self.countries_names, self.countries_matrix))
        else:
            self.countries_names, self.countries_matrix = self.get_cobject('countries').get_content()
    
    def loadLanguages(self):
        if not self.is_loaded('languages'):
            gkey = genLanguages(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.languages_matrix = v.fit_transform(gkey)
            self.languages_names = v.get_feature_names()
            self.create_cobject('languages', (self.languages_names, self.languages_matrix))
        else:
            self.languages_names, self.languages_matrix = self.get_cobject('languages').get_content()
    
    def loadMetacriticScore(self):
        if not self.is_loaded('metacritic_score'):
            gkey = genMetacriticScore(self.films.iterator())
            v =  DictVectorizer(dtype=np.float32)
            self.metacritic_score_matrix = v.fit_transform(gkey)
            self.create_cobject('metacritic_score', self.metacritic_score_matrix)
        else:
            self.metacritic_score_matrix = self.get_cobject('metacritic_score').get_content()
    
    def loadProductionCompanies(self):
        if not self.is_loaded('production_companies'):
            gkey = genProductionCompanies(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.production_companies_matrix = v.fit_transform(gkey)
            self.production_companies_names = v.get_feature_names()
            self.create_cobject('production_companies', (self.production_companies_names, self.production_companies_matrix))
        else:
            self.production_companies_names, self.production_companies_matrix = self.get_cobject('production_companies').get_content()
    
    def loadReviews(self):
        if not self.is_loaded('reviews'):
            gkey = genReviews(self.films.iterator())
            v =  DictVectorizer(dtype=np.float32)
            self.reviews_matrix = v.fit_transform(gkey)
            self.reviews_names = v.get_feature_names()
            self.create_cobject('reviews', (self.reviews_names, self.reviews_matrix))
        else:
            self.reviews_names, self.reviews_matrix = self.get_cobject('reviews').get_content()
    
    def loadSeason(self):
        if not self.is_loaded('season'):
            gkey = genSeason(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.season_matrix = v.fit_transform(gkey)
            self.season_names = v.get_feature_names()
            self.create_cobject('season', (self.season_names, self.season_matrix))
        else:
            self.season_names, self.season_matrix = self.get_cobject('season').get_content()
    
    def loadStats(self):
        if not self.is_loaded('genre_stats'):
            self.keywordsbygenre = self.genres_matrix.transpose() * self.keyword_matrix
            self.create_cobject('genre_stats', self.keywordsbygenre)
        else:
            self.keywordsbygenre = self.get_cobject('genre_stats').get_content()
    
    def loadKeywords(self):
        self.dim_keywords = 30 #TODO : optimize
        if not self.is_loaded('keywords'):
            gkey = genKeywords(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.keyword_matrix = v.fit_transform(gkey)
            self.keyword_names = v.get_feature_names()
            self.keywords_KM = KMeans(n_clusters = self.dim_keywords, init='k-means++', verbose=1)
            self.keywords_reduced_KM = self.keywords_KM.fit_transform(TfidfTransformer().fit_transform(self.keyword_matrix))
            # 0 means closer to centroids.
            self.create_cobject('keywords', (self.keyword_names, self.keyword_matrix, self.keywords_reduced_KM))
        else:
            self.keyword_names, self.keyword_matrix, self.keywords_reduced_KM = self.get_cobject('keywords').get_content()
        self.nb_keywords = self.keyword_matrix.shape[1]
    
    def loadActors(self):
        self.dim_actors = 10 #TODO : optimize
        if not self.is_loaded('actors'):
            v = DictVectorizer(dtype=int)
            self.actor_matrix = v.fit_transform(genActorsTuples2(self.films.iterator()))
            self.actor_names = v.get_feature_names()
            # Normalize actor matrix ?
            # TODO : play on arguments (ex: n_neighbors) in spectral clustering
            # self.actor_reduced_SC = reduceDimBySpectralClustering(self.actor_matrix, self.actor_names, self.dim_actors) # uses dimreduce
            
            #self.actors_SC = SpectralClustering(n_clusters = self.dim_actors, eigen_solver='arpack', affinity="nearest_neighbors", n_neighbors=8)
            #actor_labels = self.actors_SC.fit_predict(self.actor_matrix.transpose())
            #self.proj_actors = scipy.sparse.csc_matrix(actor_labels==0, dtype=int).transpose()
            #for i in range(1, self.dim_actors):
            #    self.proj_actors = scipy.sparse.hstack([self.proj_actors, scipy.sparse.csc_matrix(actor_labels==i, dtype=int).transpose()])
            #self.actor_reduced_SC = first_reduction * self.proj_actors
            #self.actor_reduced_SC = normalize(self.actor_reduced.astype(np.double), norm='l1', axis=1)
            self.actor_reduced_SC = self.actor_matrix # TODO
            
            self.create_cobject('actors', (self.actor_names, self.actor_matrix, self.actor_reduced_SC))
        else:
            self.actor_names, self.actor_matrix, self.actor_reduced_SC = self.get_cobject('actors').get_content()
        self.nb_actors = self.actor_matrix.shape[1]
    
    def loadWriters(self):
        self.dim_writers = 20 # must be lower than dim_keywords #TODO : optimize
        keywords_reduced = self.keywords_reduced_KM
        if not self.is_loaded('writers'):
            v=DictVectorizer(dtype=int)
            self.writer_matrix = v.fit_transform(genWriters(self.films.iterator()))
            self.writer_names = v.get_feature_names()
            self.writer_keyword_matrix = self.writer_matrix.transpose() * keywords_reduced #TODO : average?
            # First method: Spectral Clustering
            self.writer_SC = SpectralClustering(n_clusters = self.dim_writers, eigen_solver='arpack', affinity="nearest_neighbors")
            writer_labels = self.writer_SC.fit_predict(self.writer_keyword_matrix)
            self.proj_writers_SC = scipy.sparse.csc_matrix(writer_labels==0, dtype=int).transpose()
            for i in range(1, self.dim_writers):
                self.proj_writers_SC = scipy.sparse.hstack([self.proj_writers_SC, scipy.sparse.csc_matrix(writer_labels==i, dtype=int).transpose()])
            self.writer_reduced_SC = self.writer_matrix * self.proj_writers
            # Second method: Average of keywords features
            self.writer_reduced_avg =  self.writer_matrix * self.writer_keyword_matrix #TODO : average? normalize ?
            self.create_cobject('writers', (self.writer_names, self.writer_keyword_matrix, self.writer_reduced_SC, self.proj_writers_SC, self.writer_reduced_avg))
        else:
            self.writer_names, self.writer_keyword_matrix, self.writer_reduced_SC, self.proj_writers_SC, self.writer_reduced_avg = self.get_cobject('writers').get_content()
        self.nb_writers = len(self.writer_names)
    
    def loadDirectors(self):
        self.dim_directors = 20 # must be lower than dim_actors #TODO : optimize
        actor_reduced = self.actor_reduced_SC
        if not self.is_loaded('directors'):
            v=DictVectorizer(dtype=int)
            self.director_matrix = v.fit_transform(genDirectors(self.films.iterator()))
            self.director_names = v.get_feature_names()
            self.director_actor_matrix = normalize(self.director_matrix.transpose(), norm='l1', axis=1) * actor_reduced #TODO : average?
            # First method: Spectral Clustering
            self.director_SC = SpectralClustering(n_clusters = self.dim_directors, eigen_solver='arpack', affinity="nearest_neighbors")
            director_labels = self.director_SC.fit_predict(self.director_actor_matrix)
            self.proj_directors_SC = scipy.sparse.csc_matrix(director_labels==0, dtype=int).transpose()
            for i in range(1, self.dim_directors):
                self.proj_directors_SC = scipy.sparse.hstack([self.proj_directors, scipy.sparse.csc_matrix(director_labels==i, dtype=int).transpose()])
            self.director_reduced_SC = self.director_matrix * self.proj_director
            # Second method: Average of actors features
            self.director_reduced_avg =  normalize(self.director_matrix, norm='l1', axis=1) * self.director_actor_matrix #TODO : average?
            self.create_cobject('directors', (self.director_names, self.director_actor_matrix, self.director_reduced_SC, self.proj_directors_SC, self.director_reduced_avg))
        else:
            self.director_names, self.director_actor_matrix, self.director_reduced_SC, self.proj_directors_SC, self.directors_reduced_avg = self.get_cobject('directors').get_content()
        self.nb_directors = len(self.director_names)
    
    def loadSearchClustering(self):
        if not self.is_loaded('search_clustering'):
            self.search_clustering = []
            X_people = scipy.sparse.hstack([self.actor_reduced_SC,self.director_reduced_SC]) #TODO:play on clustering types
            X_budget = self.budget_matrix
            X_review = self.reviews_matrix
            X_genre =  self.genres_matrix
            X_budget[np.isnan(X_budget)] = -1 # replace NaN with -1 for missing values
            completer = Imputer(missing_values=-1)
            completer.fit(X_budget)
            X_budget = completer.transform(X_budget) #TODO: answer this question: use log instead ?
            X_budget = X_budget/np.max(X_budget)
            X_review = X_review/100 # because grades should be in [0,1] #WARNING BDD DAVID OU BENJAMIN
            X_review = X_review/X_review.shape[1] #divide by number of columns
            X_genre = X_genre/X_genre.shape[1] #divide by number of columns
            X_people = X_people/X_people.shape[1] #divide by number of columns
            for k in range(16):
                people_weight = self.high_weight if (k>>0)%2 else self.low_weight
                budget_weight = self.high_weight if (k>>1)%2 else self.low_weight
                review_weight = self.high_weight if (k>>2)%2 else self.low_weight
                genre_weight = self.high_weight if (k>>3)%2 else self.low_weight
                X = scipy.sparse.hstack([people_weight*X_people, budget_weight*X_budget, review_weight*X_review, genre_weight*X_review])
                KM = KMeans(n_clusters=self.n_clusters_search)
                KM.fit_predict(X)
                self.search_clustering[k] = {'labels' : KM.labels_, 'cluster_centers' : KM.cluster_centers_}
            self.create_cobject('search_clustering',self.search_clustering)
        else:
            self.search_clustering = self.get_cobject('search_clustering').get_content()
    
    def __init__(self):
        super(CinemaService, self).__init__()
        # Load films data
        self.loadFilms()
        # Load prediction features
        self.loadActors() # TODO : Enable Spectral clustering
        #self.loadDirectors() TODO : Error with renormalization
        self.loadSeason()
        self.loadBudget()
        self.loadKeywords()
        self.loadGenres()
        # Load prediction labels
        self.loadBoxOffice()
        self.loadPrizes()
        self.loadReviews()
        # Load other features
        self.loadStats()
        #self.loadWriters() Error with renormalization
        self.loadRuntime()
        self.loadMetacriticScore()
        #self.loadReleaseDate() #TODO DOES NOT WORK
        self.loadProductionCompanies()
        #self.loadImdb() #TODO beware of None values
        self.loadCountries()
        self.loadLanguages()
        print('ok 3')
        # Load search clusterings
        self.n_clusters_search = 20
        self.p_norm = 2 # p-norm used for distances
        self.high_weight = 1 # for the distance definition
        self.low_weight = 0 # for the distance definition
        #self.loadSearchClustering()
    
    def suggest_keywords(self, args):
        if args.has_key('str') and args.has_key('nbresults'):
            if args['nbresults'].__class__ == int and args['nbresults'] >= 0:
                tot = np.zeros(self.nb_keywords)
                rex = re.compile(args['str'])
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
                            raise ParsingError('No film for id ' + args['id'])
                    else:
                        raise ParsingError('Criteria must be boolean.')
                except KeyError:
                    raise ParsingError('Missing criterium.')
            else:
                raise ParsingError('Wrong format for nbresults or criteria.')
        else:
            raise ParsingError('Please define the IMDb identfier, the number of expected results and search criteria.')
    
    def compute_search(self, film, nbresults, criteria, filters=None):
        '''
        Return a list of couples (value, film)
        '''
        return []
    
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
            if (filt_in['budget']['min'].__class__==float) and (filt_in['budget']['max'].__class__ == float):
                filt_out['budget'] = filt_in['budget']
        except exceptions.KeyError:
            pass
        
        try:
            if (filt_in['reviews']['min'].__class__ == float):
                filt_out['reviews'] = filt_in['reviews']
        except exceptions.KeyError:
            pass
        
        filt_out['release_period'] = {'begin' :datetime.date.min, 'end': datetime.date.max}
        try:
            filt_out['release_period']['begin'] = dateutil.parser.parse( filt_in['release_period']['begin'] ).date()
        except exceptions.ValueError, exceptions.KeyError:
            pass
        try:
            filt_out['release_period']['end'] = dateutil.parser.parse( filt_in['release_period']['end'] ).date()
        except exceptons.ValueError, exceptions.KeyError:
            pass
        
        return filt_out
    
    def predict_request(self, args):
        # Get results
        lang = None
        if args.has_key('language'):
            try:
                lang = Language.objects.get(identifier = str(args['language']))
            except Language.DoesNotExist, exceptions.KeyError :
                pass
        results = self.compute_predict(self.parse_criteria(args), language = lang)
        
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
        keywords = []
        for keyword in results['keywords']:
            keyword.append(keyword.word)
        
        reviews = []
        grades = []
        for item in results['reviews']:
            reviews.append({'journal' : item['journal'].name,
                            'grade' : item['grade'],
                            'keywords' : keywords
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
    
    def compute_predict(self, criteria, language=None):
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
                                     'keywords' : list of Keyword Object
                                    },
                'bag_of_words' : list of {'keyword' : Keyword Object,
                                          'value' : float dans [0,1]
                                         }
               }
        '''
        return {}
    
    def parse_predict_criteria(self, crit_in):
        crit_out = {}
        
        if crit_in.has_key('actors'):
            if crit_in['actors'].__class__ == list:
                crit_out['actors'] = []
                for person_id in crit_in['actors']:
                    try:
                        crit_out['actors'].append(Person.objects.get(imdb_id=str(person_id)))
                    except Person.DoesNotExist, exceptions.TypeError:
                        pass
        
        if crit_in.has_key('genres'):
            if crit_in['genres'].__class__ == list:
                crit_out['genres'] = []
                for genre in crit_in['genres']:
                    try:
                        crit_out['genres'].append(Genre.objects.get(imdb_id=str(genre)))
                    except Genre.DoesNotExist, exceptions.TypeError:
                        pass
        
        if crit_in.has_key('directors'):
            if crit_in['directors'].__class__ == list:
                crit_out['directors'] = []
                for person_id in crit_in['directors']:
                    try:
                        crit_out['directors'].append(Person.objects.get(imdb_id=str(person_id)))
                    except Person.DoesNotExist, exceptions.TypeError:
                        pass
        
        if crit_in.has_key('keywords'):
            if crit_in['keywords'].__class__ == list:
                crit_out['keywords'] = []
                for keyword in crit_in['keywords']:
                    try:
                        crit_out['keywords'].append(Keyword.objects.get(word=str(keyword)))
                    except Keyword.DoesNotExist:
                        crit_out['keywords'].append(str(keyword))
        
        if crit_in.has_key('budget'):
            if crit_in['budget'].__class__ == float:
                crit_out['budget'] = crit_in['budget']
        
        try:
            if crit_in['release_period']['season'] in ['winter', 'spring', 'summer', 'fall']:
                crit_out['release_period'] = crit_in['release_period']
        except exceptions.KeyError:
            pass
        
        return crit_outl


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
