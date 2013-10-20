BOT_NAME = 'allocine'

SPIDER_MODULES = ['allocine.spiders']
NEWSPIDER_MODULE = 'allocine.spiders'

ITEM_PIPELINES = {
    'allocine.pipelines.JsonWriterPipeline': 1,
    'scrapy.contrib.pipeline.images.ImagesPipeline' : 1,
    'allocine.pipelines.DbWriterPipeline' : 1,
    }

IMAGES_STORE = '/Users/benjamin/allocine/'
IMAGES_EXPIRES = 90