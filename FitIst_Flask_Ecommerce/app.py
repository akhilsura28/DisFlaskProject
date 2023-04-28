from flask import Flask, render_template, request
import sqlite3
import re

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        msg = ''

        email = request.form['usermail']
        password = request.form['pswd']

        if not email or not password:
            msg = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Please enter valid email'
        elif not len(password) > 6:
            msg = 'Your password should be more than 6 characters'

        if msg == '':
            with sqlite3.connect("database.db") as users:
                cursor = users.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE usermail = ? AND userpassword = ?", (email, password))
                user = cursor.fetchone()
                if user:
                    # session['user_id'] = user[0]
                    msg = 'Logged in successfully !'
                    return render_template('login.html', email=user[2])
                else:
                    msg = 'Incorrect username / password !'

        return render_template('login.html', error=msg, type='login')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('login.html', error='', type='register')

    msg = ''

    username = request.form['username']
    password = request.form['pswd']
    email = request.form['usermail']
    confirmpassword = request.form['confirmpswd']

    if not username or not email or not password or not confirmpassword:
        msg = 'Please fill out the form !'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        msg = 'Please enter valid email'
    elif not len(password) > 6:
        msg = 'Your password should be more than 6 characters'
    elif not password == confirmpassword:
        msg = 'password and confirm password should be same'

    if msg == '':
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE usermail = ?', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        else:
            cursor.execute(
                'INSERT INTO users (username, usermail, userpassword) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            return render_template('login.html', email=email, error='')

    return render_template('login.html', error=msg, type='register')


@app.route('/categories/<category>')
def categories(category):
    products = []
    print("fetching products for category: ", category)
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        if category == 'all':
            cursor.execute("SELECT * FROM products")
        else:
            cursor.execute(
                "SELECT * FROM products WHERE category = ?", (category,))
        products = cursor.fetchall()
    return render_template('categories.html', category=category, products=products)


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/checkout', methods=["GET", "POST"])
def checkout():
    if request.method == 'GET':
        return render_template('payment.html')
    else:
        return render_template('order_placed.html')


@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    else:
        search = request.form['search']
        products = []
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM products WHERE name LIKE ?", ('%'+search+'%',))
            products = cursor.fetchall()
        return render_template('search.html', products=products)
