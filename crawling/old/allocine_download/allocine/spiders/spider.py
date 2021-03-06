from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

import re

from allocine.items import FilmItem

class TestSpider(BaseSpider):
    name = 'test'
    allowed_domains = ['allocine.fr']
    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]

    def parse(self, response):
        sel = Selector(response)
        for h3 in sel.xpath('//h3').extract():
            yield MyItem(title=h3)

        for url in sel.xpath('//a/@href').extract():
            yield Request(url, callback=self.parse)


class AllocineSpider(CrawlSpider):
    name = "allocine"
    allowed_domains = ["allocine.fr"]
    start_urls = ["http://www.allocine.fr/film/tous/"]
    
    rules = (
        Rule(
            link_extractor=SgmlLinkExtractor(allow=(r"decennie-\d+/$",)),
            callback="parse_films",
            follow=True
            ),
        Rule(
            link_extractor=SgmlLinkExtractor(allow=(r"decennie-\d+/\?page=\d+",),restrict_xpaths=('//li[@class="navnextbtn"]',)),
            callback="parse_films",
            follow=True
            ),
    )

    def __init__(self):
        self.logfile = open('/home/pesto/allocine/crawled_addresses.log', 'wb')

        
    def parse_films(self, response):
        hxs = HtmlXPathSelector(response)
        results = hxs.select('//div[@class="mainzone"]')
        films = []
        for res in results:
            film = FilmItem()
            
            result = res.select('.//div[@class="titlebar"]//a')
            
            film["ident"] = re.findall(r'\d+', result.select('@href').extract()[0])[0]
            film["decennie"] = response.url.split("/")[-2]
            film["titre"] = result.select('text()').extract()[0]
            film["url"] = result.select('@href').extract()[0]

            resulti = res.select('.//div[@class="picturezone"]/a/img')
            s = resulti.select('.//@src').extract()[0]
              
            film["image_urls"] = [ s ]
            
            notes = res.select('.//div[@class="notationbar"]//img//@alt').extract()
            
            film["note_presse"] = notes[0]
            film["note_spectateur"] = notes[1]
            
            try:
                film["affiche"] = s
            except:
                film["affiche"] = ""                        
            films.append(film)
        return(films)
