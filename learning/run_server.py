import tornado.ioloop
import tornado.web

import ajax_server.handlers
import service.prodbox

if __name__ == "__main__":
    app_learn = service.prodbox.CinemaService()
    app_learn.loadData()
    app_learn.loadSearchClustering()
    app_learn.loadPredict()

    app = tornado.web.Application(
        [(r'/', ajax_server.handlers.TestHandler),
         (r'/predict/', ajax_server.handlers.Handler, dict(app_learn = app_learn, method="predict")),
         (r'/search/', ajax_server.handlers.Handler, dict(app_learn = app_learn, method="search")),
         (r'/suggest/', ajax_server.handlers.Handler, dict(app_learn = app_learn, method="suggest_keywords"))]
        )
    app.listen(8080)
    
    s = raw_input("Should we start the server ?")
    if s!="y":
        app.quit()
    else:
        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt, SystemExit:
            app_learn.quit()
