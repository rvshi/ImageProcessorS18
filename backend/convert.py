import base64
import numpy as np
from PIL import Image
from mimetypes import guess_extension
from uuid import uuid4
import re
import os
from io import BytesIO


def save_image(img_str):
    '''Converts image string to binary and saves onto drive

    :param img_str: base64 image string
    :return uuid: UUID4 of image'''

    uuid = uuid4().hex
    str_parts = img_str.split(',')

    if(len(str_parts) == 2):
        img_type = str_parts[0]
        img_raw = str_parts[1]

        try:
            extension = re.search('data:image/(.+);', img_type).group(1)
        except AttributeError:  # no match found
            return None

        with open('images/{}.{}'.format(uuid, extension), 'wb') as f:
            f.write(base64.b64decode(img_raw))
            return uuid

    return None


def get_image_by_uuid(uuid):
    '''Converts image base64 string to uint array, saves intermediate image
    file to server

    :param img_str: base64 image string
    :param uuid: UUID of image to save
    :return data: grayscale image array
    '''

    for f in os.listdir('images/'):
        if re.match(uuid, f):
            im = Image.open('images/' + f)
            im = im.convert('L')
            im_arr = np.asarray(im)
            return im_arr

    return None


def save_image_from_arr(img_arr):
    '''Converts uint array to png file (intermediary format stored on server)

    :param img_arr: uint array
    :return uuid: uuid of converted image'''

    uuid = uuid4().hex
    img = Image.fromarray(img_arr)
    img.save('images/{}.png'.format(uuid), 'PNG')
    return uuid


def get_image_as_b64(uuid, filetype='png'):
    '''Gets b64 image string by uuid

    :param uuid: uuid of image
    :param filetype: file type to output, options are jpeg, png, or gif
    :return: b64 string of image
    '''

    filetype = filetype.lower()
    img_format = None
    if filetype == 'png':
        img_format = 'PNG'
    elif filetype == 'jpeg' or filetype == 'jpg':
        img_format = 'JPEG'
    elif filetype == 'gif':
        img_format = 'GIF'
    else:
        return None  # error, incorrect file type

    # convert file to desired type
    output = BytesIO()
    image = Image.open('images/{}.png'.format(uuid))
    image.save(output, format=img_format)
    contents = base64.b64encode(output.getvalue()).decode()
    output.close()
    return contents
