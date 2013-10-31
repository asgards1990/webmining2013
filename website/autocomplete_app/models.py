from django.db import models
from cinema.models import Person,Genre,Keyword

class PersonsSearch (models.Model):
    personnes = models.ManyToManyField(Person)
    
class GKSearch (models.Model):
    genre=models.ForeignKey(Genre)
    keyword=models.ManyToManyField(Keyword)
    
class Prediction (models.Model):
    actors = models.ManyToManyField(Person,related_name='actor')
    genre = models.ForeignKey(Genre)
    keyword=models.ManyToManyField(Keyword)
    director = models.ManyToManyField(Person,related_name='director')

    
    
    