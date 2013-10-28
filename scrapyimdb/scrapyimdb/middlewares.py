from scrapy.exceptions import IgnoreRequest
from scrapy import log

from status.models import ScrapyStatus

class FilterDownloadedMiddleware(object):
    def is_downloaded(self, imdb_id):
        try:
            status = ScrapyStatus.objects.get(imdb_id = imdb_id)
            return status.downloaded
        except ScrapyStatus.DoesNotExist:
            return False
 
    def process_request(self, request, spider):
        imdb_id = None
        try:
            imdb_id = re.search('nm\d+', response.url).group(0)
            if imdb_id == None:
                imdb_id = re.search('co\d+', response.url).group(0)
            if imdb_id == None:
                imdb_id = re.search('tt\d+', response.url).group(0)
            if is_downloaded(imdb_id):
                log.msg(imdb_id + ' already downloaded.', level = log.WARNING)
                return IgnoreRequest()
            else:
                return None
        except:
            return None
