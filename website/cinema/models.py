from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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
    gender = models.CharField(max_length=1, validators=[RegexValidator('(m|f)')], null=True,blank=True)
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']
        
class  Journal (models.Model):
    name = models.CharField(max_length=255)
    prestige = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)], null=True,blank=True)
    country = models.ManyToManyField(Country, null=True,blank=True)
    language = models.ManyToManyField(Language, null=True,blank=True)
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']
  
class  Review (models.Model):
    grade = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(10.0)], null=True,blank=True)
    summary = models.TextField(null=True,blank=True)
    text = models.TextField(null=True,blank=True)
    reviewer = models.ManyToManyField(Reviewer, null=True,blank=True)
    journal = models.ManyToManyField(Journal, null=True,blank=True)
    def __unicode__(self):
        return "{0} par {1} pour {2}".format(self.grade, self.reviewer.name, self.journal.name)       
    class Meta:
        ordering = ['-grade']
        
class  ProductionCompany (models.Model):
    imdb_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, unique=True)
    country = models.ManyToManyField(Country, null=True,blank=True)
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']
        
class  Institution (models.Model):
    name = models.CharField(max_length=255)
    prestige = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)], null=True,blank=True)
    country = models.ManyToManyField(Country, null=True,blank=True)
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']

class  Prize (models.Model):
    award = models.CharField(max_length=255)
    level = models.CharField(max_length=1, validators=[RegexValidator('(n|w)')]) #nomination or win
    prestige = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)], null=True,blank=True)
    year = models.IntegerField(null=True,blank=True)
    institution = models.ManyToManyField(Institution)
    def __unicode__(self):
        return "{0} for award named {1} in {2}".format(self.level, self.award, self.year)   
    class Meta:
        ordering = ['year', 'award']
        
class  Person (models.Model):
    imdb_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, validators=[RegexValidator('(m|f)')], null=True,blank=True) #restreindre masculin et feminin / imdb ne fournit que le sexe des acteurs
    bith_date = models.DateField(null=True,blank=True)
    countries = models.ManyToManyField(Country, null=True,blank=True)
    prizes = models.ManyToManyField(Prize, null=True,blank=True)
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    class Meta:
        ordering = ['last_name','first_name']
        
class  Film (models.Model):
    imdb_id = models.CharField(max_length=10, unique=True)
    title_original = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255,blank=True,null=True)
    title_french = models.CharField(max_length=255,blank=True,null=True)
    release_date = models.DateField()
    countries = models.ManyToManyField(Country, null=True, blank=True)
    synopsis_wiki = models.TextField(null=True,blank=True)
    synopsis_imdb = models.TextField(null=True,blank=True)
    budget = models.IntegerField(null=True,blank=True)
    box_office = models.IntegerField(null=True,blank=True)
    keywords = models.TextField(null=True,blank=True)
    actors = models.ManyToManyField(Person, through='ActorWeight', related_name='aw')
    directors = models.ManyToManyField(Person, through='DirectorWeight', related_name='dw')
    writers = models.ManyToManyField(Person, through='WriterWeight', related_name='ww')
    production_companies = models.ManyToManyField(ProductionCompany, through='ProductionCompanyWeight', null=True)
    genres = models.ManyToManyField(Genre, null=True,blank=True)
    prizes = models.ManyToManyField(Prize, null=True,blank=True)
    languages = models.ManyToManyField(Language, null=True,blank=True)
    reviews = models.ManyToManyField(Review, null=True,blank=True)
    def __unicode__(self):
        return u'%s' % (self.title_original)
    class Meta:
        ordering = ['title_original']
   
class ActorWeight(models.Model):
    weight = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)])
    actor = models.ForeignKey(Person, related_name='actor_in_aw')
    film = models.ForeignKey(Film, related_name='film_in_aw')
    def __unicode__(self):
        return "{0} plays in {1} with weight {2}".format(self.actor, self.film, self.weight)

class DirectorWeight(models.Model):
    weight = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)])
    director = models.ForeignKey(Person, related_name='director_in_dw')
    film = models.ForeignKey(Film, related_name='film_in_dw')
    def __unicode__(self):
        return "{0} has directed {1} with weight {2}".format(self.director, self.film, self.weight)

class WriterWeight(models.Model):
    weight = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)])
    writer = models.ForeignKey(Person, related_name='writer_in_ww')
    film = models.ForeignKey(Film, related_name='film_in_ww')
    def __unicode__(self):
        return "{0} has written {1} with weight {2}".format(self.writer, self.film, self.weight)

class ProductionCompanyWeight(models.Model):
    weight = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)])
    production_company = models.ForeignKey(ProductionCompany, related_name='production_company_in_pcw')
    film = models.ForeignKey(Film, related_name='film_in_pcw')
    def __unicode__(self):
        return "{0} has produced {1} with weight {2}".format(self.production_company, self.film, self.weight)
  
class  Keyword (models.Model):
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



