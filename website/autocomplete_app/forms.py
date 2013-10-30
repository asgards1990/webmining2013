from django import forms
import autocomplete_light
from models import PersonsSearch, GKSearch, Prediction
from cinema.models import Person
from autocomplete_light import FixedModelForm
        
# Selection d'un film
class FilmSearchForm(forms.Form):        
    title_original = forms.CharField(widget=autocomplete_light.TextWidget('FilmAutocomplete'))
          
# Selection multiple d'acteurs        
class MultipleActorSearchForm(FixedModelForm):
    personnes = forms.ModelMultipleChoiceField(Person.objects.all(),widget=autocomplete_light.MultipleChoiceWidget('Actor'))
    class Meta :
        model = PersonsSearch
        
# Selection multipl de producteurs       
class MultipleDirectorSearchForm(FixedModelForm):
    personnes = forms.ModelMultipleChoiceField(Person.objects.all(),widget=autocomplete_light.MultipleChoiceWidget('Director'))
    class Meta :
        model = PersonsSearch
        
#Formulaire de selection genre + keywords
class GKSearchForm(FixedModelForm):
    class Media :
        js = ('javascript/dependant_autocomplete.js',)
    class Meta :
        model = GKSearch
        widgets = autocomplete_light.get_widgets_dict(GKSearch)
        
class PredictionForm(FixedModelForm):
    actors = forms.ModelMultipleChoiceField(Person.objects.all(),widget=autocomplete_light.MultipleChoiceWidget('Actor'))
    directors = forms.ModelMultipleChoiceField(Person.objects.all(),widget=autocomplete_light.MultipleChoiceWidget('Actor'))
    class Media :
        js = ('javascript/dependant_autocomplete.js',)
    class Meta :
        model = Prediction
        widgets = autocomplete_light.get_widgets_dict(Prediction)