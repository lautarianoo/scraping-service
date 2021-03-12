
import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
import django
django.setup()

from scraping.parser import hh
from scraping.models import Vacancy, City, NameProf, Errors, Url
from django.db import DatabaseError

User = get_user_model()
parser = ((hh, 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&no_magic=true&specialization=1&page=2'),
          (hh, 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&no_magic=true&specialization=1&page=1'),
          (hh, 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&no_magic=true&specialization=1&page=4'),
          (hh, 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&no_magic=true&specialization=1&page=0')
)

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['prof_id']) for q in qs)
    return settings_lst

def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['prof_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['prof'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls

q = get_settings()
u = get_urls(q)
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
    er = Errors(data=errors).save()
