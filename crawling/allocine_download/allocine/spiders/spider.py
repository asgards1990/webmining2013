from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

import re

from allocine.items import FilmItem

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
              
            #if s.split('/')[-1]!='empty_photo.jpg':
            film["image_urls"] = [ s ]
            
            notes = res.select('.//div[@class="notationbar"]//img//@alt').extract()
            
            film["note_presse"] = notes[0]
            film["note_spectateur"] = notes[1]
            
            #result_title = result.select('//div[@class="titlebar"]//a')
            #result_picture = result.select('//div[@class="picturezone"]//img')
            #film["ident"] = re.findall(r'\d+', result_title.select('@href').extract()[0])[0]
            #film["decennie"] = response.url.split("/")[-2]
            #film["titre"] = result_title.select('text()').extract()[0]
            #film["url"] = result_title.select('@href').extract()[0]
            try:
                #film["affiche"] = result_picture.select('@src').extract()[0]
                film["affiche"] = s
            except:
                film["affiche"] = ""                        
            films.append(film)
        return(films)
    
#    def parse_film_page(self, response):
#        hxs = HtmlXPathSelector(response)
#        items = []
#        
#        poster = ImageItem()
#        poster["image_urls"] = hxs.select('//div[contains(@class, "poster")]//img[contains(@itemprop, "image")]/@src').extract()[0]
#        items.append(poster)
#    	
#    	return(items)
