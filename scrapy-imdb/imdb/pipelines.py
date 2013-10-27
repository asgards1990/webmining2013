from cinema.models import *
from status.models import ScrapyStatus
from imdb.items import *
from scrapy.exceptions import DropItem
from scrapy import log
from scrapy.contrib.pipeline.images import ImagesPipeline

def is_extracted(imdb_id):
    try:
        return ScrapyStatus.objects.get(imdb_id  = imdb_id).extracted
    except ScrapyStatus.DoesNotExist:
        return False
    
def set_extracted(imdb_id):
    try:
        return ScrapyStatus.objects.get(imdb_id = imdb_id).extracted
    except ScrapyStatus.DoesNotExist:
        log.msg('No extracted status found for ' + imdb_id + '.')

def defineFilm(id):
    try :
        return Film.objects.get(imdb_id = id)
    except Film.DoesNotExist:
        return Film.objects.create(imdb_id = id)

def defineActorWeight(actor, film):
    try:
        return ActorWeight.objects.get(actor = actor, film = film)
    except ActorWeight.DoesNotExist:
        return ActorWeight.objects.create(actor = actor, film = film)

def defineCompany(id):
    try :
        return ProductionCompany.objects.get(imdb_id = id)
    except ProductionCompany.DoesNotExist:
        return ProductionCompany.objects.create(imdb_id = id)

def definePerson(id):
    try :
        return Person.objects.get(imdb_id = id)
    except Person.DoesNotExist:
        return Person.objects.create(imdb_id = id)

def defineInstitution(name):
    try:
        return Institution.objects.get(name = name)
    except Institution.DoesNotExist:
        return Institution.objects.create(name = name)

def defineReviewer(name):
    try:
        return Reviewer.objects.get(name = name)
    except Reviewer.DoesNotExist:
        return Reviewer.objects.create(name = name)

def defineJournal(name):
    try:
        return Journal.objects.get(name = name)
    except Journal.DoesNotExist:
        return Journal.objects.create(name = name)

def defineGenre(name):
    try:
        return Genre.objects.get(name = name)
    except Genre.DoesNotExist:
        log.msg('Unlisted genre : ' + name + '.')
        #WARNING
        return Genre.objects.create(name = name)

def defineLanguage(identifier):
    try:
        return Language.objects.get(identifier = identifier)
    except Language.DoesNotExist:
        log.msg('Unlisted language with identifier ' + identifier + '.')
        return None

def defineKeyword(word):
    try:
        return Keyword.objects.get(word = word)
    except Keyword.DoesNotExist:
        return Keyword.objects.create(word = word)

class MyImagesPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            return item
            #raise DropItem("Item contains no images")
        if isinstance(item, FilmItem):
            film = defineFilm(item['imdb_id'])
            film.image_url = image_paths[0]
            film.save()
        if isinstance(item, PersonItem):
            person = definePerson(item['imdb_id'])
            person.image_url = image_paths[0]
            person.save()
        return item

class PagesPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PageItem):
            if is_extracted(item['imdb_id']):
                raise DropItem(item['imdb_id'] + ' already extracted.')
            else:
                if isinstance(item, FilmItem):
                    film = defineFilm(item['imdb_id'])
                    film.english_title = item['english_title']
                    film.original_title = item['original_title']
                    if item.has_key('year'):
                        film.year = item['year']
                    if item.has_key('release_date'):
                        film.release_date = item['release_date']
                    if item.has_key('runtime'):
                        film.runtime = item['runtime']
                    for genre in item['genres']:
                        film.genres.add(defineGenre(genre))
                    film.imdb_summary = item['summary']
                    film.imdb_storyline = item['story_line']
                    if item.has_key('budget'):
                        film.budget = item['budget']
                    if item.has_key('boxoffice'):
                        film.box_office = item['boxoffice']
                    if item.has_key('rating_count'):
                        film.imdb_nb_user_ratings = item['rating_count']
                    if item.has_key('rating_value'):
                        film.imdb_user_rating = item['rating_value']
                    if item.has_key('review_count_user'):
                        film.imdb_nb_user_reviews = item['review_count_user']
                    if item.has_key('review_count_critic'):
                        film.imdb_nb_reviews = item['review_count_critic']
                    if item.has_key('metacritic_score'):
                        film.metacritic_score = item['metacritic_score']
                    if item['languages'] != []:
                        film.language = defineLanguage(item['languages'][0])
                    film.save()
                elif isinstance(item, PersonItem):
                    person = definePerson(item['imdb_id'])
                    if item.has_key('name'):
                        person.name = item['name']
                    if item.has_key('birth_date'):
                        person.birth_date = item['birth_date']
                    if item.has_key('birth_place'):
                        pass #person.birth_place = item['birth_place']
                    person.save()
                elif isinstance(item, CompanyItem):
                    comp = defineCompany(item['imdb_id'])
                    if item.has_key('name'):
                        comp.name = item['name']
                    comp.save()
                set_extracted(item['imdb_id'])
                return item
        else:
            return item

class LinksPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, LinkItem):
            if isinstance(item, CountryCompany):
                try:
                    country = Country.objects.get(identifier = item['country'])
                    comp = defineCompany(item['attached_to'])
                    comp.country = country
                except Country.DoesNotExist:
                    log.msg('Country ' + item['language']  + 'not found.')
                return item
            film = defineFilm(item['attached_to'])
            if isinstance(item, KeywordsItem):
                for word in item['words']:
                    film.keywords.add(defineKeyword(word))
                film.save()
            elif isinstance(item, WriterItem):
                writer = definePerson(item['imdb_id'])
                writer.name = item['name']
                film.writers.add(writer)
                writer.save()
            elif isinstance(item, ActorItem):
                actor = definePerson(item['imdb_id'])
                actor.name = item['name']
                actor.save()
                actor_weight = defineActorWeight(actor, film)
                actor_weight.rank = item['rank']
                actor_weight.save()
            elif isinstance(item, StarItem):
                actor = definePerson(item['imdb_id'])
                actor.name = item['name']
                actor.save()
                actor_weight = defineActorWeight(actor, film)
                actor_weight.star = True
                actor_weight.save()
            elif isinstance(item, DirectorItem):
                director = definePerson(item['imdb_id'])
                director.name = item['name']
                director.save()
                film.directors.add(director)
                film.save()
            elif isinstance(item, AwardItem):
                prize = Prize()
                prize.film = film
                prize.year = item['year']
                prize.institution = defineInstitution(item['institution'])
                prize.win = item['win']
                prize.save()
                #TODO prize.category =
            elif isinstance(item, ReviewItem):
                review = Review()
                review.film = film
                if item.has_key('reviewer'):
                    reviewer = defineReviewer(item['reviewer'])
                    review.reviewer = reviewer
                review.grade = float(item['grade'])
                journal = defineJournal(item['journal'])
                review.journal = journal
                if item.has_key('full_review_url'):
                    review.full_review_url = item['full_review_url']
                review.summary = item['summary']
                film.reviews
                review.save()
            elif isinstance(item, ProducerItem):
                comp = defineCompany(item['imdb_id'])
                comp.name = item['name']
                film.production_companies.add(comp)
                comp.save()
        return item
