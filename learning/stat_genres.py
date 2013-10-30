from cinema.models import Film

all_films = Film.objects.all()

films = []
for film in all_films:
    genres = film.genres.all()
    if len(genres) > 0:
        films.append(film)

print("Number of films with at least one genre: {}".format(len(films)))
print("Total numbers of films: {}".format(len(films)))
