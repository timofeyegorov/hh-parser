import requests

with open('areas.txt', 'w', encoding='utf-8') as f:
    text = f.write(requests.get('https://api.hh.ru/areas/').text)