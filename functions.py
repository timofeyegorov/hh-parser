import requests

def get_valutes():
    rates = {}
    valutes = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    valutes = valutes.json()['Valute']
    for key in valutes.keys():
        rates[key] = [valutes[key]['Value'], valutes[key]['Nominal']]
    return rates

def convert_salary(value, rates, valute):
    return value * rates[valute][0] / rates[valute][1]

def read_salary(key, rates):
    if key == None:
        return [0, 'Зарплата не указана']
    else:
        min_salary = key['from']
        max_salary = key['to']
        currency_valute = key['currency']
        if currency_valute != 'RUR':
            if currency_valute == 'BYR':
               currency_valute = 'BYN'
            if min_salary != None:
                min_salary = convert_salary(min_salary, rates, currency_valute)
            if max_salary != None:
                max_salary = convert_salary(max_salary, rates, currency_valute)
        if max_salary == None:
            return [1, min_salary]
        elif min_salary == None:
            return [2, max_salary]
        else:
            return [3, min_salary, max_salary]

def salary_comparison(cur_salary, coparison_value, flag=True):
    if flag:
        return cur_salary if cur_salary > coparison_value else coparison_value
    else:
        return cur_salary if cur_salary < coparison_value else coparison_value

def count_requirements(vocabulary):
    requirements_dict = {}
    for word in vocabulary:
        if word in requirements_dict.keys():
            requirements_dict[word] += 1
        else:
            requirements_dict[word] = 1
    return requirements_dict

def get_area_id(AREAS, area_name):
    area_id = '0'
    for i in range(len(AREAS)):
        # print('1.' + AREAS[i]['name'])
        for j in range(len(AREAS[i]['areas'])):
            # print('   2.' + AREAS[i]['areas'][j]['name'])
            if area_name.lower() == AREAS[i]['areas'][j]['name'].lower():
                area_id = AREAS[i]['areas'][j]['id']
            for k in range(len(AREAS[i]['areas'][j]['areas'])):
                # print('      3.' + AREAS[i]['areas'][j]['areas'][k]['name'])
                if area_name.lower() == AREAS[i]['areas'][j]['areas'][k]['name'].lower():
                    area_id = AREAS[i]['areas'][j]['areas'][k]['id']
    return area_id