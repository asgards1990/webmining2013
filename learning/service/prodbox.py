from objects import *
from vectorizers import *
from status.models import TableUpdateTime
from cinema.models import *
import filmsfilter as flt
import numpy as np
import scipy

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize
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
    def __init__(self):
        super(CinemaService, self).__init__()
        
        self.films = flt.filter1()
        if not self.is_loaded('films'):
            #self.films = flt.filter1()
            self.indexes = hashIndexes(self.films.iterator())
            self.create_cobject('films', self.indexes)
        else:
            self.indexes = self.get_cobject('films').get_content()
        self.nbfilms = len(self.indexes)
        
        self.dim_keywords = 30
        if not self.is_loaded('keywords'):
            gkey = genKeywords(self.films.iterator())
            v =  DictVectorizer(dtype=int)
            self.keyword_matrix = v.fit_transform(gkey)
            self.keyword_names = v.get_feature_names()
            
            self.keywords_KM = KMeans(n_clusters = self.dim_keywords, init='k-means++', verbose=1)
            self.keywords_reduced = self.keywords_KM.fit_transform(TfidfTransformer().fit_transform(self.keyword_matrix))
            # 0 means closer to centroids.
            
            self.create_cobject('keywords', (self.keyword_names, self.keyword_matrix, self.keywords_reduced))
        else:
            self.keyword_names, self.keyword_matrix, self.keywords_reduced = self.get_cobject('keywords').get_content()
        self.nbkeywords = self.keyword_matrix.shape[1]
        
        if not self.is_loaded('genre_stats'):
            self.filmsbygenre = {}
            self.keywordsbygenre = {}
            for genre in Genre.objects.all():
                self.filmsbygenre[genre.name] = map(lambda e : self.indexes[e], map(lambda e: e.imdb_id, self.films.filter(genres = genre)))
                if self.filmsbygenre[genre.name] == []:
                    self.keywordsbygenre[genre.name] = np.zeros(self.nbkeywords)
                else:
                    self.keywordsbygenre[genre.name] = np.mean(self.keyword_matrix[self.filmsbygenre[genre.name]].toarray(), axis=0)
            self.create_cobject('genre_stats', (self.filmsbygenre, self.keywordsbygenre))
        else:
            self.filmsbygenre, self.keywordsbygenre = self.get_cobject('genre_stats').get_content()

        if not self.is_loaded('actors'):
            v = DictVectorizer(dtype=int)
            self.actor_matrix = v.fit_transform(genActorsTuples2(self.films.iterator()))
            self.actor_names = v.get_feature_names()
            self.create_cobject('actors', (self.actor_names, self.actor_matrix))
        else:
            self.actor_names, self.actor_matrix = self.get_cobject('actors').get_content()

        self.dim_writers = 20 # must be lower than dim_keywords
        if not self.is_loaded('writers'):
            v=DictVectorizer(dtype=int)
            writer_matrix = v.fit_transform(genWriters(self.films.iterator()))
            self.writer_names = v.get_feature_names()
            # Distance to keywords' centroids of writers.
            self.writer_keyword_matrix = writer_matrix.transpose() * self.keywords_reduced
            
            self.writer_SC = SpectralClustering(n_clusters = self.dim_writers, eigen_solver='arpack', affinity="nearest_neighbors")
            writer_labels = self.writer_SC.fit_predict(self.writer_keyword_matrix)
            self.proj_writers = scipy.sparse.csc_matrix(writer_labels==0, dtype=int).transpose()
            for i in range(1, self.dim_writers):
                self.proj_writers = scipy.sparse.hstack([self.proj_writers, scipy.sparse.csc_matrix(writer_labels==i, dtype=int).transpose()])
            self.writer_reduced = writer_matrix * self.proj_writers
            
            self.create_cobject('writers', (self.writer_names, self.writer_keyword_matrix, self.writer_reduced, self.proj_writers))
        else:
            self.writer_names, self.writer_keyword_matrix, self.writer_reduced, self.proj_writers = self.get_cobject('writers').get_content()

        self.nbwriters = len(self.writer_names)

        # TODO : load other variables

        self.dim_actors = 20
        s = raw_input('Start Spectral Clustering on actors ?')
        if s=='y':
            self.firstKM = MiniBatchKMeans(n_clusters=500, init='k-means++', n_init=1, init_size=2000, batch_size=3000, verbose=1)
            first_reduction = self.firstKM.fit_transform(self.actor_matrix)
            #first_reduction = np.exp( - first_reduction ** 2 ) # go from distance to similarity matrix
            
            #self.firstSVD = TruncatedSVD(n_components = 500, n_iterations = 100)
            #first_reduction = self.firstSVD.fit_transform(self.actor_matrix)
            
            self.actors_SC = SpectralClustering(n_clusters = self.dim_actors, eigen_solver='arpack', affinity="nearest_neighbors", n_neighbors=10)
            self.actor_labels = self.actors_SC.fit_predict(first_reduction.transpose())
            self.proj_actors = scipy.sparse.csc_matrix(self.actor_labels==0, dtype=int).transpose()
            for i in range(1, self.dim_actors):
                self.proj_actors = scipy.sparse.hstack([self.proj_actors, scipy.sparse.csc_matrix(self.actor_labels==i, dtype=int).transpose()])
            self.actor_reduced = first_reduction * self.proj_actors
            self.actor_reduced = normalize(self.actor_reduced.astype(np.double), norm='l1', axis=1)
            self.topic_actors = []
            for i in range(self.dim_actors):
                tot = np.sum(self.firstKM.cluster_centers_[self.firstKM.labels_[self.actor_labels == i]], axis=0)
                #tot = self.firstSVD.inverse_transform(self.actor_labels == i)[0,:]
                persons = []
                for person in (np.array(self.actor_names)[np.argsort(-tot)[:10]]).tolist():
                    try:
                        persons.append( Person.objects.get(imdb_id = person[:9]) )
                    except:
                        continue
                self.topic_actors.append((persons))

    def suggest_keywords(self, args):
        if args.has_key('str') and args.has_key('nbresults'):
            if args['nbresults'].__class__ == int and args['nbresults'] >= 0:
                tot = np.zeros(self.nbkeywords)
                rex = re.compile(args['str'])
                found = [(rex.search(m)!=None) for m in self.keyword_names]
                if args.has_key('filter') and args['filter'].__class__ == list:
                    for element in args['filter']:
                        try:
                            value, genre = element
                            tot += found * (value * self.keywordsbygenre[genre])
                        except:
                            continue
                else:
                    tot = found * np.mean(self.keyword_matrix.toarray(), axis=0)
                ind = list(np.argsort(-tot)[:min(args['nbresults'], self.nbfilms)])
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

        return crit_out
