#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from cinema.forms import HomeForm, ResultsForm, PredictionForm

def home(request):
    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            recherche = form.cleaned_data['recherche']
            criteriaActorsDirector = form.cleaned_data['criteriaActorsDirector']
            criteriaGenre = forms.cleaned_data['criteriaGenre']
            criteriaBudget = forms.cleaned_date['criteriaBudget']
            criteriaReview = forms.cleaned_date['criteriaReview']
              
            send = True

        else:
            form = HomeForm()

    return render(request, 'test.html', locals())

def resultsForm(request):
    if request.method == 'POST':
        form = ResultsForm(request.POST)
        if form.is_valid():
            criteriaActorsDirector = form.cleaned_data['criteriaActorsDirector']
            criteriaGenre = forms.cleaned_data['criteriaGenre']
            criteriaBudget = forms.cleaned_date['criteriaBudget']
            criteriaReview = forms.cleaned_date['criteriaReview']
            director = forms.cleaned_date['director']
            actors = forms.cleaned_date['actors']
            genre = forms.cleaned_date['genre']
            budget = forms.cleaned_date['budget']
            review = forms.cleaned_date['review']
              
            send = True

        else:
            form = ResultsForm()

    return render(request, 'test.html',locals())

def predictionForm(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            criteriaActorsDirector = form.cleaned_data['criteriaActorsDirector']
            criteriaGenre = forms.cleaned_data['criteriaGenre']
            criteriaBudget = forms.cleaned_date['criteriaBudget']
            criteriaReview = forms.cleaned_date['criteriaReview']
            director = forms.cleaned_date['director']
            actors = forms.cleaned_date['actors']
            genre = forms.cleaned_date['genre']
            budget = forms.cleaned_date['budget']
            review = forms.cleaned_date['review']
            keyWords = forms.cleaned_date['keyWords']
              
            send = True

        else:
            form = PredictionForm()

    return render(request, 'test.html',locals())


