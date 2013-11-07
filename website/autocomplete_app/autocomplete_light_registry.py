import autocomplete_light

from cinema.models import Film, Person, Genre, Keyword
from django.db.models import Q

# Autocompletion pour un film
class FilmAutocomplete(autocomplete_light.AutocompleteModelBase):
	search_fields=['original_title','english_title']
	autocomplete_js_attributes={'placeholder': 'Title ?'}
    
autocomplete_light.register(Film, FilmAutocomplete)

# Autocompletion pour une personne
class PersonAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields=['name']
    choice_template = 'autocomplete/person_autocomplete.html'
    
autocomplete_light.register(Person, PersonAutocomplete, name='Actor',
                            choices = (Person.objects.filter(Q(actorweight__rank__isnull=False) | Q(actorweight__star=True)).distinct()),
                            autocomplete_js_attributes={'placeholder': 'Add an actor by name',})
                            
autocomplete_light.register(Person, PersonAutocomplete, name='Director',
                            choices = (Person.objects.filter(Q(actorweight__rank__isnull=False) | Q(actorweight__star=True)).distinct()),
                            autocomplete_js_attributes={'placeholder': 'Add a director by name',})
                           
# Autocompletion simple genre-keywords
                           
class GenreAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['name']
    autocomplete_js_attributes={'placeholder': 'Add a genre','minimum_characters': 0,}

autocomplete_light.register(Genre, GenreAutocomplete)

class KeywordAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['word']
    autocomplete_js_attributes={'placeholder': 'Add a keyword',}
    
    def choices_for_request(self):
        q=self.request.GET.get('q','')
        genre_name=self.request.GET.get('genre_id',None)
        choices=self.choices.all()
        #Selection quand on ecrit le keyword
        if q:
            choices=choices.filter(word__icontains=q)
        #Selection par rapport au genre selectionne
        if genre_name :
            choices=choices.filter(genrepopularkeyword__genre__id=genre_name)
        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Keyword, KeywordAutocomplete)
                            
# Autocompletion pour double genre

class Genre1Autocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['name']
    autocomplete_js_attributes={'placeholder': 'Add a genre','minimum_characters': 0,}
    
    def choices_for_request(self):
        q=self.request.GET.get('q','')
        genre2_name=self.request.GET.get('genre2_id',None)
        choices=self.choices.all()
        if q:
            choices=choices.filter(name__icontains=q)
        if genre2_name and genre2_name !=-2:
            choices=choices.filter(~Q(id=genre2_name))
        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Genre, Genre1Autocomplete, name='genre1')

class Genre2Autocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['name']
    autocomplete_js_attributes={'placeholder': 'Add a genre','minimum_characters': 0,}
    
    def choices_for_request(self):
        q=self.request.GET.get('q','')
        genre1_name=self.request.GET.get('genre1_id',None)
        choices=self.choices.all()
        if q:
            choices=choices.filter(name__icontains=q)
        if genre1_name and genre1_name !=-2:
            choices=choices.filter(~Q(id=genre1_name))
        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Genre, Genre2Autocomplete, name='genre2')
                            
                            
# Autocompletion pour keywords a partir de genre1 et genre 2

class KeywordAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['word']
    autocomplete_js_attributes={'placeholder': 'Add a keyword','minimum_characters': 1,}
    
    def choices_for_request(self):
        q=self.request.GET.get('q','')
        genre1_name=self.request.GET.get('genre1_id',None)
        genre2_name=self.request.GET.get('genre2_id',None)
        choices=self.choices.all()
        #Selection quand on ecrit le keyword
        if q:
            choices=choices.filter(word__icontains=q)
        #Selection par rapport au genre selectionne
        if genre1_name and genre2_name and genre1_name !=-2 and genre2_name !=-2:
            choices=choices.filter(Q(genrepopularkeyword__genre__id=genre1_name) | Q(genrepopularkeyword__genre__id=genre2_name))
        elif genre1_name and genre1_name !=-2: 
            choices=choices.filter(genrepopularkeyword__genre__id=genre1_name)
        elif genre2_name and genre2_name  !=-2: 
            choices=choices.filter(genrepopularkeyword__genre__id=genre2_name)
        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Keyword, KeywordAutocomplete,name='keyword_complex')

class KeywordAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['word']
    autocomplete_js_attributes={'placeholder': 'Add a keyword','minimum_characters': 1,}

autocomplete_light.register(Keyword, KeywordAutocomplete,name='keyword_simple')


