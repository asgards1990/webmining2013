import tornado.ioloop
import tornado.web
import tornado.escape

from cinema.models import *

import datetime
import dateutil.parser
import exceptions

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("test.html")

class PredictionHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        if self.request.headers.get('X-Requested-With') == "XMLHttpRequest":
            try:
                args = tornado.escape.json_decode(self.get_argument("json_request"))
                lang = None
                if args.has_key('language'):
                    try:
                        lang = Language.objects.get(identifier = str(args['language']))
                        self.answer_predict_request(self.parse_criteria(args), language = lang)
                    except Language.DoesNotExist, exceptions.KeyError :
                        pass
                self.answer_predict_request(self.parse_criteria(args), language = lang)
            except ValueError:
                self.error('Wrong JSON format.')
        else:
            self.error('No proper JSON request found.')

            
    def answer_predict_request(self, criteria, language = None):
        self.finish(tornado.escape.json_encode({'success' : True, 'error' : '' }))
    
    def parse_criteria(self, crit_in):
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

    def error(self, err_msg):
        self.finish(tornado.escape.json_encode({'success' : False, 'error' : err_msg }))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "senellart.com")
        self.set_header("Access-Control-Allow-Origin", "tiresias.enst.fr")
        self.set_header("Access-Control-Allow-Origin", "null") # Uncomment to enable acces from every host.
    

class SearchHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        if self.request.headers.get('X-Requested-With') == "XMLHttpRequest":
            try:
                args = tornado.escape.json_decode(self.get_argument("json_request"))
                if args.has_key('id') and args.has_key('nbresults') and args.has_key('criteria'):
                    if (args['nbresults'].__class__==int) and (args['criteria'].__class__==dict):
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
                                        self.answer_search_request(film, args['nbresults'] , crit, filters = self.parse_filter(args['filter']) )
                                    else:
                                        self.answer_search_request(film, args['nbresults'], crit)
                                except Film.DoesNotExist:
                                    self.error('No film for id ' + args['id'])
                            else:
                                self.error('Criteria must be boolean.')
                        except KeyError:
                            self.error('Missing criterium.')
                    else:
                        self.error('Wrong format for nbresults or criteria.')
                else:
                    self.error('Please define the IMDb identfier, the number of expected results and search criteria.')
            except ValueError:
                self.error('Wrong JSON format.')
        else:
            self.error('No proper JSON request found.')
    
    def parse_filter(self, filt_in):
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

        if filt_in.has_key('genre'):
            if filt_in['genre'].__class__ == list:
                filt_out['genre'] =[]
                for person_id in filt_in['genre']:
                    try:
                        filt_out['genre'].append( Genre.objects.get(name=str(person_id)) )
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
        except excpeitons.ValueError, exceptions.KeyError:
            pass
        return filt_out

    def answer_search_request(self, film, nbresults, criteria, filters=None):
        '''
        answer_search_request is only called with checked arguments.
        '''
        results = []
        query_results = []
        for (v, f) in results:
            query_results.append({'id': f.imdb_id , 'orignal_title': f.original_title , 'title' : f.english_title, 'value' : v})
        self.finish(tornado.escape.json_encode({'success' : True, 'error' : '', 'nbresults' : nbresults, 'results' : query_results}))
        

    def error(self, err_msg):
        self.finish(tornado.escape.json_encode({'success' : False, 'error' : err_msg }))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "senellart.com")
	self.set_header("Access-Control-Allow-Origin", "tiresias.enst.fr")
	self.set_header("Access-Control-Allow-Origin", "null") # Uncomment to enable acces from every host.

class LearningService(object):
    def __init__(self):
        self.init_time = datetime.datetime.now()

    def quit(self):
        print("Learning service initialized at "+ self.init_time.isoformat()  +" is closing : tables are being cached.")

if __name__ == "__main__":
    app = tornado.web.Application(
        [(r'/', TestHandler),
         (r'/predict/', PredictionHandler),
         (r'/search/', SearchHandler)]
        )
    app.listen(8080)

    learn = LearningService()

    try:
        tornado.ioloop.IOLoop.instance().start()
    except exceptions.KeyboardInterrupt, exceptions.SystemExit:
        learn.quit()

