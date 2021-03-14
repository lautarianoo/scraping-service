import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint


headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'},

    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'},

    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'}
]

def hh(url, city=None, prof=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'vacancy-serp'})
            div_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})
            if main_div:
                for div in div_list:
                    earning = div.find('div', attrs={'class': 'vacancy-serp-item__sidebar'})
                    title = div.find('span', attrs={'class': 'g-user-content'})
                    href = title.a['href']
                    content = div.find('div', attrs={'class': 'g-user-content'})
                    company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
                    jobs.append({'title': title.text, 'url': href, 'description': content.text, 'company': company.text, 'earning': earning.text, 'city_id': city, 'prof_id': prof})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page you not response'})
        return jobs, errors

if __name__ == '__main__':
    url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&no_magic=true&specialization=1&page=4'
    jobs, errors = hh(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
