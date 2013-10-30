webmining2013
=============

To use Django's models from other Python programs, set the following paths:

--POUR LINUX--
export DJANGO_SETTINGS_MODULE=website.settings
export PYTHONPATH=/home/pesto/webmining2013/website:$PYTHONPATH
--POUR WINDOWS--
set DJANGO_SETTINGS_MODULE=website.settings
set PYTHONPATH=C:\Users\user1\webmining2013\website;%PYTHONPATH%
and for example in the Python file:
from cinema.models import Country
