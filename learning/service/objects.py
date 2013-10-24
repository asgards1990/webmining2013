import datetime
import dateutil.parser
import pickle

class ParsingError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CachedObject:
    def __init__(self, name, default = None):
        try:
            fi = open('_' + name, 'r')
            d = pickle.load(fi)
            fi.close()
            self.name = d['name']
            self.saved = d['saved']
            self.modified = d['modified']
            self.version = d['version']
            self.obj = d['obj']
            print('Initializing ' + self.name + ' at version ' + self.version.isoformat() + '.')
        except:
            print('Cache file "_' + name + '" does not exist or cannot be read : creating new object ...')
            self.name = name
            self.saved = False
            self.modified = True
            self.version = datetime.datetime.now()
            self.obj = default

    def _(self):
        return self.obj

    def update(self, obj):
        self.obj = obj
        self.modified = True

    def save(self):
        if not self.saved:
            try:
                fi = open('_' + self.name, 'w')
                pickle.dump({'name':self.name, 'saved' : True, 'modified' : False, 'version' : self.version, 'obj' : self.obj}, fi)
                fi.close()
                print('Writing _' + self.name + '...')
            except IOError:
                print('Object ' + self.name + 'cannot be cached.')
                self.saved = False

    def __str__(self):
        return self.name

    def update_status(self):
        '''                                                                                                                                                                         
        Function to be overridden : check if the object has been modified and update status, version and signature.                                                                 
        '''
        pass

class LearningService(object):
    def __init__(self, list_file="cache"):
        self.init_time = datetime.datetime.now()
        self.clist = CachedObject(list_file, default = [])
        self.cobjects = []
        for name_object in self.clist._():
            self.cobjects.append( CachedObject(name_object, None ) )

    def save_cache(self):
        if self.clist.modified and not self.clist.saved:
            self.clist.save()
        for co in self.cobjects:
            if co.modified and not co.saved:
                co.save()
    
    def quit(self):
        print("Learning service initialized at "+ self.init_time.isoformat()  +" is closing : tables are being cached.")
        self.save_cache()
