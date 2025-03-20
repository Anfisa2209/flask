import datetime

from flask import Flask

from data.db_session import global_init, create_session
from data.department import Department
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    # db/mars.db
    global_init('db/mars.db')
    session = create_session()


    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = 'captain'
    user.speciality = 'research engineer'
    user.address = 'module_1'
    user.email = 'scott_chief@mars.org'
    user.hashed_password = '1cap'
    user.set_password(user.hashed_password)

    session.add(user)
    session.commit()

    user = User()
    user.surname = "Борщов"
    user.name = "Вася"
    user.age = 23
    user.position = 'captain'
    user.speciality = 'research engineer'
    user.address = 'module_2'
    user.email = 'scott_chief1@mars.org'
    user.hashed_password = '124a'
    user.set_password(user.hashed_password)
    session.add(user)
    session.commit()

    user = User()
    user.surname = "Березов"
    user.name = "Петя"
    user.age = 25
    user.position = 'captain'
    user.speciality = 'research engineer'
    user.address = 'module_3'
    user.email = 'email@mars.org'
    user.hashed_password = '124a'
    user.set_password(user.hashed_password)

    session.add(user)
    session.commit()

    user = User()
    user.surname = "Березов"
    user.name = "Саша"
    user.age = 25
    user.position = 'captain'
    user.speciality = 'research engineer'
    user.address = 'module_3'
    user.email = 'email2@mars.org'
    user.hashed_password = '124a'
    user.set_password(user.hashed_password)

    session.add(user)
    session.commit()

    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    session.add(job)
    session.commit()

    dep = Department()
    dep.title = 'Геологическая разведка'
    dep.chief = 1
    dep.members = '1, 2, 3'
    dep.email = 'scott_chief@mars.org'

    session.add(dep)
    session.commit()


if __name__ == '__main__':
    main()
