import datetime
from django.utils.timezone import utc
from status.models import *

models_list = ['ActorWeight', 'Country', 'Film', 'Genre', 'GenrePopularKeyword', 'Institution', 'InstitutionInfluence', 'Journal', 'JournalInfluence', 'Keyword', 'Language', 'Person', 'Prize', 'ProductionCompany', 'Review', 'Reviewer']

for item  in models_list:
    entry = TableUpdateTime()
    entry.model_name = item
    entry.update_time = datetime.datetime.utcnow().replace(tzinfo=utc)
    entry.save()
    del entry

