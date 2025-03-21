from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from SQL.data import db_session
from SQL.data.job_form import JobForm
from SQL.data.jobs import Jobs
from SQL.data.login_form import LoginForm
from SQL.data.register_form import RegisterForm
from SQL.data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_ses = db_session.create_session()
    return db_ses.get(User, user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/")
def works_log():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    # users = session.query(User).all()
    # names = {name.id: {name.surname, name.name} for name in users}
    # return render_template('index.html', jobs=jobs, names=names, )
    captions = ['Title of activity', 'Team leader', 'Duration', 'List of collaborators', 'Is finished']
    team_leaders = [f"{user.name} {user.surname}" for job in jobs
                    for user in session.query(User).filter(User.id == job.team_leader)]
    return render_template('work.html', jobs=jobs, captions=captions, team_leaders=team_leaders)


@app.route("/addjob", methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            work_size=form.duration.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            team_leader=form.team_leader.data)
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Добавить работу', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobForm()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id, (Jobs.user == current_user) | (current_user.id == 1)).first()

    if not job:
        abort(404)
    if request.method == "GET":
        form.job.data = job.job
        form.duration.data = job.work_size
        form.collaborators.data = job.collaborators
        form.team_leader.data = job.team_leader
        form.is_finished.data = job.is_finished

    if form.validate_on_submit():
        job.job = form.job.data
        job.work_size = form.duration.data
        job.collaborators = form.collaborators.data
        job.team_leader = form.team_leader.data
        job.is_finished = form.is_finished.data

        db_sess.commit()
        return redirect('/')

    return render_template(
        'addjob.html',
        title='Редактирование работы',
        form=form
    )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.user == current_user) | (current_user.id == 1)
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init('SQL/db/mars.db')
    app.run(port=8080, host='127.0.0.1')
