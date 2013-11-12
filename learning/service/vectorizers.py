import numpy as np
from cinema.models import *
import datetime

#TODO : uniformize generator functions' names

def getSeason(date):
    if not date:
        return False
    if date.month in [12, 1, 2]:
        return 'winter'
    if date.month in [3, 4, 5]:
        return 'spring'
    if date.month in [6, 7, 8]:
        return 'summer'
    if date.month in [9, 10, 11]:
        return 'fall'

def genNullableFeature(iter_films,feature_name):
    while True:
        film = next(iter_films)
	yield {feature_name:getattr(film,feature_name)}

def genRuntime(iter_films):
    return genNullableFeature(iter_films,'runtime')

def genBudget(iter_films):
    return genNullableFeature(iter_films,'budget')

def genMetacriticScore(iter_films):
    return genNullableFeature(iter_films,'metacritic_score')

def genBoxOffice(iter_films):
    return genNullableFeature(iter_films,'box_office')

def genImdbUserRating(iter_films):
    return genNullableFeature(iter_films,'imdb_user_rating')

def genImdbNbUserRatings(iter_films):
    return genNullableFeature(iter_films,'imdb_nb_user_ratings')

def genImdbNbUserReviews(iter_films):
    return genNullableFeature(iter_films,'imdb_nb_user_reviews')

def genImdbNbReviews(iter_films):
    return genNullableFeature(iter_films,'imdb_nb_reviews')

def genReleaseDate(iter_films):
    while True:
        film = next(iter_films)
	yield {'year':film.release_date.year,
            'month':film.release_date.month,
            'day':film.release_date.day}

def genLanguages(iter_films):
    while True:
        film = next(iter_films)
        if film.language:
            yield {'language' : film.language.identifier}
        else:
            yield {'language' : '_nothing'}

def genSeason(iter_films):
    while True:
        film = next(iter_films)
        season = getSeason(film.release_date)
        if season:
	        yield {getSeason(film.release_date) : 1}
        else:
            yield {'winter' : 0.25, 'fall': 0.25, 'summer' : 0.25, 'spring' : 0.25}

def genFeature(iter_films, feature_name, feature_content_name):
    while True:
        film = next(iter_films)
        attr = getattr(film, feature_name)
        if attr.count() == 0:
            yield {'_nothing' : 1}
        else:
            d = {}
            for item in attr.all():
                content = getattr(item, feature_content_name)
                d[content] = 1
            yield d

def genKeywords(iter_films):
    return genFeature(iter_films,'keywords', 'word')

def genGenres(iter_films):
    return genFeature(iter_films,'genres', 'name')

def genCountries(iter_films):
    return genFeature(iter_films,'country', 'identifier')

def genDirectors(iter_films):
    return genFeature(iter_films,'directors', 'imdb_id')

def genWriters(iter_films):
    return genFeature(iter_films,'writers', 'imdb_id')

def genProductionCompanies(iter_films):
    return genFeature(iter_films,'production_companies', 'imdb_id')

def hashIndexes(iter_films):
    d1, d2, d3 = {}, {}, {}
    k = 0
    for film in iter_films:
        d1[film.pk] = k
        d2[k] = film.pk
        d3[k] = film.english_title
        k += 1
    return d1, d2, d3

def genPrizes(iter_films):
    while True:
        film = next(iter_films)
        prizes = Prize.objects.filter(film=film)
        if prizes.count() == 0:
            yield {'_nothing' : 1}
        else:
            d = {}
            for prize in prizes.all():
                #d[prize.institution.name+'_'+str(prize.win)] = 1
                d[prize.institution.name+'_False'] = 1
                d[prize.institution.name+'_True'] = 1 if prize.win else 0
            yield d

def genReviews(iter_films):
    while True:
        film = next(iter_films)
        reviews = Review.objects.filter(film=film).exclude(grade=None)
        if reviews.count() == 0:
            yield {'_nothing' : 1}
        else:
            d = {}
            for review in reviews.all():
                d[review.journal.name] = 1+review.grade
            yield d

def genReviewsContent(iter_films):
    while True:
        film = next(iter_films)
        reviews = Review.objects.filter(film=film).exclude(grade=None)
        d = {}
        for review in reviews.all():
            d[review.journal.name] = review.summary
        yield d

def genReviewsContent2(iter_films):
    while True:
        film = next(iter_films)
        reviews = Review.objects.filter(film=film).exclude(grade=None)
        s = ""
        for review in reviews.all():
            s = s+" "+review.summary
        yield s

def genActors(iter_films):
    while True:
        film = next(iter_films)
        aws = ActorWeight.objects.filter(film=film)
        if aws.count() == 0:
            yield {'_nothing' : 1}
        else:
            d = {}
            for aw in aws.all():
                d[aw.actor.imdb_id] = 1
            yield d

def genRanks(iter_films):
    while True:
        film = next(iter_films)
        aws = ActorWeight.objects.filter(film=film)
        if aws.count() == 0:
            yield {'_nothing' : 1}
        else:
            d = {}
            for aw in aws.all():
                if aw.rank == None: # in Benjamin's database, stars have a None rank
                    d[aw.actor.imdb_id] = 1
                else:
                    d[aw.actor.imdb_id] = aw.rank
            yield d

def genStars(iter_films):
    while True:
        film = next(iter_films)
        aws = ActorWeight.objects.filter(film=film)
        if aws.count() == 0:
            yield {'_nothing' : 1}
        else:
            d = {}
            for aw in aws.all():
                d[aw.actor.imdb_id] = aw.star
            yield d


