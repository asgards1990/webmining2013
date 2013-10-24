#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'cinema.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^results/$', 'cinema.views.resultsForm', name='results'),
    url(r'^prediction/$', 'cinema.views.predictionForm'),
    url(r'^search/', 'cinema.views.filmsearch')
)

#urlpatterns += staticfiles_urlpatterns()
