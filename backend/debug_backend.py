import requests
import base64

test_img = 'exampleImages/tower.jpg'
un = 'test@mail.com'
pw = '12345'
baseURL = 'http://localhost:5000/'


def main():
    headers = login(un, pw)
    upload(headers, un, test_img)
    process(headers, un)
    download(headers, un, 'jpeg')


def read_image(path):
    with open(path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()


def login(username, password):
    body = {
        'username': username,
        'password': password
    }
    r = requests.post(baseURL + 'login', json=body)
    jwt = r.json()['jwt']

    __headers__ = {
        'authorization': 'Bearer ' + jwt,
        'content-type': 'application/json',
    }
    return __headers__


def upload(headers, username, test_img):
    body = {
        'username': username,
        'file': 'data:image/png;base64,' + read_image(test_img)
    }
    r = requests.post(baseURL + 'upload', headers=headers, json=body)
    originalID = r.json()['fileID']


def process(headers, username):
    body = {
        'username': username
    }
    r = requests.post(baseURL + 'process', headers=headers, json=body)
    newID = r.json()['fileID']


def download(headers, username, img_format):
    body = {
        'username': username,
        'filetype': img_format
    }
    r = requests.post(baseURL + 'download', headers=headers, json=body)
    data = r.json()['file']
    with open('exampleImages/temp.{}'.format(img_format), 'wb') as f:
        f.write(base64.decodebytes(data.encode()))


if __name__ == '__main__':
    main()
