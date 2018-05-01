import os
from pymodm import fields, MongoModel, connect
from pymodm.errors import DoesNotExist
from passlib.hash import pbkdf2_sha256

connect("mongodb://localhost:27017/database")


class User(MongoModel):
    username = fields.EmailField(primary_key=True)
    password = fields.CharField()
    original_image = fields.CharField()  # original image
    processed_image = fields.CharField()


def add_user(username, password):
    try:
        user = User.objects.raw({'_id': username}).first()
    except DoesNotExist:
        user = User(username, password=pbkdf2_sha256.hash(password))
        user.save()


def get_user(username):
    try:
        user = User.objects.raw({'_id': username}).first()
        return user
    except DoesNotExist:
        return None


def delete_user(username):
    try:
        user = User.objects.raw({'_id': username}).first()
        user.delete()
    except DoesNotExist:
        pass

    return False


def login_user(username, password):
    try:
        user = User.objects.raw({'_id': username}).first()
        if user.password and pbkdf2_sha256.verify(password, user.password):
            return True
    except DoesNotExist:
        pass

    return False


def save_original_image_uuid(username, uuid):
    try:
        user = User.objects.raw({'_id': username}).first()
        user.original_image = uuid
        user.save()
    except DoesNotExist:
        return None


def save_processed_image_uuid(username, uuid):
    try:
        user = User.objects.raw({'_id': username}).first()
        user.processed_image = uuid
        user.save()
    except DoesNotExist:
        return None


def get_original_image(username):
    try:
        user = User.objects.raw({'_id': username}).first()
        return user.original_image
    except DoesNotExist:
        return None


def get_processed_image(username):
    try:
        user = User.objects.raw({'_id': username}).first()
        return user.processed_image
    except DoesNotExist:
        return None


def delete_image(name):
    for f in os.listdir('images/'):
        if f.startswith(name):
            os.remove('images/' + f)
            return


def remove_images(username):
    try:
        user = User.objects.raw({'_id': username}).first()
        if user.original_image is not None:
            delete_image(user.original_image)
        if user.processed_image is not None:
            delete_image(user.processed_image)
        return True
    except DoesNotExist:
        return False
