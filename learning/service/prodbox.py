from objects import *
from cinema.models import *

import exceptions

class CinemaService(LearningService):
    def update(self):
        pass

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
                            raise service.ParsingError('No film for id ' + args['id'])
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
        # lang = None
        # if args.has_key('language'):
        #     try:
        #         lang = Language.objects.get(identifier = str(args['language']))
        #         self.answer_predict_request(self.parse_criteria(args), language = lang)
        #     except Language.DoesNotExist, exceptions.KeyError :
        #         pass
        #     self.answer_predict_request(self.parse_criteria(args), language = lang)
        return {}

    def compute_predict_request(self, criteria, language=None):
        '''
        Return {'prizes' : list of Prize, ''}
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
