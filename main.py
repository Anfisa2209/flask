import os

from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    astronaut_id = StringField('ID астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    cap_id = StringField('ID капитана', validators=[DataRequired()])
    cap_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/table/<string:sex>/<int:age>')
def table(sex, age):
    return render_template('table.html', sex=sex, age=age)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return render_template('success.html', title='Успех')


@app.route('/distribution')
def distribution():
    return render_template('distribution.html')


@app.route('/gallery', methods=['POST', 'GET'])
def gallery():
    if request.method == 'GET':
        image_list = return_files('static/img/mars_img')
        return render_template('gallery.html', image_list=image_list)

    elif request.method == 'POST':
        f = request.files['file']

        number = len(return_files('static/img/mars_img')) + 1
        with open(f'static/img/mars_img/mars{number}.png', 'wb') as image_file:
            image_file.write(f.read())

        image_list = return_files('static/img/mars_img')
        return render_template('gallery.html', image_list=image_list)


def return_files(path):
    file_list = []
    for currentdir, dirs, files in os.walk(path):
        for file in files:
            file_list.append(f'{path}/{file}')
    return file_list


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
