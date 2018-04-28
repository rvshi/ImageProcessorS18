import base64
import scipy.io as scio
import h5py
import numpy as np
from uuid import uuid4
import os


def convert_image(img_str):
    '''Converts image base64 string to uint array

    :param img_str: base64 image string
    :return data: grayscale image array
    '''

    uuid = uuid4().hex
    filename = 'images/{}.mat'.format(uuid)
    file = open(filename, 'wb')
    file.write(base64.b64decode(img_str))
    file.close()

    data = None

    try:
        mat_content = scio.loadmat(filename)
        data = mat_content['I2']
    except NotImplementedError:
        f = h5py.File('test.mat')
        data = f['I2']

    data = np.array(data)
    os.remove(filename)

    return data
