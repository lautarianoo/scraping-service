import asyncio
import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
import django
django.setup()

from scraping.parser import hh
from scraping.models import Vacancy, Errors, Url
from django.db import DatabaseError
import json
import ast

User = get_user_model()
parser = ((hh, 'hh'),
          (hh, 'hh'),
          (hh, 'hh'),
          (hh, 'hh')
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
        tmp['url_data'] = ast.literal_eval(tmp['url_data'])
        urls.append(tmp)
    return urls

settings = get_settings()
url_list = get_urls(settings)

jobs, errors = [], []

for data in url_list:
    for func, key in parser:
        url = data['url_data'][key]
        j, e = func(url, city=data['city'], prof=data['prof'])
        jobs += j
        errors += e

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Errors(data=errors).save()
