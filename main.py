from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from requests import get

from SQL.data import db_session
from SQL.data.department import Department
from SQL.data.department_form import DepartmentForm
from SQL.data.job_form import JobForm
from SQL.data.jobs import Jobs
from SQL.data.old_login_form import LoginForm as OldLoginForm
from SQL.data.register_form import RegisterForm
from SQL.data.users import User
from api.jobs_api import jobs_bp
from api.user_api import user_bp
from api_v2.jobs_resource import JobsResource, JobsListResource
from api_v2.users_resource import UsersResource, UsersListResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.register_blueprint(jobs_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')

api_version2 = Api(app)
api_version2.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
api_version2.add_resource(UsersListResource, '/api/v2/users')

api_version2.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')
api_version2.add_resource(JobsListResource, '/api/v2/jobs')

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/distribution')
def distribution():
    user_list = ['Ваня', 'Петя', 'Саша', 'Кирилл']
    return render_template('distribution.html', user_list=user_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = OldLoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return render_template('success.html', title='Успех', content='Добро пожаловать на корабль')


@login_manager.user_loader
def load_user(user_id):
    db_ses = db_session.create_session()
    return db_ses.get(User, user_id)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).filter(User.email == form.email.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user, remember=form.remember_me.data)
#             return redirect("/")
#         return render_template('login.html',
#                                message="Неправильный логин или пароль",
#                                form=form)
#     return render_template('login.html', title='Авторизация', form=form)
#

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
            email=form.email.data,
            city_from=form.city_from.data
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


@app.route('/departments', methods=['GET', 'POST'])
def department_view():
    session = db_session.create_session()
    departments = session.query(Department)
    captions = ['Title of department', 'Chief', 'Members', 'Email']
    return render_template('departments.html', departments=departments, captions=captions)


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Department).filter(Department.email == form.email.data).first():
            return render_template('add_department.html', title='Регистрация',
                                   form=form,
                                   message="Такой email уже есть")
        department = Department(
            title=form.title.data,
            members=form.members.data,
            email=form.email.data,
            chief=form.chief.data)
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_department.html', title='Добавить департамент', form=form)


@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id,
                                                  (Department.chief_user == current_user) | (
                                                          current_user.id == 1)).first()

    if not department:
        abort(404)
    if request.method == "GET":
        form.title.data = department.title
        form.chief.data = department.chief
        form.members.data = department.members
        form.email.data = department.email

    if form.validate_on_submit():
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data

        db_sess.commit()
        return redirect('/departments')

    return render_template(
        'add_department.html',
        title='Редактирование депортамента',
        form=form
    )


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id,
                                                  (Department.chief == current_user.id) | (current_user.id == 1)
                                                  ).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


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
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.team_leader == current_user.id) | (current_user.id == 1)
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/users_show/<int:user_id>', methods=['GET'])
@login_required
def users_show(user_id):
    if user_id != current_user.id:
        return abort(403)
    user_info = get(f'http://localhost:8080/api/users_show/{user_id}').json()
    status_code = get(f'http://localhost:8080/api/users_show/{user_id}').status_code
    if not user_info.get('users'):
        return abort(status_code)
    return render_template('users_show.html', user=user_info['users'][0])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init('SQL/db/mars.db')
    app.run(port=8080, host='127.0.0.1', debug=True)
