from scrapy import log
from scrapy.exceptions import NotConfigured
import os

class CacheReaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        dir = crawler.settings.get('DOWNLOAD_DIRECTORY', None)
        if not dir:
            raise NotConfigured
        return cls(dir)
    
    def __init__(self, dir):
        self.dir = dir
    
    def process_request(self, request, spider):
        if request.meta.has_key('download'):
            if os.path.isfile(self.dir + request.meta['download']):
                target = request.meta.pop('download')
                request = request.replace(url = 'file://localhost' + self.dir + target)
                log.msg('Opening ' + request.url, level = log.INFO)
                return request

class CacheWriterMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        dir = crawler.settings.get('DOWNLOAD_DIRECTORY', None)
        if not dir:
            raise NotConfigured
        return cls(dir)
    
    def __init__(self, dir):
        self.dir = dir
    
    def process_spider_input(self, response, spider):
        if response.status in [200] and response.meta.has_key('download'):
            if not os.path.isfile(self.dir + response.meta['download']):
                try:
                    f = open(self.dir + response.meta['download'], "wb")
                    f.write(response.body)
                    f.close()
                    log.msg('Saving ' + response.meta['download'], level = log.INFO)
                except IOError:
                    log.msg('Unable to write down ' + response.meta['download'], level = log.ERROR)