from flask import jsonify
from flask import jsonify, request
from flask_jwt_simple import create_jwt

from pymodm.errors import DoesNotExist
from pymodm import connect

from segment import segment
from database import(login_user,
                     get_processed_image,
                     get_original_image, save_original_image_uuid,
                     save_processed_image_uuid,
                     remove_images)
from images import save_image, get_image_by_uuid, get_image_as_b64


def act_login(req):
    """Authenticates login with email and password

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


def act_list(username):
    """Lists the original and processed images for a user

    :param username: client username
    """
    return(jsonify({
        'originalID': get_original_image(username),
        'processedID': get_processed_image(username)
    }), 200)


def act_upload(req):
    """Uploads original user image

    :param req: request from client
    """
    params = request.get_json()
    username = params.get('username', None)
    file = params.get('file', None)

    uuid = save_image(file)
    if uuid is None:
        return (jsonify({'error': 'Error saving image'}), 400)

    remove_images(username)
    save_original_image_uuid(username, uuid)
    return (jsonify({'fileID': uuid}), 200)


def act_process(req):
    """Processes the original image that has been uploaded

    :param req: request from client
    """

    username = request.get_json().get('username', None)

    uuid = get_original_image(username)
    if uuid is None:
        return (jsonify({'error': 'Original image not found'}), 400)
    newUuid = segment(uuid)
    save_processed_image_uuid(username, newUuid)
    return (jsonify({'fileID': newUuid}), 200)


def act_download(req):
    '''Handles download request for images

    :param req: json request from client
    '''
    params = request.get_json()
    fileID = params.get('fileID', None)
    filetype = params.get('filetype', None)

    if fileID is None:
        return (jsonify({'error': 'Processed image not found'}), 400)
    img_str = get_image_as_b64(fileID, filetype=filetype)
    return (jsonify({'file': img_str}), 200)
