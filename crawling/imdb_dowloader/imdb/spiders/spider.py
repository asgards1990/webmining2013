from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

import re

from imdb.items import FilmItem

class ImdbSpider(CrawlSpider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    start_urls = ["http://www.imdb.com/search/title?at=0&sort=moviemeter,asc&start=1&title_type=feature&year=1950,2013"]
    
    rules = (
        Rule(
            link_extractor=SgmlLinkExtractor(allow=("http://www.imdb.com/search/title?at=0&sort=moviemeter,asc&start=\d+ &title_type=feature&year=1950,2013", restrict_xpaths=('//span[@class="pagination"]',)))),
            callback="parse_films",
            follow=True
            ),
       )


def parse_films(self, response):
        hxs = HtmlXPathSelector(response)
        results = hxs.select('//tr[@class="even detailed"]')
        films = []
        for res in results:
        	film["ident"] = 0
            	film["title"] = 0
            	film["img_url"] = 0
        	print("***\n")
		print(film)
		print("***\n")

        return(films)
