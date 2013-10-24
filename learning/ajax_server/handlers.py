import tornado.ioloop
import tornado.web
import tornado.escape

import service.objects

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("test.html")

class PredictionHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def initialize(self, app_learn):
        self.app_learn = app_learn

    def post(self):
        if self.request.headers.get('X-Requested-With') == "XMLHttpRequest":
            try:
                args = tornado.escape.json_decode(self.get_argument("json_request"))
                try:
                    query_results = self.app_learn.predict_request(args)
                    query_results['success'] = True
                    query_results['error'] = ''
                    self.finish(tornado.escape.json_encode(query_results))
                except service.objects.ParsingError as e:
                    self.error(e.value)
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
    def initialize(self, app_learn):
        self.app_learn = app_learn

    def post(self):
        if self.request.headers.get('X-Requested-With') == "XMLHttpRequest":
            try:
                args = tornado.escape.json_decode(self.get_argument("json_request"))
                try:
                    query_results = self.app_learn.search_request(args)
                    query_results['success'] = True
                    query_results['error'] = ''
                    self.finish(tornado.escape.json_encode(query_results))
                except service.objects.ParsingError as e:
                    self.error(e.value)
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
