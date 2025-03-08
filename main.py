from flask import Flask, render_template

app = Flask(__name__)


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof=prof)


@app.route('/list_prof/<lst>')
def list_prof(lst):
    professions = ['инженер', 'врач', 'строитель', 'пилот', 'штурман']
    return render_template('list_prof.html', list=lst, professions=professions)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
