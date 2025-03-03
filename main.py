from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/')
def text():
    return """
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        <h1>Миссия Колонизация Марса</h1>
    </body>
    </html>"""


@app.route('/index')
def index():
    return """
            <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
            <h1>И на Марсе будут яблони цвести!</h1>
        </body>
        </html>"""


@app.route('/promotion')
def promotion():
    lines = ['Человечество вырастает из детства.',
             'Человечеству мала одна планета.',
             'Мы сделаем обитаемыми безжизненные пока планеты.',
             'И начнем с Марса!',
             'Присоединяйся!']
    return """
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        <h3>{}</h3>
        <h3>{}</h3>
        <h3>{}</h3>
        <h3>{}</h3>
        <h3>{}</h3>
    </body>
    </html>""".format(*lines)


@app.route('/image_mars')
def image():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Привет, Марс!</title>
    </head>
    <body>
        <h1>Жди нас, Марс!</h1>
        <img src="{url_for('static', filename='img/MARS.png')}" alt="картинка с Марсом">
        <p>
            Вот такая красивая планета.
        </p>

    </body>
    </html>"""


@app.route('/promotion_image')
def promotion_image():
    lines = ['Человечество вырастает из детства.',
             'Человечеству мала одна планета.',
             'Мы сделаем обитаемыми безжизненные пока планеты.',
             'И начнем с Марса!',
             'Присоединяйся!']
    url_style = url_for('static', filename='css/style.css')
    url_image = url_for('static', filename='img/MARS.png')
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Привет, Марс!</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link rel="stylesheet" type="text/css" href="{}">
</head>
<body>
    <h1>Жди нас, Марс!</h1>
    <img src={} alt="картинка с марсом">
    <div class="alert alert-primary" role="alert">
        <h3>{}</h3>
    </div>
    <div class="alert alert-secondary" role="alert">
      <h3>{}</h3>
    </div>
    <div class="alert alert-success" role="alert">
      <h3>{}</h3>
    </div>
    <div class="alert alert-danger" role="alert">
      <h3>{}</h3>
    </div>
    <div class="alert alert-warning" role="alert">
      <h3>{}</h3>
    </div>

</body>
</html>'''.format(url_style, url_image, *lines)


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    prof = sorted(i.capitalize() for i in
                  ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач', 'инженер по терраформированию',
                   'климатолог', 'специалист по радиационной защите'])
    if request.method == 'GET':
        return '''
        <!doctype html>
        <html lang="en">
            <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
            crossorigin="anonymous">
            <link rel="stylesheet" type="text/css" href="static/css/style.css"/>
            <title>Пример формы</title>
            </head>
            <body>
            <h1>Анекта претендента</h1>
            <h2>на участие в миссии</h2>
            <br>
            <div>
                <form class="login_form" method="post" enctype="multipart/form-data">
                    <input type="text" class="form-control" id="text" placeholder="Введите фамилию" name="second_name">
                    <br>
                    <input type="text" class="form-control" id="text" placeholder="Введите имя" name="first_name">
                    <br>
                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                    <br>
                    <div class="form-group">
                        <label for="classSelect">Какое у вас образование?</label>
                        <select class="form-control" id="classSelect" name="class">
                            <option>Общее образование</option>
                            <option>Профессиональное образование</option>
                            <option>Дополнительное образование</option>
                            <option>Профессиональное обучение</option>
                        </select>
                        </div>
                    <br>
                    <div class="form-group">
                        <label for="profession">Какие у вас профессии?</label><br>
                        <input class="form-check-input" type="checkbox" name="prof1" id="prof">
                        <label class="form-check-label" for="prof">{}</label><br>
                        <input class="form-check-input" type="checkbox" name="prof2" id="prof">
                        <label class="form-check-label" for="prof">{}</label><br>
                        <input class="form-check-input" type="checkbox" name="prof3" id="prof">
                        <label class="form-check-label" for="prof">{}</label><br>
                        <input class="form-check-input" type="checkbox" name="prof4" id="prof">
                        <label class="form-check-label" for="prof">{}</label><br>
                        <input class="form-check-input" type="checkbox" name="prof5" id="prof">
                        <label class="form-check-label" for="prof">{}</label><br>
                        <input class="form-check-input" type="checkbox" name="prof6" id="prof">
                        <label class="form-check-label" for="prof">{}</label><br>
                        <input class="form-check-input" type="checkbox" name="prof7" id="prof">
                        <label class="form-check-label" for="prof">{}</label><br>
                        <input class="form-check-input" type="checkbox" name="prof8" id="prof">
                        <label class="form-check-label" for="prof">{}</label>
                    </div>
                    <br>
                    <div class="form-group">
                        <label for="form-check">Укажите пол</label>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                            <label class="form-check-label" for="male">
                            Мужской
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                            <label class="form-check-label" for="female">
                            Женский
                            </label>
                        </div>
                    </div>
                    <br>
                    <div class="form-group">
                        <label for="about">Почему вы хотите принять участие в миссии?</label>
                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                    </div>
                    <br>
                    <div class="form-group">
                        <label for="photo">Приложите фотографию</label>
                        <br>
                        <input type="file" class="form-control-file" id="photo" name="file">
                    </div>
                    <div class="form-group form-check"><br>
                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                        <label class="form-check-label" for="acceptRules">Готовы остаться на Марсе?</label>
                    </div>
                    <br>
                    <button type="submit" class="btn btn-primary">Отправить</button>
                </form>
            </div>
            </body>
        </html>'''.format(*prof)
    elif request.method == 'POST':
        get_items = ['second_name', 'first_name', 'email', *[f'prof{i + 1}' for i in range(len(prof))], 'sex',
                     'about', 'file', 'accept']
        for item in get_items:
            print(request.form.get(item))
        return "Форма отправлена"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
