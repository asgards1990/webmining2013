from django.conf.urls import patterns, url
from views import filmsearch, resultsForm, predictionForm
#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.shortcuts import render

urlpatterns = patterns('cinema.views',
    #Formulaire de recherch de film
    url(r'^filmsearch/$', 'filmsearch'),
    url(r'^results/$', 'resultsForm'),
    url(r'^prediction/$', 'predictionForm'),
)
