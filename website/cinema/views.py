from django.shortcuts import render
import autocomplete_app.forms as forms
from django.http import HttpResponse
from cinema.models import Film, ActorWeight, Person
from django.utils import simplejson

def filmInfo(request):
    if request.method == 'POST':
        film_id = request.POST.get('film_id')
    else:
        return HttpResponse("Erreur")

    try:
        film = Film.objects.get(imdb_id = film_id)
    except Film.DoesNotExist:
        return HttpReponse("movie not found",)                

    film = Film.objects.get(imdb_id = film_id)
    actor_ids = ActorWeight.objects.filter(film=film).order_by('rank').values_list('actor_id')
    actors = Person.objects.in_bulk(actor_ids)
    l = len(actors)
    outputActors =[]
    for item in actor_ids[:5]:
	actor=actors[item[0]]
	actorDico = {'imdb_id':actor.imdb_id,'name':actor.name,'image_url':actor.image_url}  
	outputActors.append(actorDico)
	
    genres = film.genres.all()
    z = len(genres)
    outputGenres =[]
    for k in range(z):
        genre = genres[k]
        outputGenres.append(genre.name)


    directors = film.directors.all()
    y = len(directors)
    outputDirectors =[]
    for k in range(y):
        director=directors[k]
	directorDico = {'imdb_id':director.imdb_id,'name':director.name,'image_url':director.image_url}  
	outputDirectors.append(directorDico)
	
    output = {'budget' : film.budget, 'plot': film.imdb_summary, 'poster':film.image_url, 'imbd_id': film.imdb_id,
              'english_title': film.english_title,'original_title':film.original_title, 'genres': outputGenres,
              'release_date':film.release_date.isoformat(),'actors':outputActors, 'directors':outputDirectors}
    
    response = HttpResponse(simplejson.dumps(output), mimetype='application/json')
    #response['Access-Control-Allow-Origin']  = 'null'
    response['Access-Control-Allow-Methods'] = 'GET,POST'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    
    return response
