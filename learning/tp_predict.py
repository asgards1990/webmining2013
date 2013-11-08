from cinema.models import Film, Person
import service.prodbox as pb 
import re

app = pb.CinemaService()

args = {
        'actors' : [app.actor_names[0], app.actor_names[50],],
        'genres' : ['Action'],
        'directors': [app.director_names[0],],
        'keywords': [app.keyword_names[0], app.keyword_names[1], app.keyword_names[2],],
        'budget' : 1000000,
        'season' : 'winter'
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

print 'Season: ', args['season']


print('--------------------')
print('Predict request')
results = app.predict_request(args)
print(results)

