from flask import Flask, jsonify, request
from flask_cors import CORS
from validate import val_upload, val_process, val_download
from actions import action_upload, action_process, action_download
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
        response = {
            'message': '[ERROR] input was incorrectly formatted.',
            'code': 400
        }
    else:
        response = action(input)
        code = 200
    return response, code


@app.route("/upload", methods=["POST"])
def upload():
    r = request.get_json()
    return handler(r, val_upload, action_upload)


@app.route("/process", methods=["POST"])
def process():
    r = request.get_json()
    return handler(r, val_process, action_process)


@app.route("/download", methods=["POST"])
def download():
    r = request.get_json()
    return handler(r, val_download, action_download)
