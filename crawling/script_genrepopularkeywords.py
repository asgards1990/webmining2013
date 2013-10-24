from cinema.models import *

def addOccurence(genre, keyword):
    result = GenrePopularKeywords.objects.filter(genre=genre, keyword=keyword)
    if result.exists():
        item = result[0]
        item.occurences = item.occurences + 1
        item.save()
    else:
        Keyword.objects.create(genre=genre, keyword=keyword, occurences=1)

for film in films:
    film_genres = film.genres.all()
    film_keywords = film.keywords.all()
    for film_genre in film_genres:
        for film_keyword in film_keywords:
            addOccurence(film_genre,film_keyword)
