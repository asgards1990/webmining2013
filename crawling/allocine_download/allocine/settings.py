BOT_NAME = 'allocine'

SPIDER_MODULES = ['allocine.spiders']
NEWSPIDER_MODULE = 'allocine.spiders'

ITEM_PIPELINES = {
    'allocine.pipelines.JsonWriterPipeline': 1,
    'allocine.pipelines.HtmlWriterPipeline': 2,
    'allocine.pipelines.ImgWriterPipeline': 3,
    }
