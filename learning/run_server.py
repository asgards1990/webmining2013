import argparse

import tornado.ioloop
import tornado.web

import ajax_server.handlers
import service.prodbox

parser = argparse.ArgumentParser(description='Launch learning server.')
parser.add_argument('integer', metavar='port', type=int, nargs='?', help='port number (default is 8080)', default=8080)
parser.add_argument('-c', dest='start', action='store_const', const=False, default=True, help='only launch precomputation (and not the server)')
args = parser.parse_args()

if __name__ == "__main__":
    app_learn = service.prodbox.CinemaService()
    app_learn.loadData()
    app_learn.loadSearchClustering()
    app_learn.loadPredict()

    if args.start:
        app = tornado.web.Application(
            [(r'/', ajax_server.handlers.TestHandler),
             (r'/predict/', ajax_server.handlers.Handler, dict(app_learn = app_learn, method="predict")),
             (r'/search/', ajax_server.handlers.Handler, dict(app_learn = app_learn, method="search")),
             (r'/suggest/film/(.*)', ajax_server.handlers.AutoCompleteHandler, dict(app_learn = app_learn, target="films")),
             (r'/suggest/', ajax_server.handlers.Handler, dict(app_learn = app_learn, method="suggest_keywords"))]
            )
        app.listen(args.integer)
        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt, SystemExit:
            app_learn.quit()
