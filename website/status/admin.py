from django.contrib import admin
from status.models import IMDBFilmStatus, IMDBPersonStatus, IMDBCompanyStatus
from status.models import ScrapyStatus

admin.site.register(ScrapyStatus)

class IMDBFilmStatusAdmin(admin.ModelAdmin):
    list_display = ('imdb_id', 'year', 'position', 
                    'film_mainpage', 'film_fullcredits', 'film_awards', 'film_reviews', 'film_keywords', 'film_companycredits',
                    'film_image',
                    'downloaded', 'extracted', 'priority')
    search_fields = ('imdb_id',)
    list_filter = ('year', 'downloaded', 'extracted',)

class IMDBPersonStatusAdmin(admin.ModelAdmin):
    list_display = ('imdb_id', 'downloaded', 'extracted')
    search_fields = ('imdb_id',)
    list_filter = ('downloaded', 'extracted',)

class IMDBCompanyStatusAdmin(admin.ModelAdmin):
    list_display = ('imdb_id', 'downloaded', 'extracted')
    search_fields = ('imdb_id',)
    list_filter = ('downloaded', 'extracted',)

admin.site.register(IMDBFilmStatus, IMDBFilmStatusAdmin)
admin.site.register(IMDBPersonStatus, IMDBPersonStatusAdmin)
admin.site.register(IMDBCompanyStatus, IMDBCompanyStatusAdmin)
