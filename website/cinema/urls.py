from django.conf.urls import patterns, url
from views import formcall, resultsForm, predictionForm

urlpatterns = patterns('',
    #Formulaire de recherch de film
    url(r'^(.+)search/$', formcall),
    url(r'^results/$', resultsForm),
    url(r'^prediction/$', predictionForm),
)
