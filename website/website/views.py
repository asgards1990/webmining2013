from django.shortcuts import render
import autocomplete_app.forms as forms

def home(request):
    return render(request, 'home.html')
    
def prediction(request):
    form = forms.PredictionForm()
    return render(request, 'prediction_menu.html', {'form': form})
	
def explore(request):
    form=forms.FilmSearchForm()
    return render(request, 'explore_menu.html', {'form': form})

