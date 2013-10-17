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

