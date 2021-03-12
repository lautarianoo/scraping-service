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
        urls.append(tmp)
    return urls

async def main(value):
    func, url, city, prof = value
    job, er = await loop.run_in_executor(None, func, url, city, prof)
    errors.extend(er)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

jobs, errors = [], []
loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['prof'])
             for data in url_list for func, key in parser]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
loop.run_until_complete(tasks)
loop.close()
for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Errors(data=errors).save()
