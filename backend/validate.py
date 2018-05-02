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
    'required': ['username', 'password'],
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
    try:
        validate(input, schema_format)
        return True
    except ValidationError:
        return False


def val_login(input):
    return val_wrapper(input, login_format)


def val_upload(input):
    return val_wrapper(input, upload_format)


def val_process(input):
    return val_wrapper(input, process_format)


def val_download(input):
    return val_wrapper(input, download_format)
