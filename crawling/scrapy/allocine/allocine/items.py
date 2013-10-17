# The models for your scraped items from Allocine

from scrapy.item import Item, Field

class FilmItem(Item):
    url = Field()
    title = Field()

