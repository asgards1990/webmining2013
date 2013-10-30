from cinema.models import Film

all_films = Film.objects.all()

films = Film.objects.exclude(runtime=None)        
bads = Film.objects.filter(runtime=None)

print("Number of films with at least one country: {}".format(len(films)))
print("Total numbers of films: {}".format(len(all_films)))


for film in bads:
    print(u"Film with no country: {}".format(film.english_title))
