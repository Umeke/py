from flask import Flask, request, jsonify, redirect, url_for, render_template,g, current_app as app, session
import sqlite3
app = Flask(__name__)
app.secret_key = "1234"
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap

def connect_db():
    sql = sqlite3.connect('./database.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db


@app.route('/usefullfiles')
def usefullfiles():
    return render_template('usefullfiles.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list', methods=['GET', 'POST'])
def list():
    db = get_db()
    cursor  = db.execute('select id, login, password  from users')
    print(123,cursor,123)
    users = cursor.fetchall()
    return render_template('user.html', **{'users': users})


@app.route('/news2')
def news2():
    return render_template('news2.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username, password  = request.form.get('username'),request.form.get('password')
        db =get_db()

        db.execute(f'insert into users (login, password) values ("{username}", "{password}")')
        db.commit()
        return render_template('index.html')
    return '''
            <form method="POST">
                <div><label>Username: <input = "text" name = "username"></label></div>
                <div><label>Password: <input = "text" name = "password"></label></div>
                <input type = "submit" value="Submit">
            </form>
            '''



@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']

        db = get_db()
        print(123, db, 123)
        cursor = db.execute('select id, login, password  from users')
        print(100,cursor,100)
        users = db.execute(f'select * from users where login="{username}"')
        user  = db.execute('SELECT * FROM users WHERE login = ?', (username,)).fetchone()
        password1 = db.execute('SELECT * FROM users WHERE password = ?', (password,)).fetchone()
        users = db.execute('SELECT * FROM users').fetchall()
        user_list = [dict(user) for user in users]
        users = cursor.fetchall()
        print(111,user_list,222)
        res="false"
        for item in user_list:
            if item['login'] == username and   item['password']:
                res="true"
                break
        #db.commit()
        #user = users.fetchall()[0]

        print(12,res,23)
        if res=="true":
            #session["login"]
            #print(1234,session["login"],1234)
            return redirect(url_for('test'))
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    return redirect(url_for('test'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/news1')
def news1():
    return render_template('news1.html')

# @app.route('/users')
# @login_required('')
# def list_users():
#     users = User.query.all()
#     return jsonify([user.username for user in users])

if __name__ == '__main__':
    app.run(debug=True)


