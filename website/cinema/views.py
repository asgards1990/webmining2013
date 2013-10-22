from django.shortcuts import render
from autocomplete_app.forms import MultipleActorSearchForm, FilmSearchForm

def filmsearch(request):
    if request.method == 'POST':
        form = MultipleActorSearchForm(request.POST)
        if form.is_valid():
            return render(request, 'thanks.html')
    else:
        form = MultipleActorSearchForm()
    return render(request, 'actor.html', {'form': form})