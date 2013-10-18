import json

class JsonWriterPipeline(object):
    
    def __init__(self):
        self.file = open('/home/pesto/allocine/films_list.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
