from flask import jsonify
from flask import jsonify, request
from flask_jwt_simple import create_jwt

from pymodm.errors import DoesNotExist
from pymodm import connect

from segment import segment
from database import(login_user,
                     get_current_image,
                     get_orig_image,                     save_orig_image_uuid,
                     save_current_image_uuid,
                     remove_images)
from convert import save_image, get_image_by_uuid, get_image_as_b64


def act_login(req):
    """Authenticates login with email

    : param req: json request from client
    """
    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    # check if user exists and the password is correct
    if login_user(username, password):
        res = {'jwt': create_jwt(identity=username)}
        return jsonify(res), 200

    return jsonify({'error': 'username or password is incorrect'}), 400


def act_upload(req):
    """Uploads user image
        :param req: request from client
    """
    img_str = req['file']
    user = req['username']

    uuid = save_image(img_str)
    if uuid is None:
        return (jsonify({'error': 'Error saving image'}), 400)

    remove_images(user)
    save_orig_image_uuid(user, uuid)
    return (jsonify({'fileID': uuid}), 200)


def act_process(req):
    """Processes image that has already been uploaded

    :param req: request from client
    """
    print('process')

    user = req['username']
    uuid = get_orig_image(user)
    if uuid is None:
        return (jsonify({'error': 'Image not found'}), 400)
    newUuid = segment(uuid)
    save_current_image_uuid(user, newUuid)
    return (jsonify({'fileID': newUuid}), 200)


def act_download(req):
    '''Processes download request

    :param req: json request from client
    '''
    user = req['username']
    uuid = get_current_image(user)
    filetype = req['filetype']
    img_str = get_image_as_b64(uuid, filetype=filetype)
    return (jsonify({'file': img_str}), 200)
