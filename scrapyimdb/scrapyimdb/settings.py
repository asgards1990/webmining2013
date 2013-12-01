BOT_NAME = 'scrapyimdb'

SPIDER_MODULES = ['scrapyimdb.spiders']
NEWSPIDER_MODULE = 'scrapyimdb.spiders'

ITEM_PIPELINES = {
    'scrapyimdb.pipelines.MyImagesPipeline' : 500,
    'scrapyimdb.pipelines.PagesPipeline' : 300,
    'scrapyimdb.pipelines.LinksPipeline' : 400,
}

IMAGES_STORE = '/home/pesto/scrapy-imdb-img/'  #'/Users/benjamin/webmining2013/scrapyimdb/cache/'
IMAGES_EXPIRES = 90

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'


DOWNLOADER_MIDDLEWARES = {
    'scrapyimdb.middlewares.CacheReaderMiddleware' : 100,
}

SPIDER_MIDDLEWARES = {
    'scrapyimdb.middlewares.CacheWriterMiddleware' : 100,
}

LOG_LEVEL = 'INFO'

DOWNLOAD_DIRECTORY = '/home/pesto/imdb/' #'/Users/benjamin/imdb/'

#DEPTH_PRIORITY = 1
#SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
#SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'