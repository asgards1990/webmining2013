from status.models import IMDBFilmStatus
from cinema.models import Film

films_with_img_downloaded = IMDBFilmStatus.objects.filter(film_image=1)

for s in films_with_img_downloaded:
    film = Film.objects.get(imdb_id = s.imdb_id)
    film.image_url = "poster/"+film.imdb_id+".jpg"
    film.save()
