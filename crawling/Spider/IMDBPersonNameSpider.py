from cinema.models import Person
from status.models import IMDBPersonStatus

named_persons = Person.objects.exclude(name='')


for person in named_persons:
    print 'Person: ', person.imdb_id
    try:
        status = IMDBPersonStatus.objects.get(imdb_id=person.imdb_id)
    except IMDBPersonStatus.DoesNotExist:
        print "Status doesn't exist"
        status = IMDBPersonStatus(imdb_id=person.imdb_id,
                                  downloaded=0, extracted=0,
                                  priority=1000000, name=0, image=0)
    status.name = 1
    status.save()

