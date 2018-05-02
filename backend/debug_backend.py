import requests
import base64
import logging
from logging_config import config


logging.basicConfig(**config)
logger = logging.getLogger(__name__)

baseURL = 'http://localhost:5000/'

test_img = 'exampleImages/cornea.png'
filetype = 'png'

un = 'ed.l.1324@gmail.com'
pw = 'bme590'


def main():
    headers = login(un, pw)
    logger.debug('Prior to processing, list of images for {0}: {1}'
                 .format(un, _list(headers, un)))
    # print(_list(headers, un))
    origID = upload(headers, un, test_img)
    procID = process(headers, un)
    download(headers, un, procID, filetype)
    logger.debug('After processing, list of images for {0}: {1}'
                 .format(un, _list(headers, un)))
    # print(_list(headers, un))


def read_image(path):
    with open(path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()


def login(username, password):
    body = {
        'username': username,
        'password': password
    }
    r = requests.post(baseURL + 'login', json=body)
    logger.debug('login response: {0}'.format(r.json()))
    # print(r.json())
    jwt = r.json()['jwt']

    __headers__ = {
        'authorization': 'Bearer ' + jwt,
        'content-type': 'application/json',
    }
    return __headers__


def _list(headers, username):
    r = requests.get(baseURL + 'list', headers=headers)
    return r.text


def upload(headers, username, test_img):
    body = {
        'username': username,
        'file': 'data:image/png;base64,' + read_image(test_img)
    }
    r = requests.post(baseURL + 'upload', headers=headers, json=body)
    logger.debug('original image uploaded. uuid: {0}'
                 .format(r.json()['fileID']))
    return r.json()['fileID']


def process(headers, username):
    body = {
        'username': username
    }
    r = requests.post(baseURL + 'process', headers=headers, json=body)
    logger.debug('processing image with uuid: {0}'
                 .format(r.json()['fileID']))
    return r.json()['fileID']


def download(headers, username, fileID, img_format):
    body = {
        'username': username,
        'fileID': fileID,
        'filetype': img_format
    }
    r = requests.post(baseURL + 'download', headers=headers, json=body)
    data = r.json()['file']
    with open('exampleImages/temp.{}'.format(img_format), 'wb') as f:
        f.write(base64.decodebytes(data.encode()))
    logger.debug('downloaded processed image with uuid: {0}'.format(r.json()['fileID']))


if __name__ == '__main__':
    main()
