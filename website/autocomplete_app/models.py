from django.db import models
from cinema.models import Person,Genre,Keyword

class PersonsSearch (models.Model):
    personnes = models.ManyToManyField(Person)
    
class GKSearch (models.Model):
    genre=models.ForeignKey(Genre)
    keyword=models.ManyToManyField(Keyword)
    
class Prediction (models.Model):
    actors = models.ManyToManyField(Person,related_name='actor')
    genre1 = models.ForeignKey(Genre,related_name='genre1')
    genre2 = models.ForeignKey(Genre,related_name='genre2')
    keyword = models.ManyToManyField(Keyword)
    director = models.ForeignKey(Person,related_name='director')

    
    
    