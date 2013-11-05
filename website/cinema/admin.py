from django.contrib import admin
from django.db.models import get_models, get_app
from cinema.models import Film

for model in get_models(get_app('cinema')):
    if model.__name__ != 'Film':
        admin.site.register(model)
        
class FilmAdmin(admin.ModelAdmin):
    search_fields = ('english_title', 'original_title')
    list_display = ('english_title', 'original_title', 'language', 'imdb_nb_user_ratings',  'imdb_user_rating', 'box_office', )
    list_filter = ('release_date', )
    raw_id_fields = ('keywords', 'production_companies', 'directors', 'writers', 'actors',)
    filter_horizontal = ('genres', 'country', )

admin.site.register(Film, FilmAdmin)