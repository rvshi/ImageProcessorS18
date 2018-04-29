from flask import jsonify
from flask import jsonify, request
from flask_jwt_simple import create_jwt

from pymodm.errors import DoesNotExist
from pymodm import connect

from segment import segment
from database import login_user, save_image, get_image

connect("mongodb://localhost:27017/database")


def act_login(req):
    """Authenticates login with email
        :param req: json request from client
    """
    params = req.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    # check if user exists and the password is correct
    if login_user(username, password):
        res = {'jwt': create_jwt(identity=username)}
        return jsonify(res), 200

    return jsonify({'error': 'username or password is incorrect'}), 400


def act_upload(req):
    """Uploads user image, processes image, and downloads the processed image
        :param req: json request from client
    """
    pass


def act_process(req):
    """Processes image that has already been uploaded
        :param req: json request from client
    """
    pass


def act_download(req):
    """Processes download request
        :param req: json request from client
    """
    img_str = get_image(req.username)
    filetype = req['filetype']i
    return jsonify({'image': img_str, 'filetype': filetype})