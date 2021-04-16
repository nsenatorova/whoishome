from flask import Flask, Response, jsonify, request, abort, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import smtplib


app = Flask(__name__)

app.secret_key = 'my secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'iot'

mysql = MySQL(app)

neighbours = [
    {
        'name': u'sosed1',
        'is_in_home': False
    },
    {
        'name': u'sosed',
        'is_in_home': False
    }
]


@app.route('/neighbours', methods=['GET'])
def get_neighbours():
    return jsonify({'neighbours': neighbours})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not request.json:
        abort(404)
    if request.method == 'POST':
        jdata = request.get_json()
        email = str(jdata['email'])
        device_id = int(jdata['id'])
        pword = str(jdata['password'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            abort(400)
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, % s, % s)', (device_id, email, pword,))
            mysql.connection.commit()
            neighbour = {
                'name': email,
                'is_in_home': True
            }
            neighbours.append(neighbour)
            smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
            smtpObj.starttls()
            smtpObj.login('iot-project@mail.ru', 'ktTusOUoT11_')
            smtpObj.sendmail("iot-project@mail.ru", email, "fuck you")
            smtpObj.quit()
            response = Response(status=201)
            return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        jdata = request.get_json()
        email = str(jdata['email'])
        password = str(jdata['password'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s AND pword = % s', (email, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['email']
            response = Response(status=201)
            return response
        else:
            abort(400)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    response = Response(status=201)
    return response


@app.route('/trigger')
def smt():
    response = Response(status=200)
    return response


if __name__ == '__main__':
    app.run(debug=True)
