from pymodm import fields, MongoModel, connect
from pymodm.errors import DoesNotExist
from passlib.hash import pbkdf2_sha256

connect("mongodb://localhost:27017/database")


class User(MongoModel):
    email = fields.EmailField(primary_key=True)
    password = fields.CharField()
    image = fields.CharField()  # the most recent image


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


def save_image(username, image_str):
    user = User.objects.raw({'_id': username}).first()
    user.update(
        {'$set': {'image': image_str}})


def get_image(username):
    try:
        user = User.objects.raw({'_id': username}).first()
        return user.image
    except DoesNotExist:
        pass

    return None
