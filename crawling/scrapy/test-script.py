from scrapy.item import Item, Field

class FilmItem(Item):
	url = Field()
	title = Field()

# Allocine's films URLs are like
# http://www.allocine.fr/film/fichefilm_gen_cfilm=NUMBER.html
# where NUMBER is an integer

# An XPATH expression to select the title could be:
# //div[@id='title']

# We start at:
# http://www.allocine.fr/film/tous/decennie-1990/?year=1997

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

class AllocineSpider(CrawlSpider):

    name = 'allocine.fr'
    allowed_domains = ['allocine.fr']
    start_urls = ['http://www.allocine.fr/film/tous/decennie-1990/?year=1997']
    rules = [Rule(SgmlLinkExtractor(allow=['/film/fichefilm_gen_cfilm=\d+.html']), 'parse_film')]

    def parse_film(self, response):
	self.log('Film data sheet %s' % response.url)        

	x = HtmlXPathSelector(response)

        film = FilmItem()
        film['url'] = response.url
        film['title'] = x.select("//div[@id='title']").extract()
        return film

