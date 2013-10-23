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
            except ValueError:
                self.error('Wrong JSON format.')
        else:
            self.error('No proper JSON request found.')

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

if __name__ == "__main__":
    app = tornado.web.Application(
        [(r'/', TestHandler),
         (r'/predict/', PredictionHandler),
         (r'/search/', SearchHandler)]
        )
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
