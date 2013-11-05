from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log

from scrapyimdb.items import *

import re
import dateutil.parser

from status.models import ScrapyStatus

class IMDbSpider(CrawlSpider):
    name = 'imdb.com'
    allowed_domains = ['imdb.com']
    tags = 'feature' # 'feature,documentary'
    sort = 'moviemeter,asc' #'release_date_us,asc'
    
    rules = (
        Rule(
            link_extractor=SgmlLinkExtractor(
                allow=(r"search/title\?at=\d+&count=\d+&release_date=\d+,\d+&sort="+sort+"&start=\d+&title_type="+tags+"&view=simple",),
                restrict_xpaths=('//div[@id="right"]')
            ),
            process_links='stop_max',
            follow=True
        ),
        Rule(
            link_extractor=SgmlLinkExtractor(
                allow=(r"title/tt\d+",),
                restrict_xpaths=('//td[@class="title"]',)
            ),
            process_links = 'stop_parsed',
            callback='parse_film'
        ),
    )

    ext_title = re.compile("tt\d+")
    ext_person = re.compile("nm\d+")
    ext_company = re.compile("co\d+") 
    extract_person = lambda self, s : self.ext_person.search(s).group(0)
    extract_company = lambda self, s : self.ext_company.search(s).group(0)
    ext_language = re.compile("language/\w+\?")
    extract_language = lambda self, s : self.ext_language.search(s).group(0).split('/')[1][:-1]
    ext_budget_dollar = re.compile("\$[\d|,]+")
    ext_budget_euro = re.compile(u'\u20ac[\d|,]+')
    extract_budget_dollar = lambda self, s : self.ext_budget_dollar.search(s).group(0)[1:].replace(',', '')
    extract_budget_euro = lambda self, s : self.ext_budget_euro.search(s).group(0)[1:].replace(',', '')
    ext_country = re.compile("country/\w+\?")
    extract_country = lambda self, s : self.ext_country.search(s).group(0).split('/')[1][:-1]

    def __init__(self, year = 1950, actors_max_rank = 100, fetch_person = False, fetch_company = False, max_position = 10000, *args, **kwargs):
        super(IMDbSpider, self).__init__(*args, **kwargs)
        self.year = year
        self.actors_max_rank = actors_max_rank
        self.fetch_person = fetch_person
        self.fetch_company = fetch_company
        self.max_position = max_position
        # http://www.imdb.com/search/title?at=0&count=250&release_date=2000,2000&sort=release_date_us,asc&start=251&title_type=feature&view=simple
        self.start_urls = ["http://www.imdb.com/search/title?at=0&count=250&release_date={0},{0}&sort={1}&start=1&title_type={2}&view=simple".format(self.year, self.sort, self.tags)]

    def stop_max(self, links):
        if links == []:
            return []
        link = links[0]
        if int(re.search('start=\d+', link.url).group(0).split('=')[1]) > int(self.max_position):
            self.log('Stopping URLs above ' + self.max_position + '.', level=log.WARNING)
            return []
        return links

    def stop_parsed(self, links):
        approved = []
        for link in links:
            if not self.is_parsed(self.ext_title.search(link.url).group(0)):
                approved.append(link)
        return approved
    
    def is_parsed(self, imdb_id):
        try:
            status = ScrapyStatus.objects.get(imdb_id = imdb_id)
            return status.parsed
        except ScrapyStatus.DoesNotExist:
            return False

    def set_parsed(self, imdb_id, year = None):
        status = ScrapyStatus()
        status.imdb_id = imdb_id
        status.parsed = True
        status.extracted = False
        status.downloaded = True
        try:
            status.year = int(year)
        except:
            pass
        status.save()

    def parse_film(self, response):
        hxs = HtmlXPathSelector(response)

        film = FilmItem()
        film['url'] = response.url
        if response.meta.has_key('id'):
            imdb_id = response.meta['id']
        else:
            imdb_id = self.ext_title.search(response.url).group(0)

        film['imdb_id'] = imdb_id
        
        try:
            film['english_title'] = hxs.select('//td[@id="overview-top"]/h1[@class="header"]/span[@class="itemprop" and @itemprop="name"]/text()').extract()[0]
        except:
            self.log('No english title for ' + film['imdb_id'] + ' : film is not parsed.')
            return []

        film['original_title'] = ''
        try:
            film['original_title'] = re.search('".+"', hxs.select('//td[@id="overview-top"]/h1[@class="header"]/span[@class="title-extra" and @itemprop="name"]/text()').extract()[0]).group(0)
        except IndexError:
            self.log("No original title for " + film['imdb_id'] + ".")

        film['image_urls'] = []
        try:
            film['image_urls'] = [ hxs.select('//td[@id="img_primary"]/*/a/img/@src').extract()[0] ]
        except IndexError:
            self.log("No image for " + film['imdb_id'] + ".")

        try:
            year_string = hxs.select('//td[@id="overview-top"]/h1[@class="header"]/span[@class="nobr"]/a/text()').extract()[0]
            film['year'] = int(year_string)
        except IndexError, ValueError:
            self.log("No year found for " + film['imdb_id'] + '.')

        try:
            release_date_string = hxs.select('//td[@id="overview-top"]/div[@class="infobar"]/span[@class="nobr"]/a/meta[@itemprop="datePublished"]/@content').extract()[0]
            film['release_date'] = dateutil.parser.parse(release_date_string).date()
        except IndexError, ValueError:
            self.log('No release data found for ' + film['imdb_id'] )

        try:
            duration_string = hxs.select('//td[@id="overview-top"]/div[@class="infobar"]/time[@itemprop="duration"]/text()').extract()[0]
            film['runtime'] = int(re.search('\d+', duration_string).group(0))
        except IndexError, ValueError:
            self.log('No runtime found for ' + film['imdb_id'] + '.')

        film['genres'] = hxs.select('//td[@id="overview-top"]/div[@class="infobar"]/a/span[@itemprop="genre"]/text()').extract()

        film['summary'] = ''
        try:
            film['summary'] = hxs.select('//td[@id="overview-top"]/p[@itemprop="description"]/text()').extract()[0][1:]
        except IndexError:
            self.log('No summary found for ' + film['imdb_id'] + '.')

        film['story_line'] = ''
        try:
            film['story_line'] = hxs.select('//div[@class="inline canwrap" and @itemprop="description"]/p/text()').extract()[0][1:]
        except IndexError:
            self.log('No story line found for ' + film['imdb_id'] + '.')

        film['writers'] = []
        writers_names = []
        try:
            list_url_writers = hxs.select('//td[@id="overview-top"]/div[@itemprop="creator"]/a[starts-with(@href, "/name")]/@href').extract()
            film['writers'] = map(self.extract_person, list_url_writers)
            writers_names = hxs.select('//td[@id="overview-top"]/div[@itemprop="creator"]/a[starts-with(@href, "/name")]/span/text()').extract()
        except:
            self.log('Cannot extract writers for ' + film['imdb_id'] + '.')

        film['countries'] = []
        try:
            parse_country = hxs.select('//div[@id="titleDetails"]/div/a[contains(@href,"country")]/@href').extract()
            film['countries'] = map(self.extract_country, parse_country)
        except:
            self.log('Unable to extract countries for ' + film['imdb_id'] + '.')

        try:
            budget_string = ''.join(hxs.select('//h4[contains(text(),"Budget")]/parent::*/text()').extract())
            film['budget'] = int(self.extract_budget(budget_string))
        except:
            self.log('No budget found for ' + film['imdb_id'] + '.')

        try:
            film['boxoffice'] = int(self.extract_budget_dollar( ''.join(hxs.select('//h4[contains(text(),"Gross")]/parent::*/text()').extract()) ) )
        except:
            self.log('No box office found for ' + film['imdb_id'] + '.')

        try:
            film['rating_count'] = int(hxs.select('//span[@itemprop="ratingCount"]//text()').extract()[0].replace(',',''))
        except:
            self.log('No rating count for ' + film['imdb_id'] + '.')

        try:
            film['rating_value'] = float(hxs.select('//span[@itemprop="ratingValue"]//text()').extract()[0])
        except:
            self.log('No rating value for ' + film['imdb_id'] + '.')

        review_count = hxs.select('//span[@itemprop="reviewCount"]//text()').extract()
        try:
            film['review_count_user'] = int(re.search('\d+', review_count[0]).group(0))
        except:
            self.log('No users\' review count found for ' + film['imdb_id'])

        try:
            film['review_count_critic'] = int(re.search('\d+', review_count[1]).group(0))
        except:
            self.log('No users\' review count found for ' + film['imdb_id'])

        try:
            metacritic_score_string = hxs.select('//a[starts-with(@href,criticreviews) and contains(@title, "Metacritic.com")]//text()').extract()[0].split('/')[0]
            film['metacritic_score'] = int(re.search('\d+', metacritic_score_string).group(0))
        except IndexError, ValueError:
            self.log('No metacritic score for ' + film['imdb_id'] + '.')

        film['stars'] = []
        stars_names = []
        try:
            parse_stars = hxs.select('//a[contains(@href,"tt_ov_st") and starts-with(@href, "/name")]/@href').extract()
            film['stars'] = map(self.extract_person , parse_stars)
            stars_names = hxs.select('//a[contains(@href,"tt_ov_st") and starts-with(@href, "/name")]/span/text()').extract()
        except:
            self.log('No stars found for ' + film['imdb_id'] + '.')

        film['directors'] = []
        directors_names = []
        try:
            parse_dir = hxs.select('//td[@id="overview-top"]/div[@itemprop="director"]/a/@href').extract()
            film['directors'] = map(self.extract_person, parse_dir)
            directors_names = hxs.select('//td[@id="overview-top"]/div[@itemprop="director"]/a/span/text()').extract()
        except:
            self.log('No director found for ' + film['imdb_id'] + '.')

        film['producers'] = []
        try:
            parse_comp = hxs.select('//span[contains(@itemtype,"Organization") and @itemprop="creator"]/a/@href').extract()
            film['producers'] = map(self.extract_company, parse_comp)
        except:
            self.log('No producer found for ' + film['imdb_id'] + '.')

        film['languages'] = []
        try:
            parse_lang = hxs.select('//a[contains(@href,"language")]/@href').extract()
            film['languages'] = map(self.extract_language, parse_lang)
        except:
            self.log('Unable to extract languages for ' + film['imdb_id'] + '.')

        list_items = [film,
                      Request(url = 'http://www.imdb.com/title/' + film['imdb_id'] + '/criticreviews', callback = self.parse_film_reviews, meta={'id' : film['imdb_id']}),
                     Request(url = 'http://www.imdb.com/title/' + film['imdb_id'] + '/awards', callback = self.parse_film_awards, meta={'id' : film['imdb_id']}),
                     Request(url = 'http://www.imdb.com/title/' + film['imdb_id'] + '/keywords', callback = self.parse_film_keywords, meta={'id' : film['imdb_id']}),
                     Request(url = 'http://www.imdb.com/title/' + film['imdb_id'] + '/companycredits', callback = self.parse_company_credits, meta={'id' : film['imdb_id']}),
                     Request(url = 'http://www.imdb.com/title/' + film['imdb_id'] + '/fullcredits', callback = self.parse_film_credits, meta={'id' : film['imdb_id']})]

        k=0
        for star in film['stars']:
            item = StarItem()
            item['attached_to'] = film['imdb_id']
            item['imdb_id'] = star
            item['name'] = stars_names[k]
            k += 1
            list_items.append(item)
    
        k=0
        for writer in film['writers']:
            item = WriterItem()
            item['attached_to'] = film['imdb_id']
            item['imdb_id'] = writer
            item['name'] = writers_names[k]
            k += 1
            list_items.append(item)
    
        k=0
        for director in film['directors']:
            item = DirectorItem()
            item['attached_to'] = film['imdb_id']
            item['imdb_id'] = director
            item['name'] = directors_names[k]
            k += 1
            list_items.append(item)

        for country in film['countries']:
            item = CountryItem()
            item['attached_to'] = film['imdb_id']
            item['country'] = country
            list_items.append(item)
        
        self.set_parsed(film['imdb_id'], year = self.year)
        return list_items

    def parse_film_keywords(self, response):
        hxs = HtmlXPathSelector(response)
        if response.meta.has_key('id'):
            imdb_id = response.meta['id']
        else:
            imdb_id = self.ext_title.search(response.url).group(0)
        words = hxs.select('//td/a[starts-with(@href,"/keyword")]/text()').extract()
        item = KeywordsItem()
        item['words'] = words
        item['attached_to'] = imdb_id
        return [item]

    def parse_film_awards(self, response):
        hxs = HtmlXPathSelector(response)
        list_item = []
        if response.meta.has_key('id'):
            imdb_id = response.meta['id']
        else:
            imdb_id = self.ext_title.search(response.url).group(0)
        list_institutions = map(lambda e : e.select('string()').extract() , hxs.select('//div[@id="main"]/div/div[@class="article listo"]/h3'))
        list_award_cats = hxs.select('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="title_award_outcome"]/span[@class="award_category"]/text()').extract()
        list_award_status = hxs.select('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]/tr/td[@class="title_award_outcome"]/b/text()').extract()
        list_award_year = map(lambda s : re.search('\d+', s).group(0) , hxs.select('//a[@class="event_year"]/text()').extract() )
        
        index = 0
        for i in range(len(list_institutions)):
            span = len(hxs.select('//div[@id="main"]/div/div[@class="article listo"]/table[@class="awards"]['+str(i+1)+']/tr/td[@class="title_award_outcome"]/@rowspan').extract())
            for _ in range(span):
                item = AwardItem()
                item['attached_to'] = imdb_id
                item['win'] = (list_award_status[index].lower().find('won') > -1)
                item['category'] = list_award_cats[index]
                try:
                    item['year'] = int(list_award_year[i])
                except ValueError:
                    self.log('Unable to extract year.')
                try:
                    item['institution'] = re.search('\w[\w| ]+', list_institutions[i][0]).group(0)
                except:
                    self.log('Unable to extract institution.')
                list_item.append(item)
                index += 1
        
        return list_item

    def parse_film_credits(self, response):
        hxs = HtmlXPathSelector(response)
        list_item = []
        if response.meta.has_key('id'):
            imdb_id = response.meta['id']
        else:
            imdb_id = self.ext_title.search(response.url).group(0)
        list_actor_urls = hxs.select('//td[@itemprop="actor"]/a/@href').extract()
        list_actor_names = hxs.select('//td[@itemprop="actor"]/a/span/text()').extract()
        list_actor = map(self.extract_person, list_actor_urls)
        for k in range(min(len(list_actor), self.actors_max_rank )):
            item = ActorItem()
            item['attached_to'] = imdb_id
            item['rank'] = k+1
            item['imdb_id'] = list_actor[k]
            item['name'] = list_actor_names[k]
            list_item.append(item)
            if self.fetch_person and not self.is_parsed(list_actor[k]):
                list_item.append(Request(url = 'http://www.imdb.com/name/' + list_actor[k], callback=self.parse_person, meta={'id' : list_actor[k]} ))

        list_writer_urls = hxs.select('//a[contains(@href,"ttfc_fc_dr")]/@href').extract()
        list_writer_names = hxs.select('//a[contains(@href,"ttfc_fc_dr")]/text()').extract()
        list_writers = map(self.extract_person, list_writer_urls)
        k = 0
        for writer in list_writers:
            item = WriterItem()
            item['attached_to'] = imdb_id
            item['imdb_id'] = writer
            item['name'] = list_writer_names[k]
            k += 1
            list_item.append(item)
            if self.fetch_person and not self.is_parsed(writer) and not writer in list_actor:
                list_item.append(Request(url = 'http://www.imdb.com/name/' + writer, callback=self.parse_person, meta={'id' : writer} ))

        list_dir_urls = hxs.select('//a[contains(@href,"ttfc_fc_dr")]/@href').extract()
        list_dir_names = hxs.select('//a[contains(@href,"ttfc_fc_dr")]/text()').extract()
        list_directors = map(self.extract_person, list_dir_urls)
        k = 0
        for director in list_directors:
            item = WriterItem()
            item['attached_to'] = imdb_id
            item['imdb_id'] = director
            item['name'] = list_dir_names[k]
            k += 1
            list_item.append(item)
            if self.fetch_person and not self.is_parsed(director) and not director in list_actor and not director in list_writers:
                list_item.append(Request(url = 'http://www.imdb.com/name/' + director, callback=self.parse_person, meta={'id' : director} ))

        return list_item
            
    def parse_film_reviews(self, response):
        hxs = HtmlXPathSelector(response)
        if response.meta.has_key('id'):
            imdb_id = response.meta['id']
        else:
            imdb_id = self.ext_title.search(response.url).group(0)
        list_item  = []
        
        review_frames = hxs.select('//tr[@itemprop="reviews"]')
        
        for review_frame in review_frames:
            item = ReviewItem()
            item['attached_to'] = imdb_id
            try:
                item['grade'] = int(review_frame.select('.//span[@itemprop="ratingValue"]/text()').extract()[0])
            except ValueError:
                self.log('Unable to extact grade.')
            try:
                item['summary'] = review_frame.select('.//div[@class="summary"]/text()').extract()[0]
            except IndexError:
                self.log('Unable to extract summary')
            try:
                item['reviewer'] = review_frame.select('.//span[@itemprop="author"]/span/text()').extract()[0]
            except:
                self.log('No reviewer found for this review.')
            try:
                item['journal'] = review_frame.select('.//b[@itemprop="publisher"]/span/text()').extract()[0]
            except IndexError:
                self.log('Unable to extract journal for this review.')

            try:
                item['full_review_url'] = review_frame.select('.//span[@itemprop="author"]/../@href').extract()[0]
            except IndexError:
                self.log('Unable to extract full review url.')
            list_item.append(item)
        
        return list_item

    def parse_person(self, response):
        hxs = HtmlXPathSelector(response)
        
        person = PersonItem()
        person['url'] = response.url
        
        if response.meta.has_key('id'):
            imdb_id = response.meta['id']
        else:
            imdb_id = self.ext_person.search(response.url).group(0)
        
        person['imdb_id'] = imdb_id
        
        if self.is_parsed(person['imdb_id']):
            return []
        
        try:
            person['name'] = hxs.select('//h1/span[@itemprop="name"]/text()').extract()[0]
        except IndexError:
            self.log('No name found for ' + person['imdb_id'] + '.')
        
        try:
            birth_date_string = hxs.select('//time[@itemprop="birthDate"]/@datetime').extract()[0]
            person['birth_date'] = dateutil.parser.parse(birth_date_string).date()
        except:
            self.log('No birth date found for ' + person['imdb_id'] + '.')
        
        try:
            person['birth_place'] = hxs.select('//a[contains(@href,"?birth_place=")]/text()').extract()[0]
        except IndexError:
            self.log('No birth place found for ' + person['imdb_id'] + '.')

        person['image_urls'] = []
        try:
            person['image_urls'] = [hxs.select('//div[@class="image"]/a/img/@src').extract()[0] ]
        except IndexError:
            self.log('No image found for ' + person['imdb_id'] + '.')
        
        self.set_parsed(person['imdb_id'])
        return [person]

    def parse_company_credits(self, response):
        hxs = HtmlXPathSelector(response)
        if response.meta.has_key('id'):
            imdb_id = response.meta['id']
        else:
            imdb_id = self.ext_title.search(response.url).group(0)
        list_co_ids = map(self.extract_company, hxs.select('//ul[1]//a[starts-with(@href,"/company")]/@href').extract())
        list_co_names = hxs.select('//ul[1]//a[starts-with(@href,"/company")]/text()').extract()
        list_items = []
        for k in range(len(list_co_ids)):
            link = ProducerItem()
            link['attached_to'] = imdb_id
            link['imdb_id'] = list_co_ids[k]
            link['name'] = list_co_names[k]
            list_items.append(link)
            if self.fetch_company and not self.is_parsed(link['imdb_id']):
                list_items.append(Request(url = 'http://www.imdb.com/company/'+link['imdb_id'], callback = self.parse_company, meta = {'id' : link['imdb_id']}))
        return list_items

    def parse_company(self, response):
        co_co = CountryCompany()
        if response.meta.has_key('id'):
            co_co['attached_to'] = response.meta['id']
        else:
            co_co['attached_to'] = self.extract_company(response.url)
        if self.is_parsed(co_co['attached_to']):
            return []
        hxs =  HtmlXPathSelector(response)
        try:
            co_co['country'] = hxs.select('//strong[@class="title"]/text()').extract()[0].split('[')[1][:-1]
            return[co_co]
        except Exception as e:
            self.log('No language found for ' + co_co['attached_to'] + '.')
            self.log('Error {}'.format(e))
            return []
