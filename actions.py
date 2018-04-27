from flask import jsonify
from model import User
from pymodm.errors import DoesNotExist
from pymodm import connect
import logging
from database.py import get_image()
from segment import segment
import scipy.io
import matplotlib
import model

connect("mongodb://localhost:27017/database")


def act_login(req):
    """Authenticates login with email

        :param req: json request from client
    """
    email = req['email']

    try:
        user = User.objects.raw({'_id': email}).first()
    except DoesNotExist:
        logging.exception('User does not exist.')
        res = {
            'email': email,
            'login_success': False,
            'error': 'User does not exist'
        }
        return (jsonify(res), 400)

    return jsonify({'email': email, 'login_success': True})


def act_upload(req):
    """Uploads user image and processes image

        :param req: .mat file from client
    """
    matfile = req['matfile']
    segment(matfile)
    pass



def act_download(req):
    '''Processes download request

    :param req: json request from client
    '''
    img_str = get_image()
    filetype = req['filetype']
    return jsonify({'image': img_str, 'filetype': filetype})
