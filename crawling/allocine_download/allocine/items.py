from scrapy.item import Item, Field

class FilmItem(Item):
    ident = Field()
    url = Field()
    titre = Field()
    decennie = Field()
    image_urls = Field()
    note_presse = Field()
    note_spectateur = Field()