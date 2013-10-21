from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

import re

from imdb.items import FilmItem

class IMDBSpider(CrawlSpider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    start_urls = ["http://www.imdb.com/year/"]
    
    rules = (
        Rule(
            link_extractor=SgmlLinkExtractor(allow=(r"d+$",)),
            callback="parse_films",
            follow=True
            ),
        Rule(
            link_extractor=SgmlLinkExtractor(allow=(r"http://www.imdb.com/search/title?year=\d+,\d+&title_type=feature&sort=moviemeter,asc",),
                                             restrict_xpaths=('//div[@class="see-more"]',)),
            callback="parse_films",
            follow=True
            ),
        Rule(
            link_extractor=SgmlLinkExtractor(allow=(r"decennie-\d+/\?page=\d+",),restrict_xpaths=('//li[@class="navnextbtn"]',)),
            callback="parse_films",
            follow=True
            ),
    )
        
    def parse_films(self, response):
        hxs = HtmlXPathSelector(response)
        # results = hxs.select('//div[@class="mainzone"]')
        films = []
        #for res in results:
        #    film = FilmItem()
        #    
        #    result = res.select('.//div[@class="titlebar"]//a')
        #    
        #    film["ident"] = re.findall(r'\d+', result.select('@href').extract()[0])[0]
        #    film["decennie"] = response.url.split("/")[-2]
        #    film["titre"] = result.select('text()').extract()[0]
        #    film["url"] = result.select('@href').extract()[0]
        #
        #    resulti = res.select('.//div[@class="picturezone"]/a/img')
        #    s = resulti.select('.//@src').extract()[0]
        #      
        #    film["image_urls"] = [ s ]
        #    
        #    notes = res.select('.//div[@class="notationbar"]//img//@alt').extract()
        #    
        #    film["note_presse"] = notes[0]
        #    film["note_spectateur"] = notes[1]
        #    
        #    try:
        #        film["affiche"] = s
        #    except:
        #        film["affiche"] = ""                        
        #    films.append(film)
        return(films)

