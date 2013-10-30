from django.shortcuts import render
import autocomplete_app.forms as forms
from cinema.forms import HomeForm, ResultsForm, PredictionForm

# Choix du formulaire
def formchoice(persontype,request=0) :
    possibilites = ['actor','director','film','genre','prediction']
    if persontype in possibilites :
        if request == 0:
            if persontype == 'actor' :
                form = forms.MultipleActorSearchForm()
            elif persontype == 'director' :
                form = forms.MultipleDirectorSearchForm()
            elif persontype == 'film' :
                form = forms.FilmSearchForm()
            elif persontype == 'genre' :
                form = forms.GKSearchForm()
            elif persontype == 'prediction' :
                form = forms.PredictionForm()
        else : 
            if persontype == 'actor' :
                form = forms.MultipleActorSearchForm(request.POST)
            elif persontype == 'director' :
                form = forms.MultipleDirectorSearchForm(request.POST)
            elif persontype == 'film' :
                form = forms.FilmSearchForm(request.POST)
            elif persontype == 'genre' :
                form = forms.GKSearchForm(request.POST)
            elif persontype == 'prediction' :
                form = forms.PredictionForm(request.POST)
    else : 
        return 0,'pb.html'
    return form,'formulaire.html'

# Vue appel de formulaire
def formcall(request,persontype):
    if request.method == 'POST'and len(request.POST)>1 :
        form,template=formchoice(persontype,request)
        if form.is_valid():
            return render(request, 'thanks.html')
    else :
        form,template=formchoice(persontype)
    return render(request, template, {'form': form})

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
