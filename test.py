# import requests
#
# # Базовый url
# URL = 'https://api.hh.ru/'
# vacancy_name = 'python-developer'
# num = 1
# # Параметры
# params = {
#     'text': f'NAME:({vacancy_name})',
#     'area': '2',
#     'page': num,
#     'per_page': 5}
#
# response = requests.get(URL + 'vacancies', params=params)
# print(response.status_code)
# res = response.json()
# print(res)
import json
from pprint import pprint


area_id = '1'

with open('areas.txt', 'r', encoding='utf-8') as f:
    text = f.read()

AREAS = json.loads(text)

for i in range(len(AREAS)):

# pprint(AREAS)