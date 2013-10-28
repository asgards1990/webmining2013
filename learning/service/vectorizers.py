import numpy as np
from sklearn.feature_extraction import DictVectorizer
from cinema.models import *

measurements = []

films = Films.objects.all()
films = [] #to remove after
for film in films:
    countries = []
    for country in film.countries:
        countries.append(country.identifier)
    genres = []
    for genre in film.genres:
        genres.append(genre.name)
    keywords = []
    for keyword in film.keywords:
        keywords.append(keyword.word)
    production_companies = []
    for pc in film.production_companies:
        production_companies.append(pc.imdb_id)
    directors = []
    for director in film.directors:
        directors.append(director.imdb_id)
    writers = []
    for writer in film.writers:
        writers.append(writer.imdb_id)
    data = {
    'release_date':film.release_date,
    'runtime':film.runtime,
    'budget':film.budget,
    'box_office':film.box_office,
    'imdb_user_rating':film.imdb_user_rating,
    'imdb_nb_user_ratings':film.imdb_nb_user_ratings,
    'imdb_nb_user_reviews':film.imdb_nb_user_reviews,
    'imdb_nb_reviews':film.imdb_nb_reviews,
    'metacritic_score':film.metacritic_score,
    'allocine_score':film.allocine_score,
    'language':film.language.identifier,
    'countries':countries,
    'genres':genres,
    'keywords':keywords,
    'production_companies':production_companies,
    'directors':directors,
    'writers':writers,
    }
    for aw in ActorWeight.objects.filter(film=film):
        data[aw.actor.imdb_id] = aw.rank
    measurements.append(data)

#vec = DictVectorizer()

#vec.fit_transform(measurements).toarray()
