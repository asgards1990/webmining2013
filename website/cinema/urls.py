from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from views import filmsearch

urlpatterns = patterns('',
    #Formulaire de recherch de film
    url(r'^filmsearch/', filmsearch),
)