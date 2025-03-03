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
            Вот она какая, красная планета.
        </p>

    </body>
    </html>"""


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
