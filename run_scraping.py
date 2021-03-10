
import os, sys


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
import django
django.setup()

from scraping.parser import hh
from scraping.models import Vacancy, City, NameProf, Error
from django.db import DatabaseError
parser = ((hh, 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&no_magic=true&specialization=1&page=2'),
          (hh, 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&no_magic=true&specialization=1&page=1'),
          (hh, 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&no_magic=true&specialization=1&page=4'),
          (hh, 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&no_magic=true&specialization=1&page=0')
)

city = City.objects.all().first()
prof = NameProf.objects.all().first()
jobs, errors = [], []
for func, url in parser:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, prof=prof)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save()
