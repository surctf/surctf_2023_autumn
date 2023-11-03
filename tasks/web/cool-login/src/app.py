from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

flag = 'redacted'

db_config = {
    'user': 'root',
    'password': 'redacted',
    'host': 'mysql_container',
    'database': 'users_db',
}

def cool(username):
    return username + ' so cool'

def notcool(username):
    return username + ' so bad cool'

def uncool(username):
    return username.strip()[:-8]


def create_users_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


def add_user(username, password):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
    connection.commit()
    connection.close()


def get_user(username, password):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    connection.close()
    return user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if 'admin' in username:
            username = notcool(username)
        else:
            username = cool(username)
        user = get_user(username,password)
        if user:
            return render_template('register.html',status='Пользователь с таким именем уже существует!')
        add_user(username, password)
        return render_template('register.html',status='Регистрация успешна! Теперь вы можете войти.')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global flag
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(cool(username),password)
        if user and user['password'] == password:
            username = uncool(user['username'])
            if username == 'admin':
                return render_template('index.html', username=username, flag=flag)
            else:
                return render_template('index.html', username=username)
        return render_template('login.html', status='Неверное имя пользователя или пароль.')
    return render_template('login.html')


if __name__ == '__main__':
    create_users_table()
    add_user('admin','admin')
    app.run(host='0.0.0.0', port=1337, debug=False)
