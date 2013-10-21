import tornado.ioloop
import tornado.web
import tornado.escape
import json

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("test.html")

class PredictionHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        d = tornado.escape.json_decode(self.get_argument("json_request"))
        self.write( tornado.escape.json_encode(d) )
        self.finish()
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "null") # Enable acces from every host.

class SearchHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        d = tornado.escape.json_decode(self.get_argument("json_request"))
        self.write( json.dumps(d) )
        self.finish()
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "null")

if __name__ == "__main__":
    app = tornado.web.Application([(r'/', TestHandler), (r'/predict/', PredictionHandler), (r'/search/', SearchHandler)])
    app.listen(2345)
    tornado.ioloop.IOLoop.instance().start()