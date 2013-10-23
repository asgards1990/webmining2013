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
    identifier = models.CharField(max_length=10, unique=True)
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
    name = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=1, validators=[RegexValidator('(m|f)')], null=True,blank=True) #later
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']

class  Journal (models.Model):
    name = models.CharField(max_length=255, unique=True)
    language = models.ForeignKey(Language, blank=True, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL) #later
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']

class  Person (models.Model):
    imdb_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True,blank=True)
    image_url = models.CharField(blank=True, max_length=255)
    birth_country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL)
    gender = models.CharField(max_length=1, validators=[RegexValidator('(m|f)')],blank=True) #later
    first_name = models.CharField(max_length=255, blank=True) #later
    last_name = models.CharField(max_length=255, blank=True) #later
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        ordering = ['name']

class  ProductionCompany (models.Model):
    imdb_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL) #later
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']

class  Institution (models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL) #later
    def __unicode__(self):
        return self.name      
    class Meta:
        ordering = ['name']

class  Keyword (models.Model):
    word = models.CharField(max_length=255, unique=True)
    def __unicode__(self):
        return self.word
    class Meta:
        ordering = ['word']

class  Film (models.Model):
    imdb_id = models.CharField(max_length=10, unique=True)
    original_title = models.CharField(max_length=255)
    english_title = models.CharField(max_length=255,blank=True)
    release_date = models.DateField()
    runtime = models.IntegerField(null=True,blank=True)
    budget = models.IntegerField(null=True,blank=True)
    box_office = models.IntegerField(null=True,blank=True)
    imdb_user_rating = models.FloatField(null=True,blank=True)
    imdb_nb_user_ratings = models.IntegerField(null=True,blank=True)
    imdb_nb_user_reviews = models.IntegerField(null=True,blank=True)
    imdb_nb_reviews = models.IntegerField(null=True,blank=True)
    imdb_summary = models.TextField(blank=True)
    imdb_storyline = models.TextField(blank=True)
    metacritic_score = models.IntegerField(null=True,blank=True)
    allocine_score = models.FloatField(null=True,blank=True)
    allocine_synopsis = models.TextField(blank=True)
    wikipedia_synopsis = models.TextField(blank=True)
    image_url = models.CharField(blank=True, max_length=255)
    language = models.ForeignKey(Language, blank=True, null=True, on_delete=models.SET_NULL)
    country = models.ManyToManyField(Country, blank=True, null=True, related_name="films")
    genres = models.ManyToManyField(Genre, blank=True, null=True, related_name="films")
    keywords = models.ManyToManyField(Keyword, blank=True, null=True, related_name="films")
    production_company = models.ManyToManyField(ProductionCompany, blank=True, null=True, related_name="films")
    directors = models.ManyToManyField(Person, blank=True, null=True, related_name='films_from_director')
    writers = models.ManyToManyField(Person, blank=True, null=True, related_name='films_from_writer')
    actors = models.ManyToManyField(Person, blank=True, null=True, through='ActorWeight', related_name='films_from_actor')
    def __unicode__(self):
        return u'%s' % (self.original_title)
    class Meta:
        ordering = ['original_title', 'release_date']

class  Prize (models.Model):
    win = models.BooleanField()
    year = models.IntegerField(null=True,blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    def __unicode__(self):
        return "{0} in {1} for film {2}. Won : {3}".format(self.institution.name, self.year, self.film.original_title, self.win)
    class Meta:
        ordering = ['year']

class  Review (models.Model):
    grade = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(1.0)], null=True,blank=True)
    summary = models.TextField(blank=True)
    text = models.TextField(blank=True)
    reviewer = models.ForeignKey(Reviewer, blank=True, null=True, on_delete=models.SET_NULL)
    journal = models.ForeignKey(Journal, blank=True, null=True, on_delete=models.SET_NULL)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    full_review_url = models.URLField(blank=True)
    def __unicode__(self):
        return "{0} from {1} for {2}".format(self.grade, self.reviewer.name, self.journal.name)       
    class Meta:
        ordering = ['-grade']

class ActorWeight(models.Model):
    rank = models.IntegerField(null=True,blank=True)
    star = models.BooleanField(default=False)
    actor = models.ForeignKey(Person, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    def __unicode__(self):
        return "{0} played in {1} and is ranked {2} in credits. Star : {3}".format(self.actor, self.film, self.rank, self.star)

class JournalInfluence(models.Model):
    influence = models.FloatField(null=True,blank=True)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    def __unicode__(self):
        return "{0} has influence {1} for {2} films".format(self.journal.name, self.influence, self.genre.name)
    class Meta:
        ordering = ['-influence']

class InstitutionInfluence(models.Model):
    influence = models.FloatField(null=True,blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    def __unicode__(self):
        return "{0} has influence {1} for {2} films in {3}".format(self.institution.name, self.influence, self.genre.name, self.country.name)
    class Meta:
        ordering = ['-influence']

class GenrePopularKeyword(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    occurences = models.IntegerField()
    def __unicode__(self):
        return "{0} occurs {1} times in {2} films".format(self.keyword.word, self.occurences, self.genre.name)
    class Meta:
        ordering = ['-occurences']
