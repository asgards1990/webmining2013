import json
import urllib

class JsonWriterPipeline(object):
    
    def __init__(self):
        self.file = open('/home/pesto/allocine/films_list.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class HtmlWriterPipeline(object):
    
    def process_item(self, item, spider):
        
        # Enregistrement de la fiche principale du film
        try:
            u = urllib.urlopen('http://www.allocine.fr' + item["url"])
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
            f = open('/home/pesto/allocine/html/' + item["ident"] + '.html', 'wb')
            f.write(u.read())
            f.close()
            u.close()
        
        # Enregistrement des critiques du film
        try:
            u = urllib.urlopen('http://www.allocine.fr/film/fichefilm-' + item["ident"] + '/critiques/presse/')
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
            f = open('/home/pesto/allocine/html/' + item["ident"] + '-reviews.html', 'wb')
            f.write(u.read())
            f.close()
            u.close()

        # Enregistrement du casting du film
        try:
            u = urllib.urlopen('http://www.allocine.fr/film/fichefilm-' + item["ident"] + '/casting/')
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
            f = open('/home/pesto/allocine/html/' + item["ident"] + '-casting.html', 'wb')
            f.write(u.read())
            f.close()
            u.close()

        return item

class ImgWriterPipeline(object):
    
    def process_item(self, item, spider):
        
        # Enregistrement de l'affiche du film
        try:
            u = urllib.urlopen(item["affiche"])
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
            f = open('/home/pesto/allocine/img/' + item["ident"] + "." + item["affiche"].split(".")[-1], 'wb')
            f.write(u.read())
            f.close()
            u.close()
       
        return item
