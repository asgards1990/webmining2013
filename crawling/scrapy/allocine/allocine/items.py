# The models for your scraped items from Allocine

from scrapy.item import Item, Field

class FilmItem(Item):
    ident = Field()
    url = Field()
    titre = Field()
    decennie = Field()
