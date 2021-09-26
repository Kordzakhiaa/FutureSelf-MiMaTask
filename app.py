import json
import os
import datetime
from functools import wraps

import jwt
from flask import Flask, request, jsonify
from passlib.handlers.sha2_crypt import sha256_crypt

from validate_data import is_valid_email, is_valid_password, check_email, check_password
from send_mail import mail_to_myself

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecretKey'


def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing Token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid Token'}), 403
        return func(*args, *kwargs)

    return wrapped


@app.route('/login_required')
@login_required
def protected():
    return jsonify({'message': 'protected page:)'})


@app.route('/register', methods=['POST', 'GET'])
def register() -> jsonify:
    if request.method == 'POST':
        user_data: dict = request.form.to_dict()
        email: str = user_data['email']
        password1: str = user_data['password1']
        password2: str = user_data['password2']

        if is_valid_email(email):
            if is_valid_password(password1):
                if password1 == password2:
                    user_data['password1'] = sha256_crypt.hash(password1)
                    user_data.pop('password2')
                    filesize = os.path.getsize('user_data.json')

                    if filesize == 0:
                        data: list = [user_data]
                        with open('user_data.json', mode='w') as f:
                            f.write(json.dumps(data, indent=2))
                    else:
                        if check_email(email):
                            return jsonify({'message': 'mail is used'}), 400
                        with open('user_data.json') as feedsjson:
                            feeds: list = json.load(feedsjson)
                        feeds.append(user_data)
                        with open('user_data.json', mode='w') as f:
                            f.write(json.dumps(feeds, indent=2))
                else:
                    return jsonify({'message': 'bad request'}), 400
            return jsonify({'message': 'created'}), 201
        return jsonify({'message': 'bad request'}), 400
    return jsonify({'message': 'register page'}), 200


@app.route('/login', methods=['GET', 'POST'])
def login() -> jsonify:
    if request.method == 'POST':
        user_data: dict = request.form.to_dict()
        email: str = user_data['email']
        password: str = user_data['password']

        if check_email(email):
            if check_password(password):
                token = jwt.encode({
                    'user': email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
                },
                    app.config['SECRET_KEY'])
                return jsonify({'token': token.decode('utf-8')})
            return jsonify({'message': 'password is incorrect'}), 403
        return jsonify({'message': 'email is incorrect or not registered'}), 400
    return jsonify({'message': 'login page'}), 200


@app.route('/send_mail', methods=['POST', 'GET'])
@login_required
def send_email():
    if request.method == 'POST':
        user_data: dict = request.form.to_dict()
        email: str = user_data['email']
        password: str = user_data['password']
        title: str = user_data['title']
        body: str = user_data['body']

        mail_to_myself(email, password, title, body)

        return jsonify({'message': 'mail successfully sent'}), 201

    return jsonify({'message': 'send mail page'}), 200


if __name__ == '__main__':
    app.run(debug=True)
