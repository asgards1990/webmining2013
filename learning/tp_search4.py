from service.prodbox import *
import datetime

serv = CinemaService()

criteria = {'actor_director':True,
          'budget':True,
          'review':True,
          'genre':True}
filters = {'actors':[], #DiCaprio nm0000138 Cotillard nm0182839
	'directors':[], # James Cameron nm0000116 Scorcese nm0000217
	'genres':[],#[Genre.objects.get(name='Action'), Genre.objects.get(name='Romance')],
	'budget':{'min':0,'max':10000000000}, #TODO : warning, always use floats!
	'reviews':{'min':0}, #TODO : warning, always use floats! beware 100
	'release_period':{'begin':1901,'end':2020}
	}

args={'id':'tt0882969', # Avatar 'tt0499549' # Argo tt1024648' # 2012 'tt1190080' # Intouchables 'tt1675434'
	'criteria':criteria,
	'nbresults':10,
    'filter':filters}

res = serv.search_request(args)

for item in res['results']:
    print item['title']

serv.quit()
