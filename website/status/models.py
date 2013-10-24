# /usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Model for IMDB status
class IMDBFilmStatus(models.Model):
    imdb_id = models.CharField(max_length=9)    # the IMDB identifier
    year = models.IntegerField()                # the release year
    position = models.IntegerField()            # the page in which the film appears
    # we need to download several webpages for each film
    film_mainpage = models.IntegerField()       
    film_fullcredits = models.IntegerField()
    film_awards = models.IntegerField()
    film_reviews = models.IntegerField()
    film_keywords = models.IntegerField()
    film_companycredits = models.IntegerField()
    # film poster
    film_image = models.IntegerField()
    # status for downloader and extracter
    downloaded = models.IntegerField()
    extracted = models.IntegerField()
    
class IMDBPersonStatus(models.Model):
    imdb_id = models.CharField(max_length=9)    # the IMDB identifier
    # status for downloader and extracter
    downloaded = models.IntegerField()
    extracted = models.IntegerField()

class IMDBCompanyStatus(models.Model):
    imdb_id = models.CharField(max_length=9)    # the IMDB identifier
    # status for downloader and extracter
    downloaded = models.IntegerField()
    extracted = models.IntegerField()

