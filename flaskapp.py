from flask import Flask, Response, jsonify, request, abort, session, make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import smtplib
import json
from pyfcm import FCMNotification
import pytest

app = Flask(__name__)

app.secret_key = 'my secret key'

app.config['MYSQL_HOST'] = 'lemonl1me.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'lemonl1me'
app.config['MYSQL_PASSWORD'] = 'кщщекщще'
app.config['MYSQL_DB'] = 'lemonl1me$iotproj'
app.config[
    'FCM_KEY'] = 'AAAAXl9OE3A:APA91bGiT83Wx_WH4ihXtGqJytzKABejFGLngv2LCfhR54yCxDB9oVLzEQlozw7HO-GnMnUw6WoDCPzOmhxT7t560YTJM7QHeXCIfEHtSVFmPZaEd0D3wkSgGsCC_cqsWVqt6ha3Ug1J'

mysql = MySQL(app)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


@app.route('/neighbours', methods=['GET'])
def get_neighbours():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT device_id, email, is_in_home FROM accounts")
    rows = cursor.fetchall()
    print(rows)
    mysql.connection.commit()
    return jsonify({"neighbours": rows})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not request.json:
        abort(404)
    if request.method == 'POST':
        jdata = request.get_json()
        email = str(jdata['email'])
        device_id = int(jdata['id'])
        pword = str(jdata['password'])
        token = str(jdata['fcm_token'])
        is_in_home = True
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            abort(400)
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, % s, % s, %s, %s)',
                           (device_id, email, pword, is_in_home, token,))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM accounts WHERE email = % s', (email,))
            account = cursor.fetchone()
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['email']
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
        token = str(jdata['fcm_token'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s AND pword = % s', (email, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['email']
            device_id = str(account['device_id'])
            cursor.execute(
                'UPDATE accounts SET token=%s WHERE email= %s',
                (token, email))
            mysql.connection.commit()
            return make_response(device_id, 201)
        else:
            abort(400)


@app.route('/neighbours/<int:device_id>/<string:email>', methods=['GET'])
def get_room(device_id, email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT device_id, email, is_in_home FROM accounts WHERE email != % s", (email,))
    rows = cursor.fetchall()
    print(rows)
    mysql.connection.commit()
    neighbours = json.loads(json.dumps(rows))
    room = [x for x in neighbours if x['device_id'] == device_id]
    return jsonify({'neighbours': room})


@app.route('/update/<string:email_update>', methods=['PUT'])
def update_account(email_update):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    jdata = request.get_json()
    device_id = int(jdata['id'])
    email = str(jdata['email'])
    pword = str(jdata['password'])
    is_in_home = jdata['is_in_home']
    cursor.execute('SELECT * FROM accounts WHERE email = % s ', (email_update,))
    account = cursor.fetchone()
    if not account:
        abort(404)
    cursor.execute(
        'UPDATE accounts SET device_id=%s, pword=%s, is_in_home=%s WHERE email= %s',
        (device_id, pword, is_in_home, email_update))
    mysql.connection.commit()
    cursor.execute(
        'UPDATE accounts SET email=%s WHERE email= %s',
        (email, email_update))
    mysql.connection.commit()
    response = Response(status=201)
    return response


@app.route('/add', methods=['POST'])
def add_neighbour():
    jdata = request.get_json()
    user_email = str(jdata['user_email'])
    new_email = str(jdata['new_email'])
    smtpObj = smtplib.SMTP('smtp.gmail.ru', 587)
    smtpObj.starttls()
    smtpObj.login('whoishome.project@gmail.com', 'ghostcoolies')
    smtpObj.sendmail("whoishome.project@gmail.com", new_email,
                     "<user_email> приглашает зарегистрироваться в нашем приложении <3<3<3")
    smtpObj.quit()


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    response = Response(status=201)
    return response


@app.route('/trigger/<int:device_id>')
def smt(device_id):
    result = send_fcm(device_id)
    if result == 1:
        response = Response(status=200)
        return response
    else:
        response = Response(status=400)
        return response


def send_fcm(device_id, title=None, body=None, data_message=None):
    push_service = FCMNotification(api_key=app.config['FCM_KEY'])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT tokens FROM accounts WHERE device_id = % s ', (device_id,))
    tokens = cursor.fetchall()
    print(tokens)
    fcm_tokens = json.loads(json.dumps(tokens))
    title = "Что-то произошло"
    body = "Похоже, кто-то ушел"
    data = {
        "click_action": "FLUTTER_NOTIFICATION_CLICK",
        "amount": "300"
    }
    try:
        if type(fcm_tokens) is list:
            print(fcm_tokens, data_message)
            result = push_service.notify_multiple_devices(registration_ids=fcm_tokens, message_title=title,
                                                          message_body=body,
                                                          message_data=data)
            print(result, '++++++++++++++', flush=True)
            return 1
        else:
            print(fcm_tokens, 'single device', data_message)
            result = push_service.notify_single_device(registration_ids=fcm_tokens, message_title=title,
                                                       message_body=body,
                                                       message_data=data)
            print(result, flush=True)
            return 1
    except ValueError as e:
        return 0


if __name__ == '__main__':
    app.run(debug=True)
