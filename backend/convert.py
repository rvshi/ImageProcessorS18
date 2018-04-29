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
    matches = re.match(img_str, 'data:(.*);.*?, (.*)')
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
