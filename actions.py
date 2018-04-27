from database import login_user
from flask import jsonify, request
from flask_jwt_simple import create_jwt


def act_login(req):
    '''Authenticates login with email

    : param req: json request from client
    '''
    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    # check if user exists and the password is correct
    if login_user(username, password):
        res = {'jwt': create_jwt(identity=username)}
        return jsonify(res), 200

    return jsonify({'error': 'username or password is incorrect'}), 400


def act_upload(req):
    pass


def act_process(req):
    pass


def act_download(req):
    pass
