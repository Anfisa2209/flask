from requests import get, post, put, delete


def test_api():
    print(get('http://localhost:8080/api/users').json())
    print(get('http://localhost:8080/api/users/1').json())
    print(delete('http://localhost:8080/api/users/7').json())
    print(post('http://localhost:8080/api/users', json={
        'surname': "test api",
        'name': "test api",
        'age': 1,
        'position': "test api",
        'speciality': "test api",
        'address': "test api",
        'email': "test_api@a.ru",
        'password': '123'
    }).json())
    print(put('http://localhost:8080/api/users/7', json={
        'surname': "test api",
        'name': "name",
        'age': 1,
        'position': "test api",
        'speciality': "test api",
        'address': "test api",
        'email': "test_api@a.ru",
        'password': '123'
    }).json())
    print(get('http://localhost:8080/api/users/7').json())


def test_api_2():
    print(get('http://localhost:8080/api/v2/users').json())  # получение всех пользователей
    print(get('http://localhost:8080/api/v2/users/1').json())  # получение одного существующего пользователя
    print(get('http://localhost:8080/api/v2/users/404').json())  # получение несуществующего пользователя

    # print(get('http://localhost:8080/api/v2/jobs').json())  # получение всех работ
    # print(get('http://localhost:8080/api/v2/jobs/3').json())  # получение существующей работы
    # print(get('http://localhost:8080/api/v2/jobs/404').json())  # получение существующей работы

    print(post('http://localhost:8080/api/v2/users', json={
        'surname': "test_api_v2",
        'name': "test_api_v2",
        'age': 2,
        'position': "test_api_v2",
        'speciality': "test_api_v2",
        'address': "test_api_v2",
        'email': "test_api_v2@a.ru",
        'hashed_password': '123'
    }).json())
    print(put('http://localhost:8080/api/v2/users/10', json={
        'surname': "test_api_v2222",
        'name': "put method v2",
        'age': 15,
        'position': "test api",
        'speciality': "test api",
        'address': "test api",
        'email': "test_api@a.ru",
        'hashed_password': '123'
    }).json())

    print(delete('http://localhost:8080/api/v2/users/10').json())  # удаление существующего пользователя
    print(delete('http://localhost:8080/api/v2/users/100').json())  # удаление несуществующего пользователя


def test_jobs_v2():
    print(get('http://localhost:8080/api/v2/jobs').json())  # получение всех работ
    print(get('http://localhost:8080/api/v2/jobs/3').json())  # получение существующей работы
    print(get('http://localhost:8080/api/v2/jobs/404').json())  # получение несуществующей работы

    print(post('http://localhost:8080/api/v2/jobs', json={'job': "v2",
                                                          'team_leader': 1,
                                                          'work_size': 12,
                                                          'collaborators': "1,2",
                                                          'is_finished': False}).json())  # создание новой работы
    print(put('http://localhost:8080/api/v2/jobs/12', json={'job': "API v2!!!!",
                                                            'team_leader': 1,
                                                            'work_size': 12,
                                                            'collaborators': "1,2",
                                                            'is_finished': True}).json())  # изменение существующей работы
    print(put('http://localhost:8080/api/v2/jobs/404', json={'job': "API v2!!!!",
                                                             'team_leader': 1,
                                                             'work_size': 12,
                                                             'collaborators': "1,2",
                                                             'is_finished': True}).json())  # изменение несуществующей работы

    print(delete('http://localhost:8080/api/v2/jobs/12').json())  # удаление существующей работы
    print(delete('http://localhost:8080/api/v2/jobs/404').json())  # удаление несуществующей работы


test_jobs_v2()
