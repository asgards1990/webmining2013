import datetime
import dateutil.parser

class ParsingError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class LearningService(object):
    def __init__(self):
        self.init_time = datetime.datetime.now()
    
    def quit(self):
        print("Learning service initialized at "+ self.init_time.isoformat()  +" is closing : tables are being cached.")
