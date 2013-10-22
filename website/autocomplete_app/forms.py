from django import forms
import autocomplete_light
from models import MultipleActorSearch
from autocomplete_light import FixedModelForm
        
# Simple selection
class FilmSearchForm(forms.Form):        
    title_original = forms.CharField(widget=autocomplete_light.TextWidget('FilmAutocomplete'))
          
# Multiple selection         
class MultipleActorSearchForm(FixedModelForm):
    class Meta :
        model = MultipleActorSearch
        widgets = autocomplete_light.get_widgets_dict(MultipleActorSearch)