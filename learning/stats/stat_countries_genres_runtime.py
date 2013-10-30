from cinema.models import Film

all_films = Film.objects.all()

films = []

for film in all_films:
    countries = film.country.all()
    genres = film.genres.all()
    if len(countries) > 0 and len(genres) > 0 and film.runtime != None:
        films.append(film)


print("Number of films with genres, countries and runtim: {}".format(len(films)))
print("Total numbers of films: {}".format(len(all_films)))
