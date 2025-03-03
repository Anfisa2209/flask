from flask import Flask, url_for

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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
