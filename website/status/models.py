# /usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class ScrapyStatus(models.Model):
    imdb_id = models.CharField(max_length=9)
    year = models.IntegerField(blank=True, null=True)
    parsed = models.BooleanField()
    extracted = models.BooleanField()
    downloaded = models.BooleanField()

    def __unicode__(self):
        return u'%s is %s parsed and %s extracted. ' % (self.imdb_id, self.parsed, self.extracted)

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
    # priority
    priority = models.IntegerField()
    
    def __unicode__(self):
        return u'%s status' % (self.imdb_id)
    
class IMDBPersonStatus(models.Model):
    imdb_id = models.CharField(max_length=9)    # the IMDB identifier
    # status for downloader and extracter
    downloaded = models.IntegerField()
    extracted = models.IntegerField()
    priority = models.IntegerField()
    name = models.IntegerField()
    image = models.IntegerField()
    
    def __unicode__(self):
        return u'%s status' % (self.imdb_id)


class IMDBCompanyStatus(models.Model):
    imdb_id = models.CharField(max_length=9)    # the IMDB identifier
    # status for downloader and extracter
    downloaded = models.IntegerField()
    extracted = models.IntegerField()
    
    def __unicode__(self):
        return u'%s status' % (self.imdb_id)

class TableUpdateTime(models.Model):
    model_name = models.CharField(max_length=255,unique=True,default=None)
    update_time = models.DateTimeField(default=None)
    def __unicode__(self):
        return u'table for objects of class %s was last modified at %s' % (self.table.__name__, self.update_time)
