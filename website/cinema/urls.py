from django.conf.urls import patterns, url
from views import filmsearch, resultsForm, predictionForm

urlpatterns = patterns('',
    #Formulaire de recherch de film
    url(r'^filmsearch/$', filmsearch),
    url(r'^results/$', resultsForm),
    url(r'^prediction/$', predictionForm),
)
