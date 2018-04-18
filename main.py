from flask import Flask, request, jsonify
from flask_cors import CORS
from validate import val_login, val_upload, val_process, val_download
from actions import act_login, act_upload, act_process, act_download
import datetime

app = Flask(__name__)
CORS(app)


def handler(input, validator, action):
    """Handles API endpoints

    :param input: input data from request
    :param validator: validator function to use
    :param action: database function to apply to data
    :return: jsonified response
    """

    if(not validator(input)):
        response = jsonify({
            'error': 'Request was incorrectly formatted.',
            'code': 400
        })
    else:
        (response, code) = action(input)
    return response, code


@app.route('/login', methods=['POST'])
def login(email):
    r = request.get_json()
    return handler(r, val_login, act_login)


@app.route("/upload", methods=["POST"])
def upload():
    r = request.get_json()
    return handler(r, val_upload, act_upload)


@app.route("/process", methods=["POST"])
def process():
    r = request.get_json()
    return handler(r, val_process, act_process)


@app.route("/download", methods=["POST"])
def download():
    r = request.get_json()
    return handler(r, val_download, act_download)
