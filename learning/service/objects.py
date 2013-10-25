import datetime
import dateutil.parser
import pickle
from django.utils.timezone import utc

CACHE_DIRECTORY = './cache/'

class ParsingError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CachedObject:
    def __init__(self, name, content = None):
        try:
            fi = open(CACHE_DIRECTORY + name + '.cache', 'r')
            d = pickle.load(fi)
            fi.close()
            self.name = d['name']
            self.saved = d['saved']
            self.modified = d['modified']
            self.version = d['version']
            self.checksum = d['checksum']
            self.obj = d['obj']
            print('Initializing ' + self.name + ' at version ' + self.version.isoformat() + '.')
        except:
            print('Cache file "' + name + '.cache" does not exist or cannot be read : creating new object ...')
            self.name = name
            self.saved = False
            self.modified = True
            self.version = datetime.datetime.utcnow().replace(tzinfo=utc)
            self.checksum = ''
            self.obj = content

    def get_content(self):
        return self.obj

    def set_content(self, obj):
        self.obj = obj
        self.modified = True

    def save(self):
        if not self.saved:
            try:
                fi = open(CACHE_DIRECTORY + self.name + '.cache', 'w')
                pickle.dump({'name':self.name, 'saved' : True, 'modified' : False, 'version' : self.version, 'obj' : self.obj}, fi)
                fi.close()
                print('Writing ' + self.name + '.cache ...')
            except IOError:
                print('Object ' + self.name + ' cannot be cached.')
                self.saved = False

    def __str__(self):
        return self.name

    def update_status(self):
        '''                                                                                                                                                                         
        Function to be overridden : check if the object has been modified and update status, version and signature.                                                                 
        '''
        pass

class LearningService(object):
    def __init__(self, list_file="cache_list"):
        self.init_time = datetime.datetime.now()
        self.clist = CachedObject(list_file, content = [])
        self.cobjects = [self.clist]

    def load_cobject(self, name):
        if name in self.clist.get_content():
            if not name in map(str, self.cobjects):
                self.cobjects.append( CachedObject(name) )
            else:
                print(name + " already loaded.")
        else:
            print(name + " does not exist in the cache. Please create it if needed.")

    def create_cobject(self, name, obj):
        if name in self.clist.get_content():
            print("Name " + name + " is already taken.")
        else:
            self.cobjects.append( CachedObject(name, content = obj) )
            l = self.clist.get_content()
            l.append(name)
            self.clist.set_content(l)
            print("Object " + name + " created and added to cache.")

    def get_cobject(self, name):
        try:
            return self.cobjects[map(str, self.cobjects).index(name)]
        except:
            print("No object found in cache with name " + name + ". Returned None instead.")
            return None

    def save_cache(self):
        for co in self.cobjects:
            if co.modified and not co.saved:
                co.save()
    
    def quit(self):
        print("Learning service initialized at "+ self.init_time.isoformat()  +" is closing : objects are being cached.")
        self.save_cache()
