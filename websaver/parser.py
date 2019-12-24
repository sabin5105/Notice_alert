import requests
from bs4 import BeautifulSoup
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")
import django
django.setup()
from parsed_data.models import WebData

def parse_web():
    req = requests('http://www.seoultech.ac.kr/service/info/janghak/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select(
        'tr > a'
    )
    data = {}
    for title in my_titles:
        data[title.text] = title.get('href')
    return data

if __name__=='__main__':
    blog_data_dict = parse_web()
    for t, l in blog_data_dict.items():
        WebData(title=t, link=l).save()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data = parse_web()

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file)