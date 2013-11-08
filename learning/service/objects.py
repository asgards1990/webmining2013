import datetime
import pickle
from django.utils.timezone import utc
from sklearn.externals import joblib

CACHE_DIRECTORY = './cache/'
JOBLIB_DIRECTORY = './joblib/'

class ParsingError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CachedObject:
    def __init__(self, name):
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
            self.loaded = True
        except:
            print('Cache file "' + name + '.cache" does not exist or cannot be read. Create it if needed.')
            self.name = name
            self.loaded = False

    def create(self, content):
        self.saved = False
        self.modified = True
        self.version = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.checksum = ''
        self.obj = content
        self.loaded = True
        return self

    def get_content(self):
        return self.obj

    def set_content(self, obj):
        self.obj = obj
        self.modified = True
        self.saved = False

    def save(self):
        if not self.saved:
            try:
                fi = open(CACHE_DIRECTORY + self.name + '.cache', 'w')
                pickle.dump({'name':self.name, 'saved' : True, 'modified' : False, 'version' : self.version, 'checksum' : self.checksum, 'obj' : self.obj}, fi)
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
        self.clist = CachedObject(list_file)
        if not self.clist.loaded:
            self.clist.create([])
        self.cobjects = [self.clist]
    
        for name in self.clist.get_content():
            self.load_cobject(name)

    def is_loaded(self, name):
        return name in map(str, self.cobjects)

    def load_cobject(self, name):
        if name in self.clist.get_content():
            if not name in map(str, self.cobjects):
                c = CachedObject(name)
                if c.loaded:
                    self.cobjects.append(c)
            else:
                print(name + " already loaded.")
        else:
            print(name + " does not exist in the cache. Please create it if needed.")

    def create_cobject(self, name, obj):
        if name in self.clist.get_content():
            print("Name " + name + " is already taken. Overriding if not loaded ...")
            if not self.is_loaded(name):
                self.cobjects.append( CachedObject(name).create(obj) )
                print("Object " + name + " created and added to cache.")
        else:
            self.cobjects.append( CachedObject(name).create(obj) )
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

    def dumpJoblibObject(self,obj,filename):
        joblib.dump(obj,JOBLIB_DIRECTORY + filename + '.pkl', compress=9)

    def loadJoblibObject(self,filename):
        return joblib.load(JOBLIB_DIRECTORY + filename + '.pkl')

    def quit(self):
        print("Learning service initialized at "+ self.init_time.isoformat()  +" is closing : objects are being cached.")
        self.save_cache()
