from service.prodbox import *

serv = CinemaService()

criteria = {'actor_director':True,
          'budget':True,
          'review':True,
          'genre':True}
args={'id':'tt1022603',
	'criteria':criteria,
	'nbresults':10}

serv.search_request(args)
