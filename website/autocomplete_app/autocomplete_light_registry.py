import autocomplete_light

from cinema.models import Film, ActorWeight

class FilmAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['title_original','title_french','title_english']
    autocomplete_js_attributes={'placeholder': 'Title ?'}
    
autocomplete_light.register(Film, FilmAutocomplete)

class ActorWeightAutocomplete(autocomplete_light.AutocompleteModelBase):
    choices = (map(lambda x :  x.actor, ActorWeight.objects.all()))
    search_fields=(('weight'),)
    autocomplete_js_attributes={'placeholder': 'Name ?'}
    
autocomplete_light.register(ActorWeight, ActorWeightAutocomplete)


