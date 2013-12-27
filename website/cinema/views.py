from django.shortcuts import render
import autocomplete_app.forms as forms
from django.http import HttpResponse
from cinema.models import Film, ActorWeight, Person
from django.utils import simplejson

def filmInfo(request):
    if request.method == 'POST':
        film_id = request.POST.get('film_id')
    else:
        return HttpResponse("Field film_id required with POST method.")
    
    try:
        film = Film.objects.get(imdb_id = film_id)
    except Film.DoesNotExist:
        return HttpReponse("No movie found for " + str(film_id) + ".")
    
    actor_ids = film.actorweight_set.values_list("id")[:5]
    outputActors = []
    
    for item in actor_ids:
        try:
            actor = Person.objects.get(id = item[0])
    	    actorDico = {'imdb_id':actor.imdb_id,'name':actor.name,'image_url':actor.image_url}
    	    outputActors.append(actorDico)
        except Person.DoesNotExist:
            pass
    
    outputGenres = map(lambda e:e['name'], film.genres.values('name'))
    
    directors = film.directors.all()
    outputDirectors =[]
    for director in directors:
	    directorDico = {'imdb_id':director.imdb_id, 'name':director.name, 'image_url':director.image_url}
	    outputDirectors.append(directorDico)
    
    output = {'budget' : film.budget, 'plot': film.imdb_summary, 'poster':film.image_url, 'imbd_id': film.imdb_id,
              'english_title': film.english_title,'original_title':film.original_title, 'genres': outputGenres,
              'release_date':film.release_date.isoformat(),'actors':outputActors, 'directors':outputDirectors}
    
    response = HttpResponse(simplejson.dumps(output), mimetype='application/json')
    #response['Access-Control-Allow-Origin']  = 'null'
    response['Access-Control-Allow-Methods'] = 'GET,POST'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    
    return response
