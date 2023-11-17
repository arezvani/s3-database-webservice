from werkzeug.wrappers import response
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, request, jsonify, make_response, g, session
from flask_session import Session
import psycopg2
from psycopg2 import Error, pool
import json
from datetime import timedelta
# import bcrypt
import sys
sys.path.append('../')
import config

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_FILE_THRESHOLD'] = 250   # 500 is default
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=10)
Session(app)

app.config['db_pool'] = db_pool = psycopg2.pool.ThreadedConnectionPool(
                                    minconn= 5,
                                    maxconn = 100,
                                    host = config.db_host,
                                    port = config.db_port,
                                    database = config.db_database,
                                    user = config.db_username,
                                    password = config.db_password
                        )


def get_information(uuid):
    cursor = g.db.cursor()
    cursor.execute("SELECT * FROM persons_information WHERE uuid=%s", [uuid])
    if cursor is not None:
        row = cursor.fetchone()
        data = {}
        for i, value in enumerate(row):
            key = cursor.description[i][0]
            if key == 'register_date':
                value = value.strftime("%Y-%m-%dT%H:%M:%S")
            data[key] = value

    return data

@app.before_request
def get_db():
    if 'db' not in g:
        g.db = app.config['db_pool'].getconn()

@app.teardown_appcontext
def close_conn(e):
    db = g.pop('db', None)
    if db is not None:
        app.config['db_pool'].putconn(db)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
            information = get_information(session['uuid'])
            response_dict = {'response': 'You have been logged in', 'information': information}
            response = make_response(jsonify(response_dict), 200)
            return response
    elif request.method == 'GET':
            response_dict = {'response': 'Please login with POST method'}
            response = make_response(jsonify(response_dict), 403)
            return response
    elif request.method == 'POST':
        request_dict = request.get_json()
        username = request_dict['username']
        usr_entered = request_dict['password']

        cursor = g.db.cursor()
        cursor.execute("SELECT * FROM persons_auth WHERE username =%s or email=%s", [username, username])
        if cursor is not None:
            row = cursor.fetchone()
            data = {}
            for i, value in enumerate(row):
                key = cursor.description[i][0]
                data[key] = value
                
            try:
                password = data['password']
                password_hash = generate_password_hash(password)

            except Exception:
                response_dict = {'response': 'Invalid Username or Password'}
                response = make_response(jsonify(response_dict), 401)
                return response
            
            # if bcrypt.checkpw(usr_entered.encode('utf-8'),password.encode('utf-8')):
            if check_password_hash(password_hash, usr_entered):
                app.logger.info('Password Matched')
                session['logged_in'] = True
                session['username'] = username
                session['uuid'] = data['uuid']

                information = get_information(session['uuid'])
                response_dict = {'response': 'You are now logged in', 'information': information}
                response = make_response(jsonify(response_dict), 200)
                cursor.close()
                return response

            else:
                response_dict = {'response': 'Invalid Username or Password'}
                response = make_response(jsonify(response_dict), 401)
                return response