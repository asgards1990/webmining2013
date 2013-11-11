from status.models import IMDBFilmStatus, IMDBPersonStatus
from cinema.models import Film, Person

films_with_img_downloaded = IMDBFilmStatus.objects.filter(film_image=1)
persons_with_img_downloaded = IMDBPersonStatus.objects.filter(image=1)

for s in films_with_img_downloaded:
    film = Film.objects.get(imdb_id = s.imdb_id)
    film.image_url = "poster/"+film.imdb_id+".jpg"
    film.save()

for s in persons_with_img_downloaded:
    person = Person.objects.get(imdb_id = s.imdb_id)
    person.image_url = "picture/"+film.imdb_id+".jpg"
    person.save()