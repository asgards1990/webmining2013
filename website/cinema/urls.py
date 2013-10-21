#-*- coding: utf-8 -*-

from django.conf.urls import petterns, include, url
from django.shortcuts import render

urlpatterns = patterns ('cinema.views', url(r'^results/$', 'resultsForm') ,url(r'^prediction/$', 'predictionForm'))

