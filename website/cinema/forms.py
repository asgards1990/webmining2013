#-*- coding: utf-8 -*-
from django import forms

class HomeForm(forms.Form):
    recherche = forms.CharField(max_length = 100)
    criteriaActorsDirector = forms.BooleanField(required=False)
    criteriaGenre = forms.BooleanField(required=False)
    criteriaBudget = forms.BooleanField(required=False)
    criteriaReview = forms.BooleanField(required=False)


class ResultsForm(forms.Form):
    criteriaActorsDirector = forms.BooleanField(required=False)
    criteriaGenre = forms.BooleanField(required=False)
    criteriaBudget = forms.BooleanField(required=False)
    criteriaReview = forms.BooleanField(required=False)
    director = forms.CharField(max_length = 50)
    actors = forms.CharField(max_length = 200)
    genre = forms.CharField(max_length = 200)
    budget = forms.IntegerField
    review = forms.CharField(max_length = 200)

class PredictionForm(forms.Form):
    criteriaActorsDirector = forms.BooleanField(required=False)
    criteriaGenre = forms.BooleanField(required=False)
    criteriaBudget = forms.BooleanField(required=False)
    criteriaReview = forms.BooleanField(required=False)
    director = forms.CharField(max_length = 50)
    actors = forms.CharField(max_length = 200)
    genre = forms.CharField(max_length = 200)
    budget = forms.IntegerField
    review = forms.CharField(max_length = 200)
    keyWords = forms.CharField(max_length = 100)




 

