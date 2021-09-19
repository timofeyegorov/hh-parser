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
# import ast
#
# with open('recomendation.txt', 'r', encoding='utf-8') as f:
#     text = f.read()
#
# print(text)
# print(type(ast.literal_eval(text)))
dd = {'1': 'Tima', '2': 'Anna'}
print(dd[0])