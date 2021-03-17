import ast
import os
import sys
import datetime
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
import django
django.setup()
from scraping.models import Vacancy, Errors, Url
from scraping_service.settings import EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f'New Vacancy from LAUTService {today}'
text_content = 'New Vacancy from LAUTService'
from_email = EMAIL_HOST_USER

empty = '<h2>К сожалению к вашим предпочтениям данных нет</h2>'
User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'prof', 'email')
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['prof']), [])
    users_dct[(i['city'], i['prof'])].append(i['email'])
if users_dct:
    params = {'city_id__in': [], 'prof_id__in': []}
    for pr in users_dct.keys():
        params['city_id__in'].append(pr[0])
        params['prof_id__in'].append(pr[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()[:10]
    vacancies = {}
    for q in qs:
        vacancies.setdefault((q['city_id'], q['prof_id']), [])
        vacancies[(q['city_id'], q['prof_id'])].append(q)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<div><h3><a href="{ row["url"] }">{ row["title"] }</a></h3><h5 align="right">{ row["earning"] }</h5></div>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
#не работает блять нихуя говное баное JSON
#if qs.exists():
    #error = qs.first()
    #error.data = ast.literal_eval(error.data)
    #city = error.data['city']
    #prof = error.data['prof']
    #email = error.data['email']
    #_html += '<hr>'
    #_html += '<h2> </h2>'
    #_html += f"<div><h3>City>{city}, Prof: {prof}, Email: {email} </h3></div>"
    #subject += f'Пожелания пользователя {today}'
    #text_content += f'Пожелания пользователя {today}'


qs = Url.objects.all().values('city', 'prof')
urls_dct = {(i['city'], i['prof']): True for i in qs}
urls_errors = ''
for keys in users_dct.keys():
    if keys not in urls_dct:
        if keys[0] and keys[1]:
            urls_errors += f'<div><h3> For city: { keys[0] } And proffesion: { keys[1] }, doesnt have URL</h3></div>'

if urls_errors:
    subject += 'Отсуствуют URL'
    _html += urls_errors

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()