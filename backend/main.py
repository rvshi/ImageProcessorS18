"""Main Flask app module with endpoints and authentication.

"""
from flask import Flask, request, jsonify
from flask_jwt_simple import (
    JWTManager, jwt_required, get_jwt_identity
)
from flask_cors import CORS
from validate import val_login, val_upload, val_process, val_download
from actions import (act_login, act_list, act_upload,
                     act_process, act_download)
from secret_key import SECRET_KEY

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)
CORS(app)


def handler(input, validator, action):
    """Handles API requests

        :param input: input data from request
        :param validator: validator function to use
        :param action: database function to apply to data
        :returns: jsonified response
    """
    if not request.is_json:
        return jsonify({"error": "JSON missing"}), 400
    elif(not validator(input)):
        return jsonify({'error': 'Request was incorrectly formatted.'}), 400
    else:
        (response, code) = action(input)
        return response, code


@app.route('/login', methods=['POST'])
def login_handler():
    r = request.get_json()
    return handler(r, val_login, act_login)


@app.route("/validate", methods=["GET"])
@jwt_required
def validate_handler():
    return jsonify({"username": get_jwt_identity()}), 200


@app.route("/list", methods=["GET"])
@jwt_required
def list_handler():
    return act_list(get_jwt_identity())


@app.route("/upload", methods=["POST"])
@jwt_required
def upload_handler():
    r = request.get_json()
    return handler(r, val_upload, act_upload)


@app.route("/process", methods=["POST"])
@jwt_required
def process_handler():
    r = request.get_json()
    return handler(r, val_process, act_process)


@app.route("/download", methods=["POST"])
@jwt_required
def download_handler():
    r = request.get_json()
    return handler(r, val_download, act_download)
