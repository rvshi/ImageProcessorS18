import base64
import scipy.io as scio
import h5py
import numpy as np
from uuid import uuid4


def convert_image(img_str):
    '''Converts image from base64 to uint array

    :param img_str: Image in base64 string
    :returns img_arr: Image in uint array
    '''
    uuid = uuid4().hex
    filename = 'temp_{}.mat'.format(uuid)
    file = open(filename, 'w')
    file.write(base64.decode(img_str))
    file.close()

    data = None

    try:
        mat_content = scio.loadmat(filename)
        data = mat_content['data']
    except:
        f = h5py.File('test.mat')
        data = f['data']

    data = np.array(data)

    return data
