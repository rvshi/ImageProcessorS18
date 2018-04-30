import os
from pymodm import fields, MongoModel, connect
from pymodm.errors import DoesNotExist
from passlib.hash import pbkdf2_sha256

connect("mongodb://localhost:27017/database")


class User(MongoModel):
    email = fields.EmailField(primary_key=True)
    password = fields.CharField()
    orig_image = fields.CharField()  # original image
    curr_image = fields.CharField()


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


def save_orig_image_uuid(username, uuid):
    try:
        user = User.objects.raw({'_id': username}).first()
        user.orig_image = uuid
        user.save()
    except DoesNotExist:
        return None


def save_current_image_uuid(username, uuid):
    try:
        user = User.objects.raw({'_id': username}).first()
        user.curr_image = uuid
        user.save()
    except DoesNotExist:
        return None


def get_orig_image(username):
    try:
        user = User.objects.raw({'_id': username}).first()
        return user.orig_image
    except DoesNotExist:
        return None


def get_current_image(username):
    try:
        user = User.objects.raw({'_id': username}).first()
        return user.curr_image
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
        if user.orig_image is not None:
            delete_image(user.orig_image)
        if user.curr_image is not None:
            delete_image(user.curr_image)
        return True
    except DoesNotExist:
        return False
