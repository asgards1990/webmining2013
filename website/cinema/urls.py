from django.conf.urls import patterns, url
from views import formcall, resultsForm, predictionForm


from django.conf.urls import patterns, include, url
from django.shortcuts import render

urlpatterns = patterns('cinema.views',
    url(r'^(.+)search/$', formcall),
    url(r'^results/$', resultsForm),
    url(r'^prediction/$', predictionForm),
)
