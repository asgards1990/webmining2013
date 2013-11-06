from cinema.models import Film
from status.models import IMDBFilmStatus

def filter1():
    print('Nb of films in DB : ' + str(Film.objects.count()))
    films = Film.objects.exclude(runtime=None).exclude(genres=None).exclude(country=None).exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).exclude(box_office=None)
    #for film in films.all():
    #    if film.imdb_nb_user_reviews==None:
    #        film.imdb_nb_user_reviews=0
    #    if film.imdb_nb_reviews==None:
    #        film.imdb_nb_reviews=0
    print('Nb of films after cleaning : ' + str(films.count()) + '. Selected ' + str(100*float(films.count())/Film.objects.count()) + ' %.')
    return films

def filter2(n): #like filter1 but returns n films, useful for tests
    print('Nb of films in DB : ' + str(Film.objects.count()))
    films = Film.objects.exclude(runtime=None).exclude(genres=None).exclude(country=None).exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).exclude(box_office=None).exclude(release_date=None)[:n]
    #for film in films.all():
    #    if film.imdb_nb_user_reviews==None:
    #        film.imdb_nb_user_reviews=0
    #    if film.imdb_nb_reviews==None:
    #        film.imdb_nb_reviews=0
    print('Nb of films after cleaning : ' + str(films.count()) + '. Selected ' + str(100*float(films.count())/Film.objects.count()) + ' %.')
    return films


def filter3(year): #like filter1 but returns n films, useful for tests
    print('Nb of films in DB : ' + str(Film.objects.count()))
    all_films = Film.objects.exclude(runtime=None).exclude(genres=None).exclude(country=None).exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).exclude(box_office=None)
    films = []
    for film in all_films:
        if film.imdb_nb_user_reviews==None:
            film.imdb_nb_user_reviews=0
        if film.imdb_nb_reviews==None:
            film.imdb_nb_reviews=0
        status = IMDBFilmStatus.objects.filter(imdb_id=film.imdb_id)
        if len(status) > 0 and status[0].year >= year:
            films.append(film)
    print('Nb of films after cleaning : ' + str(films.count()) + '. Selected ' + str(100*float(films.count())/Film.objects.count()) + ' %.')
    return films

def filter_random(n):
    '''
    Return a queryset of n films uniformly chosen among "valid" films.
    '''
    films = Film.objects.exclude(runtime=None).exclude(genres=None).exclude(country=None).exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).exclude(box_office=None)
    for film in films:
        if film.imdb_nb_user_reviews==None:
            film.imdb_nb_user_reviews=0
        if film.imdb_nb_reviews==None:
            film.imdb_nb_reviews=0
    print('Nb of films after cleaning : ' + str(films.count()) + '. Selected ' + str(100*float( min(n,films.count()) )/Film.objects.count()) + ' %.')
    if n >= films.count():
        return films
    return films.order_by('?')[:n]
