import json
from cinema.models import Film

class JsonWriterPipeline(object):
    
    def __init__(self):
        self.file = open('/Users/benjamin/allocine/films_list.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class DbWriterPipeline(object):

	def __init__(self):
	    pass
	
	def process_item(self, item, spider):
	    f = Film(title_original=item["titre"], imdb_id=item["ident"], release_date="2013-10-18")
	    f.save()
	    return item