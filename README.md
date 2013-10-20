webmining2013
=============

To use Django's models from other Python programs, set the following paths:

export DJANGO_SETTINGS_MODULE=website.settings
export PYTHONPATH=/home/pesto/webmining2013/website:$PATH

and for example in the Python file:
from cinema.models import Country
