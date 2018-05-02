"""Module for validating requests.

"""
from jsonschema import validate, ValidationError

# Regex from http://usernameregex.com
email_type = {
    'type': 'string',
    'pattern': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
}

login_format = {
    'type': 'object',
    'properties': {
        'username': email_type,
        'password': {
            'type': 'string'
        },
    },
    'required': ['username'],
    'additionalProperties': False
}

upload_format = {
    'type': 'object',
    'properties': {
        'username': email_type,
        'file': {
            'binaryEncoding': 'base64'
        }
    },
    'required': ['username', 'file'],
    'additionalProperties': False
}

process_format = {
    'type': 'object',
    'properties': {
        'username': email_type
    },
    'required': ['username'],
    'additionalProperties': False
}

download_format = {
    'type': 'object',
    'properties': {
        'username': email_type,
        'fileID': {
            'type': 'string'
        },
        'filetype': {
            'type': 'string'
        }
    },
    'required': ['username', 'fileID', 'filetype'],
    'additionalProperties': False
}


def val_wrapper(input, schema_format):
    """Validation endpoints

        :param input: input json data from request
        :param schema_format: schema format to use
        :returns: validation true or false
    """
    try:
        validate(input, schema_format)
        return True
    except ValidationError:
        return False


def val_login(input):
    """Validate login format for username and password

        :param input: input json data from user request
        :return: validation true or false
    """
    return val_wrapper(input, login_format)


def val_upload(input):
    """Validate upload format for username and b64 image file

        :param input: input json data from user request
        :return: validation true or false
    """
    return val_wrapper(input, upload_format)


def val_process(input):
    """Validate process format for username

        :param input: input json data from user request
        :return: validation true or false
    """
    return val_wrapper(input, process_format)


def val_download(input):
    """Validate download format for username and image uuid

        :param input: input json data from user request
        :return: validation true or false
    """
    return val_wrapper(input, download_format)
