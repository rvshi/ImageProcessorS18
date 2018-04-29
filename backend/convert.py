import base64
import numpy as np
from PIL import Image
from mimetypes import guess_extension
from uuid import uuid4
import re
import os


def save_image(img_str):
    '''Converts image string to binary and saves onto drive

    :param img_str: base64 image string
    :return uuid: UUID4 of image'''

    uuid = uuid4().hex
    img_str_esc = re.escape(img_str)
    matches = re.match('data:(.*);.*?,(.*)', img_str_esc)
    extension = guess_extension(matches[1])
    img = matches[2]
    filename = 'images/{}.{}'.format(uuid, extension)
    file = open(filename, 'wb')
    file.write(base64.b64decode(img))
    file.close()
    return uuid


def get_image_by_uuid(uuid):
    '''Converts image base64 string to uint array, saves intermediate image
    file to server

    :param img_str: base64 image string
    :param uuid: UUID of image to save
    :return data: grayscale image array
    '''

    for f in os.listdir('images/'):
        if re.match(uuid, f):
            im = Image.open(f)
            im_arr = np.asArray(im)
            return im_arr

    return None


def save_image_from_arr(img_arr):
    '''Converts uint array to png file

    :param img_arr: uint array
    :return uuid: uuid of converted image'''

    uuid = uuid4().hex
    img = Image.fromarray(img_arr)
    img.save('images/{}.png'.format(uuid))
    return uuid


def get_image_as_b64(uuid, filetype='png'):
    '''Gets b64 image by uuid

    :param uuid: uuid of image
    :return: b64 string of image
    '''

    extension = None
    if filetype == 'png':
        extension = 'png'
    elif filetype == 'jpeg':
        extension = 'jpg'

    filename = 'images/{}.{}'.format(uuid, extension)
    with open(filename, 'rb') as f:
        img_str = base64.b64encode(f.read())
        return img_str

    return None
