from service.prodbox import *
import datetime

serv = CinemaService()

criteria = {'actor_director':True,
          'budget':False,
          'review':False,
          'genre':False}
filters = {'actors':[],
	'directors':[],
	'genres':[],#[Genre.objects.get(name='Action'), Genre.objects.get(name='Romance')],
	'budget':{'min':5000000.,'max':10000000000000000000000.}, #TODO : warning, always use floats!
	'reviews':{'min':0.}, #TODO : warning, always use floats!
	'release_period':{'begin':'2010','end':'2020'}
	}
filters=None
args={'id':'tt1024648', # Avatar 'tt0499549' # Argo tt1024648' # 2012 'tt1190080' # Intouchables 'tt1675434'
	'criteria':criteria,
	'nbresults':10,
    'filter':filters}

res = serv.search_request(args)

for item in res['results']:
    print item

serv.quit()
