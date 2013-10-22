from django.shortcuts import render
from autocomplete_app.forms import MultipleActorSearchForm, FilmSearchForm
from django.http import HttpResponse
from cinema.forms import HomeForm, ResultsForm, PredictionForm

def filmsearch(request):
    if request.method == 'POST':
        form = MultipleActorSearchForm(request.POST)
        if form.is_valid():
            return render(request, 'thanks.html')
    else:
        form = MultipleActorSearchForm()
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
