from cinema.models import Film

def filter1():
    print('Nb of films in DB : ' + str(Film.objects.count()))
    films = Film.objects.exclude(runtime=None).exclude(genres=None).exclude(country=None).exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).exclude(box_office=None)
    for film in films:
        if film.imdb_nb_user_reviews==None:
            film.imdb_nb_user_reviews=0
        if film.imdb_nb_reviews==None:
            film.imdb_nb_reviews=0
    print('Nb of films after cleaning : ' + str(films.count()) + '. Selected ' + str(float(films.count())/Film.objects.count()) + ' %.')
    return films

def filter2(): #like filter1 but returns 100 films, useful for tests
    print('Nb of films in DB : ' + str(Film.objects.count()))
    films = Film.objects.exclude(runtime=None).exclude(genres=None).exclude(country=None).exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).exclude(box_office=None)[:100]
    for film in films:
        if film.imdb_nb_user_reviews==None:
            film.imdb_nb_user_reviews=0
        if film.imdb_nb_reviews==None:
            film.imdb_nb_reviews=0
    print('Nb of films after cleaning : ' + str(films.count()) + '. Selected ' + str(float(films.count())/Film.objects.count()) + ' %.')
    return films
