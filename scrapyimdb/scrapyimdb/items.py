from scrapy.item import Item, Field

class PageItem(Item):
    url = Field()
    imdb_id = Field()

class LinkItem(Item):
    attached_to = Field()

class FilmItem(PageItem):
    original_title = Field()
    english_title = Field()
    image_urls = Field()
    images = Field()
    year = Field()
    release_date = Field()
    runtime = Field()
    genres = Field()
    summary = Field()
    story_line = Field()
    writers = Field()
    countries = Field()
    budget = Field()
    boxoffice = Field()
    rating_count = Field()
    rating_value = Field()
    review_count_user = Field()
    review_count_critic = Field()
    metacritic_score = Field()
    stars = Field()
    directors = Field()
    producers = Field()
    languages = Field()

class PersonItem(PageItem):
    name = Field()
    birth_date = Field()
    birth_place = Field()
    image_urls = Field()
    images = Field()

class CompanyItem(PageItem):
    name = Field()
    country = Field()

class KeywordsItem(LinkItem):
    words = Field()

class ActorItem(LinkItem):
    imdb_id = Field()
    rank = Field()
    name = Field()

class StarItem(LinkItem):
    imdb_id = Field()
    name = Field()

class WriterItem(LinkItem):
    imdb_id = Field()
    name = Field()

class DirectorItem(LinkItem):
    imdb_id = Field()
    name = Field()

class AwardItem(LinkItem):
    win = Field()
    year = Field()
    institution = Field()
    category = Field()

class ReviewItem(LinkItem):
    grade = Field()
    summary = Field()
    journal = Field()
    reviewer = Field()
    full_review_url = Field()

class ProducerItem(LinkItem):
    imdb_id = Field()
    name = Field()

class CountryCompany(LinkItem):
    country = Field()

class CountryItem(LinkItem):
    country = Field()
    
class GrossItem(LinkItem):
    bo = Field()
