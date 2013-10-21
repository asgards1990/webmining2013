BOT_NAME = 'imdb'

SPIDER_MODULES = ['imdb.spiders']
NEWSPIDER_MODULE = 'imdb.spiders'

ITEM_PIPELINES = {
    'imdb.pipelines.DuplicatesPipeline': 1,
    #'imdb.pipelines.JsonWriterPipeline': 2,
    #'imdb.pipelines.HtmlWriterPipeline': 3,
    #'imdb.pipelines.ImgWriterPipeline': 4,
    }
