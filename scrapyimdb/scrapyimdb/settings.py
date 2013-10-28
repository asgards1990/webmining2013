# Scrapy settings for imdb project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapyimdb'

SPIDER_MODULES = ['scrapyimdb.spiders']
NEWSPIDER_MODULE = 'scrapyimdb.spiders'

ITEM_PIPELINES = {'scrapyimdb.pipelines.MyImagesPipeline' : 500, 'scrapyimdb.pipelines.PagesPipeline' : 300, 'scrapyimdb.pipelines.LinksPipeline' : 400}

IMAGES_STORE = '/home/pesto/scrapy-imdb-img/' # '/Users/benjamin/webmining2013/scrapyimdb/cache/'
IMAGES_EXPIRES = 90

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'imdb (+http://www.yourdomain.com)'

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'


DOWNLOADER_MIDDLEWARES = {
#    'imdb.middlewares.FilterDownloadedMiddleware' : 200,
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 300,
}

HTTPCACHE_ENABLED = True

HTTPCACHE_DIR = '/home/pesto/scrapy-http-cache/'

#HTTPCACHE_POLICY = 'scrapy.contrib.httpcache.RFC2616Policy'

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

LOG_LEVEL = 'INFO'