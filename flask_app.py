from flask import Flask, render_template, request, Response
from main import main_function
import ast

app = Flask(__name__)
app.static_folder = 'static'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/for_test/')
def for_test():
    x1 = {'1':'Тима', '2':'Вася', '3':'Дима', '4':'Пидор'}
    return render_template('for_test.html', x1=x1)

@app.route('/form/', methods = ['GET', 'POST'])
def form():
    if request.method == 'POST':
        text = ' '
        vacancy_name = request.form['vacancy_name']
        region = request.form['region']
        result_dict = main_function(vacancy_name, region)
        if type(result_dict) == list:
            if result_dict[0] == 'Такого региона не существует':
                return render_template('breaking_result.html', result_dict=result_dict, text=text)
            elif result_dict[0] == 'По ключевой фразе в данном регионе не найдено вакансий':
                return render_template('breaking_result.html', result_dict=result_dict, text=text)
        else:
            with open('recomendation.txt', 'r', encoding='utf-8') as f:
                text = f.read()
            text = ast.literal_eval(text)
            return render_template('result.html', result_dict=result_dict, text=text)
    else:
        return render_template('form.html')

@app.route('/feedback/')
def feedback():
    return render_template('feedback.html')

@app.route('/about_me/')
def about_me():
    return render_template('about_me.html')

@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')

@app.route('/getCSV')
def getCSV():

    csv = '1;2;3;4'
    return Response(csv, mimetype='text/csv',
                    headers={'Content-disposition':
                             "attachment; filename=report.csv"})

if __name__ == '__main__':
    app.run(debug=True)