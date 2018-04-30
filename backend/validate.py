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
        'filetype': {
            'type': 'string'
        }
    },
    'required': ['username', 'filetype'],
    'additionalProperties': False
}


def val_login(input):
    try:
        validate(input, login_format)
        return True
    except ValidationError:
        return False


def val_upload(input):
    try:
        validate(input, upload_format)
        return True
    except ValidationError:
        return False


def val_process(input):
    try:
        validate(input, process_format)
        return True
    except (ValueError, ValidationError):
        return False


def val_download(input):
    try:
        validate(input, download_format)
        return True
    except ValidationError:
        return False
