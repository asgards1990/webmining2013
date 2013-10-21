import os
import json
import urllib
from scrapy import signals
from scrapy.exceptions import DropItem

# from cinema.models import Film

class DuplicatesPipeline(object):

    def __init__(self):
        self.logfile = open('/home/pesto/allocine/duplicates.log', 'wb')

    def process_item(self, item, spider):
        if os.path.exists('/home/pesto/allocine/html/' + item["ident"] + '.html'):
            self.logfile.write(item["ident"] + ' has already been processed' + "\n")
            raise DropItem("Duplicate item found: %s" % item)
        else:
            return item

class JsonWriterPipeline(object):
    
    def __init__(self):
        self.file = open('/home/pesto/allocine/films_list.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

# class DbWriterPipeline(object):
#
#   def __init__(self):
#	    pass
#	
#	def process_item(self, item, spider):
#	    f = Film(title_original=item["titre"], imdb_id=item["ident"], release_date="2013-10-18")
#	    f.save()
#	    return item

class HtmlWriterPipeline(object):
    
    def __init__(self):
        self.logfile = open('/home/pesto/allocine/html.log', 'wb')

    def process_item(self, item, spider):
        
        # Enregistrement de la fiche principale du film
        try:
            u = urllib.urlopen('http://www.allocine.fr' + item["url"])
        except HTTPError as e:
            self.logfile.write('ERROR: http://www.allocine.fr' + item["url"] + "\n")
            self.logfile.write('The server couldn\'t fulfill the request.' + "\n")
            self.logfile.write('Error code: ' + e.code + "\n")
        except URLError as e:
            self.logfile.write('ERROR: http://www.allocine.fr' + item["url"] + "\n")
            self.logfile.write('We failed to reach a server.' + "\n")
            self.logfile.write('Reason: ' + e.reason + "\n")
        else:
            f = open('/home/pesto/allocine/html/' + item["ident"] + '.html', 'wb')
            f.write(u.read())
            f.close()
            u.close()
            self.logfile.write('http://www.allocine.fr' + item["url"] + ' downloaded' + "\n")
        
        # Enregistrement des critiques du film
        try:
            u = urllib.urlopen('http://www.allocine.fr/film/fichefilm-' + item["ident"] + '/critiques/presse/')
        except HTTPError as e:
            self.logfile.write('ERROR: http://www.allocine.fr/film/fichefilm-' + item["ident"] + '/critiques/presse/' + "\n")
            self.logfile.write('The server couldn\'t fulfill the request.' + "\n")
            self.logfile.write('Error code: ' + e.code + "\n")
        except URLError as e:
            self.logfile.write('ERROR: http://www.allocine.fr/film/fichefilm-' + item["ident"] + '/critiques/presse/' + "\n")
            self.logfile.write('We failed to reach a server.' + "\n")
            self.logfile.write('Reason: ' + e.reason + "\n")
        else:
            f = open('/home/pesto/allocine/html/' + item["ident"] + '-reviews.html', 'wb')
            f.write(u.read())
            f.close()
            u.close()
            self.logfile.write('http://www.allocine.fr/film/fichefilm-' + item["ident"] + '/critiques/presse/' + ' downloaded' + "\n")

        # Enregistrement du casting du film
        try:
            u = urllib.urlopen('http://www.allocine.fr/film/fichefilm-' + item["ident"] + '/casting/')
        except HTTPError as e:
            self.logfile.write('ERROR: http://www.allocine.fr/film/fichefilm-' + item["ident"] + '/casting/' + "\n")
            self.logfile.write('The server couldn\'t fulfill the request.' + "\n")
            self.logfile.write('Error code: ' + e.code + "\n")
        except URLError as e:
            self.logfile.write('ERROR: http://www.allocine.fr/film/fichefilm-' + item["ident"] + '/casting/' + "\n")
            self.logfile.write('We failed to reach a server.' + "\n")
            self.logfile.write('Reason: ' + e.reason + "\n")
        else:
            f = open('/home/pesto/allocine/html/' + item["ident"] + '-casting.html', 'wb')
            f.write(u.read())
            f.close()
            u.close()
            self.logfile.write('http://www.allocine.fr/film/fichefilm-' + item["ident"] + '/casting/' + ' downloaded' + "\n")

        return item

class ImgWriterPipeline(object):
   
    def __init__(self):
            self.logfile = open('/home/pesto/allocine/img.log', 'wb')

    def process_item(self, item, spider):
        
        # Enregistrement de l'affiche du film
        try:
            u = urllib.urlopen(item["affiche"])
        except HTTPError as e:
            self.logfile.write("ERROR: " + item["affiche"] + "\n")
            self.logfile.write('The server couldn\'t fulfill the request.' + "\n")
            self.logfile.write('Error code: ' + e.code + "\n")
        except URLError as e:
            self.logfile.write("ERROR: " + item["affiche"] + "\n")
            self.logfile.write('We failed to reach a server.' + "\n")
            self.logfile.write('Reason: ' + e.reason + "\n")
        else:
            f = open('/home/pesto/allocine/img/' + item["ident"] + "." + item["affiche"].split(".")[-1], 'wb')
            f.write(u.read())
            f.close()
            u.close()
            self.logfile.write(item["affiche"] + ' downloaded' + "\n")
       
        return item
