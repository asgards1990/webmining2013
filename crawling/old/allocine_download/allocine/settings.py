BOT_NAME = 'allocine'

SPIDER_MODULES = ['allocine.spiders']
NEWSPIDER_MODULE = 'allocine.spiders'

ITEM_PIPELINES = {
    'allocine.pipelines.DuplicatesPipeline': 1,
    'allocine.pipelines.JsonWriterPipeline': 2,
    # 'allocine.pipelines.DbWriterPipeline' : 2,
    'allocine.pipelines.HtmlWriterPipeline': 3,
    'allocine.pipelines.ImgWriterPipeline': 4,
    # 'scrapy.contrib.pipeline.images.ImagesPipeline' : 4,
    }

# IMAGES_STORE = '/home/pesto/allocine/'
# IMAGES_EXPIRES = 90
