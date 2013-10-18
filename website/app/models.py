from django.db import models

# Create your models here.

from django.core.validators import RegexValidator

class  Country (models.Model):
    name = models.CharField(max_length=255, unique=True)
    nationality = models.CharField(max_length=255, unique=True) 
    def __unicode__(self):
        return self.name       
    class Meta:
        ordering = ['name']
        
class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __unicode__(self):
        return self.name    
    class Meta:
        ordering = ['name']
        
class  Genre (models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class  Reviewer (models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, validators=[RegexValidator('(m|f)')], null=True)
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']
        
class  Journal (models.Model):
    name = models.CharField(max_length=255)
    prestige = models.FloatField(min=0.0, max=1.0, null=True)
    country = models.ManyToManyField(Country, null=True)
    language = models.ManyToManyField(Language, null=True)
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']
  
class  Review (models.Model):
    grade = models.FloatField(min=0.0, max=10.0, null=True)
    summary = models.TextField(null=True)
    text = models.TextField(null=True)
    reviewer = models.ManyToManyField(Reviewer, null=True)
    journal = models.ManyToManyField(Journal, null=True)
    def __unicode__(self):
        return "{0} par {1} pour {2}".format(self.grade, self.reviewer.name, self.journal.name)       
    class Meta:
        ordering = ['-grade']
        
class  ProductionCompany (models.Model):
    imdb_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, unique=True)
    country = models.ManyToManyField(Country, null=True)
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']
        
class  Institution (models.Model):
    name = models.CharField(max_length=255)
    prestige = models.FloatField(min=0.0, max=1.0, null=True)
    country = models.ManyToManyField(Country, null=True)
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']

class  Prize (models.Model):
    award = models.CharField(max_length=255)
    level = models.CharField(max_length=1, validators=[RegexValidator('(n|w)')]) #nomination or win
    prestige = models.FloatField(min=0.0, max=1.0, null=True)
    year = models.IntegerField(null=True)
    institution = models.ManyToManyField(Institution)
    def __unicode__(self):
        return "{0} pour {1} en {2}".format(self.level, self.award, self.year)   
    class Meta:
        ordering = ['year', 'institution', 'award']
        
class  Person (models.Model):
    imdb_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, validators=[RegexValidator('(m|f)')], null=True) #restreindre masculin et féminin / imdb ne fournit que le sexe des acteurs
    bith_date = models.DateField(null=True)
    countries = models.ManyToManyField(Country, null=True)
    prizes = models.ManyToManyField(Prize, null=True)
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    class Meta:
        ordering = ['last_name','first_name']
        
class  Film (models.Model):
    imdb_id = models.CharField(max_length=10, unique=True)
    title_original = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255)
    title_french = models.CharField(max_length=255)
    release_date = models.DateField()
    countries = models.ManyToManyField(Country, null=True)
    synopsis_wiki = models.TextField(null=True)
    synopsis_imdb = models.TextField(null=True)
    budget = models.IntegerField(null=True)
    box_office = models.IntegerField(null=True)
    keywords = models.TextField(null=True)
    actors = models.ManyToManyField(Person, through='ActorWeight')
    directors = models.ManyToManyField(Person, through='DirectorWeight')
    writers = models.ManyToManyField(Person, through='WriterWeight')
    production_companies = models.ManyToManyField(ProductionCompany, through='ProductionCompanyWeight', null=True)
    genres = models.ManyToManyField(Genre, null=True)
    prizes = models.ManyToManyField(Prize, null=True)
    languages = models.ManyToManyField(Language, null=True)
    reviews = models.ManyToManyField(Review, null=True)
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    class Meta:
        ordering = ['last_name','first_name']
   
class ActorWeight(models.Model):
    weight = models.FloatField(min=0.0, max = 1.0)
    actor = models.ForeignKey(Person)
    film = models.ForeignKey(Film)
    def __unicode__(self):
        return "{0} joue dans {1} avec le poids {2}".format(self.actor, self.film, self.weight)

class DirectorWeight(models.Model):
    weight = models.FloatField(min=0.0, max = 1.0)
    director = models.ForeignKey(Person)
    film = models.ForeignKey(Film)
    def __unicode__(self):
        return "{0} réalise {1} avec le poids {2}".format(self.director, self.film, self.weight)

class WriterWeight(models.Model):
    weight = models.FloatField(min=0.0, max = 1.0)
    writer = models.ForeignKey(Person)
    film = models.ForeignKey(Film)
    def __unicode__(self):
        return "{0} écrit {1} avec le poids {2}".format(self.writer, self.film, self.weight)

class ProductionCompanyWeight(models.Model):
    weight = models.FloatField(min=0.0, max = 1.0)
    production_company = models.ForeignKey(ProductionCompany)
    film = models.ForeignKey(Film)
    def __unicode__(self):
        return "{0} produit {1} avec le poids {2}".format(self.production_company, self.film, self.weight)
  
class  Keyword (models.Model): #Verifier si ok
    word = models.CharField(max_length=255, unique=True)
    films = models.ManyToManyField(Film)
    def __unicode__(self):
        return self.word     
    class Meta:
        ordering = ['word']

class FilmImage (models.Model):
    filename = models.CharField(max_length=255, unique=True)
    film = models.ManyToManyField(Film)
    def __unicode__(self):
        return self.filename  
    class Meta:
        ordering = ['filename']
        
class PersonImage (models.Model):
    filename = models.CharField(max_length=255, unique=True)
    person = models.ManyToManyField(Person)
    def __unicode__(self):
        return self.filename  
    class Meta:
        ordering = ['filename']
