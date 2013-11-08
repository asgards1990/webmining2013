from cinema.models import Film, Person
import service.prodbox as pb 
import re

app = pb.CinemaService()

args = {
        'actors' : ['nm0948000',],
        'genres' : ['Action'],
        'directors': ['nm0906667',],
        'keywords': ['pistol', 'murder',],
        'budget' : 100,
        'release_period' : {'season':'no-season'}
        }

print 'Actors:'
for actor in args['actors']:
    print '-', Person.objects.get(imdb_id=actor)

print 'Genres:'
for genre in args['genres']:
    print '-', genre

print 'Directors:'
for director in args['directors']:
    print '-', Person.objects.get(imdb_id=director)

print 'Keywords:'
for keyword in args['keywords']:
    print '-', keyword

print 'Budget: ', args['budget']

print 'Season: ', args['release_period']['season']


print('--------------------')
print('Predict request')
results = app.predict_request(args)
print(results)

