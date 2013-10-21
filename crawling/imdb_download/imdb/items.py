from scrapy.item import Item, Field

class FilmItem(Item):
    ident = Field()
    url = Field()
    title = Field()
    img_url = Field()
