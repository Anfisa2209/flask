from requests import get, post, put, delete

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
    'password':'123'
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