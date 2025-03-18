import json
import os
import random

from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired

from SQL.data.db_session import global_init, create_session
from SQL.data.jobs import Jobs
from SQL.data.users import User


class LoginForm(FlaskForm):
    astronaut_id = StringField('ID астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    cap_id = StringField('ID капитана', validators=[DataRequired()])
    cap_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('position', validators=[DataRequired()])
    speciality = StringField('speciality', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('Submit')


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
    return render_template('success.html', title='Успех', content='Доступ разрешен, добро пожаловать на корабль')


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


@app.route('/member')
def random_member():
    with open('templates/crew_members.json', encoding='utf8') as json_file:
        data = json.load(json_file)
    member = random.choice(data)
    return render_template('member.html', member=member)


@app.route('/')
def works_log():
    global_init('SQL/db/mars.db')
    session = create_session()
    jobs = session.query(Jobs)
    captions = ['Title of activity', 'Team leader', 'Duration', 'List of collaborators', 'Is finished']
    team_leaders = [f"{user.name} {user.surname}" for job in jobs
                    for user in session.query(User).filter(User.id == job.team_leader)]
    return render_template('work.html', jobs=jobs, captions=captions, team_leaders=team_leaders)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        global_init('SQL/db/mars.db')
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.age.data < 0:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Возраст не может быть отрицательным!")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/successful_login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/successful_login')
def successful_login():
    return render_template('success.html', title='Успех', content='Вы успешно зарегистрированы')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
