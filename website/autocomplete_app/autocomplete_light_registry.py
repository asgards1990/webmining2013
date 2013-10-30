import autocomplete_light

from cinema.models import Film, Person, Genre, Keyword

# Autocompletion pour un film
class FilmAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['original_title','english_title']
    autocomplete_js_attributes={'placeholder': 'Title ?'}
    
autocomplete_light.register(Film, FilmAutocomplete)

# Autocompletion pour une personne
class PersonAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields=['name']
    autocomplete_js_attributes={'placeholder': 'Name ?'}
    choice_template = 'autocomplete/person_autocomplete.html'
    
autocomplete_light.register(Person, PersonAutocomplete, name='Actor',
                            choices = (Person.objects.filter(actorweight__rank__isnull=False)))
                            
autocomplete_light.register(Person, PersonAutocomplete, name='Director',
                            choices = (Person.objects.filter(films_from_director__imdb_id__isnull=False)).distinct())
                            
                            
# Autocompletion pour genre + keywords
class GenreAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['name']
    autocomplete_js_attributes={'placeholder': 'Genre ?'}

autocomplete_light.register(Genre, GenreAutocomplete)

class KeywordAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['word']
    autocomplete_js_attributes={'placeholder': 'Keyword ?'}
    
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




