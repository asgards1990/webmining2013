from cinema.models import Film

all_films = Film.objects.all()

films = []
bads = []
for film in all_films:
    genres = film.genres.all()
    if len(genres) > 0:
        films.append(film)
    else:
        bads.append(film)

print("Number of films with at least one genre: {}".format(len(films)))
print("Total numbers of films: {}".format(len(all_films)))

print("Ration of films with no genre : {}".format(float(len(bads))/len(all_films)))

for film in bads:
    print(u"Film with no genre: {}".format(film.english_title))
