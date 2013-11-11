from cinema.models import Film

all_films = Film.objects.all()

films = []
bads = []

for film in all_films:
    countries = film.country.all()
    if len(countries) > 0:
        films.append(film)
    else:
        bads.append(film)

print("Number of films with at least one country: {}".format(len(films)))
print("Total numbers of films: {}".format(len(all_films)))
print("Ration of films with no country: {}".format(float(len(bads))/len(all_films)))

for film in bads:
    print(u"Film with no country: {}".format(film.english_title))
