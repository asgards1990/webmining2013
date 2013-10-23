from cinema.models import *

# THIS SCRIPT FILLS ALL GENRE ENTRIES IN THE DATABASE

genres_list = ['Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','Film-Noir','Game-Show','History','Horror','Music','Musical','Mystery','News','Reality-TV','Romance','Sci-Fi','Sport','Talk-Show','Thriller','War','Western']

for item in genres_list:
    Genre.objects.create(name=item)
