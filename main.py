from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from model import User
from pymodm.errors import DoesNotExist
from pymodm import connect
import logging

app = Flask(__name__, static_url_path='/static')
CORS(app)

connect("mongodb://localhost:27017/database")


@app.route('/login', methods=['POST'])
def login(email):
    '''Authenticates login with email
    :param email: email'''

    try:
        user = User.objects.raw({'_id': email}).first()
    except DoesNotExist:
        logging.exception('User does not exist.')
        return 'User does not exist', 400

    return jsonify({email: email, login_success: True})
