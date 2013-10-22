from django.db import models
from cinema.models import ActorWeight

class MultipleActorSearch (models.Model):
    actors = models.ManyToManyField(ActorWeight)