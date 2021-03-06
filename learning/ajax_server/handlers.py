import tornado.ioloop
import tornado.web
import tornado.escape
import service.objects

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("test.html")

class Handler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def initialize(self, app_learn, method):
        self.app_learn = app_learn
        self.method = method

    def post(self):
        if True or self.request.headers.get('X-Requested-With') == "XMLHttpRequest":
            try:
                args = tornado.escape.json_decode(self.get_argument("json_request"))
            except ValueError as e:
                self.error('Wrong JSON format. Error: {}'.format(e))
            else:
                try:
                    if self.method=='search':
                        query_results = self.app_learn.search_request(args)
                    elif self.method=='predict':
                        query_results = self.app_learn.predict_request(args)
                    elif self.method=='suggest_keywords':
                        query_results = self.app_learn.suggest_keywords(args)
                    else:
                        raise service.objects.ParsingError('Undefined method.')
                    query_results['success'] = True
                    query_results['error'] = ''
                    self.finish(tornado.escape.json_encode(query_results))                
                except service.objects.ParsingError as e:
                    self.error(e.value)
        else:
            self.error('No proper JSON request found.')

    def error(self, err_msg):
        self.finish(tornado.escape.json_encode({'success' : False, 'error' : err_msg }))

    def set_default_headers(self):
        #self.set_header("Access-Control-Allow-Origin", "senellart.com")
        #self.set_header("Access-Control-Allow-Origin", "tiresias.enst.fr")
        self.set_header("Access-Control-Allow-Origin", "*") # Uncomment to enable acces from every host.
        
        
class AutoCompleteHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def initialize(self, app_learn, target):
        self.app_learn = app_learn
        self.target = target

    def get(self, q):
        if True or self.request.headers.get('X-Requested-With') == "XMLHttpRequest":
            try:
                if self.target=='films':
                    query_results = self.app_learn.suggest_films(q)
                else:
                    raise service.objects.ParsingError('Undefined autocomplete target.')
                query_results['success'] = True
                query_results['error'] = ''
                self.finish(tornado.escape.json_encode(query_results))                
            except service.objects.ParsingError as e:
                self.error(e.value)
        else:
            self.error('No proper JSON request found.')

    def error(self, err_msg):
        self.finish(tornado.escape.json_encode({'success' : False, 'error' : err_msg }))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")   
