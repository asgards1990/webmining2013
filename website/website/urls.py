from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^cinema/', include('cinema.urls')),
)
urlpatterns += patterns('website.views',
    url(r'^$', 'home'),
    url(r'^prediction/$', 'prediction'),
	url(r'^explore/$', 'explore'),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('', url(r'^cinema/keywordGenre/','cinema.views.keywordGenre'))
