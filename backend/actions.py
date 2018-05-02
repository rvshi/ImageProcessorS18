"""Module for handling requests.

"""
from flask import jsonify
from flask_jwt_simple import create_jwt

from pymodm.errors import DoesNotExist
from pymodm import connect

from segment import segment
from database import (login_user, get_processed_image, get_original_image,
                      save_original_image_uuid, save_processed_image_uuid,
                      remove_images)
from images import save_image, get_image_by_uuid, get_image_as_b64
import logging
from logging_config import config


logging.basicConfig(**config)
logger = logging.getLogger(__name__)


def act_login(request):
    """Authenticates login with email and password

        :param request: json request from client
        :returns: json of jwt
    """

    username = request.get('username', None)
    password = request.get('password', None)

    # check if user exists and the password is correct
    if login_user(username, password):
        res = {'jwt': create_jwt(identity=username)}
        return jsonify(res), 200

    return jsonify({'error': 'username or password is incorrect'}), 400


def act_list(username):
    """Lists the original and processed images for a user

        :param username: client username
        :returns: json including uuid's of original and processed images
    """
    return (jsonify({
        'originalID': get_original_image(username),
        'processedID': get_processed_image(username)
    }), 200)


def act_upload(request):
    """Uploads original user image

        :param request: request from client
        :returns: uuid of uploaded image
    """

    username = request.get('username', None)
    file = request.get('file', None)

    uuid = save_image(file)
    if uuid is None:
        logger.error('No image saved, uuid {0} is invalid'.format(uuid))
        return jsonify({'error': 'Error saving image'}), 400

    remove_images(username)
    save_original_image_uuid(username, uuid)
    return jsonify({'fileID': uuid}), 200


def act_process(request):
    """Processes the original image that has been uploaded

        :param request: request from client
        :returns: uuid of processed image
    """

    username = request.get('username', None)

    uuid = get_original_image(username)
    if uuid is None:
        logger.error('No image processed, uuid {0} is invalid'.format(uuid))
        return jsonify({'error': 'Original image not found'}), 400
    newUuid = segment(uuid)
    save_processed_image_uuid(username, newUuid)
    logger.debug('New processed image with uuid {0} saved'.format(newUuid))
    return jsonify({'fileID': newUuid}), 200


def act_download(request):
    """Handles download request for images

        :param request: json request from client
        :returns: b64 image string of processed image
    """

    fileID = request.get('fileID', None)
    filetype = request.get('filetype', None)

    if fileID is None:
        logger.error('No image downloaded, uuid {0} is invalid'
                     .format(fileID))
        return jsonify({'error': 'Processed image not found'}), 400
    img_str = get_image_as_b64(fileID, filetype=filetype)
    logger.debug('New image with uuid {0} and filetype {1} downloaded'
                 .format(fileID, filetype))
    return jsonify({'file': img_str}), 200
