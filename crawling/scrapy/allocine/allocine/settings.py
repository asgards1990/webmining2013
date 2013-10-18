BOT_NAME = 'allocine'

SPIDER_MODULES = ['allocine.spiders']
NEWSPIDER_MODULE = 'allocine.spiders'

ITEM_PIPELINES = {
    'allocine.pipelines.JsonWriterPipeline': 1,
    }
