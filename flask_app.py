from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form/', methods = ['GET', 'POST'])
def form():
    if request.method == 'POST':
        vacancy_name = request.form['vacancy_name']
        print(vacancy_name)
        return render_template('form.html')
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

if __name__ == '__main__':
    app.run(debug=True)