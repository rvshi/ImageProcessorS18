import base64
import numpy as np
from PIL import Image
# from mimetypes import guess_extension
from uuid import uuid4
import re
import os
from io import BytesIO


def save_image(img_str):
    """Converts image string to binary and saves onto drive

        :param img_str: base64 image string
        :returns: uuid of image
    """
    uuid = uuid4().hex

    try:
        img_type, img_raw = split_img_str(img_str)
    except ValueError:
        return None

    try:
        extension = re.search('data:image/(.+);', img_type).group(1)
    except AttributeError:  # no match found
        return None

    with open('images/{}.png'.format(uuid, extension), 'wb') as f:
        print(img_raw)
        f.write(base64.b64decode(img_raw))
        return uuid

    return None


def split_img_str(img_str):
    '''Splits image string from frontend into metadata and b64 binary

    :param img_str: raw string from frontend
    :returns: tuple of image type and binary
    '''

    str_parts = img_str.split(',')

    if(len(str_parts) == 2):
        img_type = str_parts[0]
        img_raw = str_parts[1]
    else:
        raise ValueError('''Invalid image string input. String must contain both
                         metadata and base64 binary string''')

    return (img_type, img_raw)


def save_image_from_arr(img_arr):
    """Converts uint array to png file (intermediary format stored on server)

        :param img_arr: uint array of image
        :returns: uuid of image
    """
    uuid = uuid4().hex
    try:
        img = Image.fromarray(img_arr.astype('uint8'))
    except ValueError:
        return None

    img.save('images/{}.png'.format(uuid), 'PNG')
    return uuid


def get_image_by_uuid(uuid):
    """Retrieves uint array of image by its uuid

        :param uuid: UUID of image as string
        :returns: grayscale image array
    """
    for f in os.listdir('images/'):
        if re.match(uuid, f):
            im = Image.open('images/' + f)
            im = im.convert('L')
            im_arr = np.asarray(im)
            return im_arr

    return None


def get_image_as_b64(uuid, filetype='png'):
    """Gets b64 image string by uuid

        :param uuid: uuid of image
        :param filetype: file type to output, options are jpeg, png, or gif
        :returns: b64 string of image
    """

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

    for f in os.listdir('images/'):
        if f.startswith(uuid):
            output = BytesIO()
            image = Image.open('images/' + f.format(uuid))

            # handle transparent images
            if image.mode in ('RGBA', 'LA'):
                background = Image.new(image.mode[:-1], image.size, '#fff')
                background.paste(image, image.split()[-1])
                image = background

            image.save(output, format=img_format)
            contents = base64.b64encode(output.getvalue()).decode()
            output.close()
    return contents
