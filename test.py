from requests import get, put

print(put('http://localhost:8080/api/jobs/3', json={  # неполный запрос
    'job': 'Купить сок',
    'team_leader': 2,
    'collaborators': '1',
}).json())
print(put('http://localhost:8080/api/jobs/88', json={  # несуществующая работа
    'job': 'Купить сок',
    'team_leader': 2,
    'collaborators': '1',
    'work_size': 12,
    'is_finished': False
}).json())
print(put('http://localhost:8080/api/jobs/11', json={  # правильный запрос
    'job': 'Купить сок',
    'team_leader': 2,
    'collaborators': '1',
    'work_size': 12,
    'is_finished': False}).json())
print(get('http://localhost:8080/api/jobs').json())
