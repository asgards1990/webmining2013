from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

import re

from allocine.items import FilmItem

class AllocineSpider(CrawlSpider):
    name = 'allocine.fr'
    allowed_domains = ['allocine.fr']
    start_urls = ['http://www.allocine.fr/']
     
    rules = [Rule(SgmlLinkExtractor(allow=['/film/fichefilm_gen_cfilm=\d+.html']), 'parse_film')]

    def parse_film(self, response):
        self.log('Film data sheet %s' % re.findall(r'\d+',response.url)[0])
        
        x = HtmlXPathSelector(response)
        
        film = FilmItem()
        film['url'] = response.url
        film['title'] = x.select("//div[@id='title']/span/text()").extract()[0]
        return film

