from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)


@app.route("/upload", methods=["POST"])
def upload():
    r = request.get_json()
    username = r["username"]
    if not validate_whitelist_email(username):
        res = {
            "Message": "Username is not valid"
        }
        code = 400
    elif not validate_image_format(r['file']):
        res = {
            "Message": "Image is not in the correct format. It must be a JPEG, PNG, or TIFF file"
        }
        code = 400
    else:
        file = r['file']
        fileID = upload_to_server(username, file)
        res = {
            "Message": "Image {} successfully added to database".format(fileID)
        }
        code = 200
    return jsonify(res), code


@app.route("/process", methods=["POST"])
def process():
    r = request.get_json()
    username = r["username"]
    if not validate_whitelist_email(username):
        res = {
            "Message": "Username is not valid"
        }
        code = 400
    else:
        fileID = r['fileID']
        processedfile = segment_image(username, fileID)
        res = {
            "Message": "Image successfully processed",
        }
        code = 200
    return jsonify(res), code
