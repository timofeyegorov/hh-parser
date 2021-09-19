from functions import *
import json
import sys

def main_function(vacancy_name, area_name):
    # Получаем список с регионами и их id
    with open('areas.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    AREAS = json.loads(text)

    # Название вакансии регион для поиска
    # vacancy_name = 'python-developer'
    # area_name = 'Новосибирск'

    # Получаем id региона
    area_id = get_area_id(AREAS, area_name)
    # Если id равно 0, то такого региона нет
    if area_id == '0':
        answer = ['Такого региона не существует',
                  'Поробуйте поменять регион поиска']
        return answer

    # Получаем курсы валют
    rates = get_valutes()

    # Базовый url
    URL = 'https://api.hh.ru/'

    # Исходные переменные
    min_salary = 400000 # Минимальная зарплата
    max_salary = 0 # Максимальная зарплата

    min_sum_salary = 0 # Сумма всех минимальных зарплат
    min_salary_indicated = 0 # Количество вакансий с указанными минимальными зарплатами
    min_average_salary = 0 # Средняя минимальная зарплата

    max_sum_salary = 0 # Сумма всех максимальных зарплат
    max_salary_indicated = 0 # Количество вакансий с указанными максимальными зарплатами
    max_average_salary = 0 # Средняя максимальная зарплата

    num_vacancies = 0 # Количество вакансий
    vocabulary = [] # Словарь для описаний вакансий

    for num in range(5):
        # Параметры
        params = {
            'text': f'NAME:({vacancy_name})',
            'area': f'{area_id}',
            'page': num,
            'per_page': 100}

        # Получаем ответ от сервера, переводим в json формат
        response = requests.get(URL + 'vacancies', params=params)
        # print(response.status_code)
        res = response.json()
        # print(res)
        for i in range(len(res['items'])):
            # print(res['items'][i]['name'])
            # print(res['items'][i]['salary'])
            curr_salary = read_salary(res['items'][i]['salary'], rates)
            if curr_salary[0] == 0:
                pass
            elif curr_salary[0] == 1:
                min_sum_salary += curr_salary[1]
                min_salary_indicated += 1
                min_salary = salary_comparison(curr_salary[1], min_salary, flag=False)
            elif curr_salary[0] == 2:
                max_sum_salary += curr_salary[1]
                max_salary_indicated += 1
                max_salary = salary_comparison(curr_salary[1], max_salary)
            else:
                min_sum_salary += curr_salary[1]
                min_salary_indicated += 1
                max_sum_salary += curr_salary[2]
                max_salary_indicated += 1
                min_salary = salary_comparison(curr_salary[1], min_salary, flag=False)
                max_salary = salary_comparison(curr_salary[2], max_salary)
            if res['items'][i]['snippet']['requirement'] != None:
                vocabulary += res['items'][i]['snippet']['requirement'].lower()\
                              .replace('.', '')\
                              .replace(',', '')\
                              .replace('(', '')\
                              .replace(')', '')\
                              .replace('*', '')\
                              .replace('/', ' ')\
                              .replace(':', ' ')\
                              .replace('«', ' ')\
                              .replace('»', ' ')\
                              .replace('...', '').split()
        num_vacancies += len(res["items"])

    if num_vacancies == 0:
        answer = ['По ключевой фразе в данном регионе не найдено вакансий',
                  'Поробуйте расширить регион поиска или введите другое название вакансии']
        return answer

    requirements_dict = count_requirements(vocabulary)
    # print(vocabulary)
    # Проверка, что словарь создан верно
    # print(len(vocabulary) == sum(list(requirements_dict.values())))
    min_average_salary = min_sum_salary / min_salary_indicated if min_salary_indicated != 0 else 0
    max_average_salary = max_sum_salary / max_salary_indicated if max_salary_indicated != 0 else 0

    average_salary = min_average_salary + (max_average_salary - min_average_salary) / 2

    result_dict = {k: v for k,v in sorted(requirements_dict.items(), key=lambda x: x[1], reverse=True)}
    filter_list = ['работы', 'знание', 'на', 'от', 'лет', 'понимание', 'или', 'знания', 'умение', 'of', 'уверенное',
                   'года', 'не', 'in', 'владение', 'принципов', 'хорошее', 'with', 'языка', 'knowledge', 'and',
                   'навыки', 'years', 'менее', 'уровне', 'проектирования', 'как', '3-х', '3+', 'по', 'имеет',
                   'писать', 'работать', 'из', 'для', 'использования', 'структур', 'их', 'or', '2-х', 'отличное']

    key_words = {}
    skip_idx = 0
    for idx,item in enumerate(result_dict.items()):
        if (len(item[0]) > 1) and (item[0] not in filter_list) and (idx - skip_idx < 50):
            # print(item)
            key_words.update({item[0]: item[1]})
        else:
            skip_idx += 1

    with open('recomendation.txt', 'w', encoding='utf-8') as f:
        f.write(f'{key_words}')

    return {'Всего найдено вакансий': num_vacancies,
            'Вакансий где указана минимальная ЗП': min_salary_indicated,
            'Вакансий где указана максимальная ЗП': max_salary_indicated,
            'Минимальная зарплата рублей': round(min_salary, 2),
            'Максимальная зарплата рублей': round(max_salary, 2),
            'Минимальная средняя зарплата рублей': round(min_average_salary, 2),
            'Максимальная средняя зарплата рублей': round(max_average_salary, 2),
            'Средняя зарплата рублей': round(average_salary, 2)}