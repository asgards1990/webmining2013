from django.shortcuts import render
from autocomplete_app.forms import MultipleActorSearchForm, FilmSearchForm
from django.http import HttpResponse
from cinema.forms import HomeForm, ResultsForm, PredictionForm
from cinema.models import *
from django.db.models import Q

def filmsearch(request):
    if request.method == 'POST':
        #form = MultipleActorSearchForm(request.POST)
        form = FilmSearchForm(request.POST)
	if form.is_valid():
            return render(request, 'thanks.html')
    else:
        #form = MultipleActorSearchForm()
        form = FilmSearchForm()
    return render(request, 'actor.html', {'form': form})

def home(request):
    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            recherche = form.cleaned_data['recherche']
            criteriaActorsDirector = form.cleaned_data['criteriaActorsDirector']
            criteriaGenre = form.cleaned_data['criteriaGenre']
            criteriaBudget = form.cleaned_date['criteriaBudget']
            criteriaReview = form.cleaned_date['criteriaReview']
              
            send = True

        else:
            form = HomeForm()

    return render(request, 'home.html', locals())

def resultsForm(request):
    if request.method == 'POST':
        form = ResultsForm(request.POST)
        if form.is_valid():
            criteriaActorsDirector = form.cleaned_data['criteriaActorsDirector']
            criteriaGenre = form.cleaned_data['criteriaGenre']
            criteriaBudget = form.cleaned_date['criteriaBudget']
            criteriaReview = form.cleaned_date['criteriaReview']
            director = form.cleaned_date['director']
            actors = form.cleaned_date['actors']
            genre = form.cleaned_date['genre']
            budget = form.cleaned_date['budget']
            review = form.cleaned_date['review']
              
            send = True

        else:
            form = ResultsForm()

    return render(request, 'results.html',locals())

def predictionForm(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            criteriaActorsDirector = form.cleaned_data['criteriaActorsDirector']
            criteriaGenre = form.cleaned_data['criteriaGenre']
            criteriaBudget = form.cleaned_date['criteriaBudget']
            criteriaReview = form.cleaned_date['criteriaReview']
            director = form.cleaned_date['director']
            actors = form.cleaned_date['actors']
            genre = form.cleaned_date['genre']
            budget = form.cleaned_date['budget']
            review = form.cleaned_date['review']
            keyWords = form.cleaned_date['keyWords']
              
            send = True

        else:
            form = PredictionForm()

    return render(request, 'prediction.html',locals())

def searchresults(request,nomFilm):
   for film in Film.objects.get(Q(original_title=nomFilm) | Q(english_title=nomFilm)):
        imdb_id=film.imdb_id
        actors=film.actors
        genres=film.genres
        keywords=film.keywords
        writers=film.writers
        image_url=film.image_url
        ratings=film.imdb_nb_user_ratings
        reviews=film.imdb_nb_user_reviews
        pitch=film.imdb_summary
        resume=film.imdb_storyline
        budget=film.budget
        box_office=film.box_office
    

        return render(request, 'prediction.html',locals())
