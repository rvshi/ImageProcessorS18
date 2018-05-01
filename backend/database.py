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
    """Creates new user if user does not exist in the mongo database

        :param username: user email as string type which serves as user id
        :param password: user password as string type
        :returns: updates user information in mongo database
    """
    try:
        user = User.objects.raw({'_id': username}).first()
    except DoesNotExist:
        user = User(username, password=pbkdf2_sha256.hash(password))
        user.save()


def get_user(username):
    """Gets user by unique username
        :param username: user email as string type which serves as user id
        :returns: user information
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        return user
    except DoesNotExist:
        return None


def delete_user(username):
    """Deletes user from mongo database
        :param username: user email as string type which serves as user id
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        user.delete()
    except DoesNotExist:
        pass

    return False


def login_user(username, password):
    """Returns true if user exists and has the correct password
        :param username: user email as string type which serves as user id
        :param password: user password as string type
        :returns: True if user has correct password, False if incorrect password
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        if user.password and pbkdf2_sha256.verify(password, user.password):
            return True
    except DoesNotExist:
        pass

    return False


def save_original_image_uuid(username, uuid):
    """Updates existing user by adding the uuid of a user-uploaded image
        :param username: user email as string type which serves as user id
        :param uuid: UUID4 of user-uploaded image
        :returns: adds uuid of user-uploaded image to mongo database
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        user.original_image = uuid
        user.save()
    except DoesNotExist:
        return None


def save_processed_image_uuid(username, uuid):
    """Updates existing user by adding the uuid of the processed image
        :param username: user email as string type which serves as user id
        :param uuid: UUID4 of processed image
        :returns: adds uuid of processed image to mongo database
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        user.processed_image = uuid
        user.save()
    except DoesNotExist:
        return None


def get_original_image(username):
    """Gets the original image uuid for a user
        :param username: user email as string type which serves as user id
        :returns: uuid of user's original image as a string
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        return user.original_image
    except DoesNotExist:
        return None


def get_processed_image(username):
    """Gets the processed image uuid for a user
        :param username: user email as string type which serves as user id
        :returns: uuid (UUID4) of user's processed image as a string
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        return user.processed_image
    except DoesNotExist:
        return None


def delete_image(name):
    """Deletes image stored in server
        :param name: name (uuid) of an image stored in the VM server
    """
    for f in os.listdir('images/'):
        if f.startswith(name):
            os.remove('images/' + f)
            return


def remove_images(username):
    """Removes all images associated with a user
        :param username: user email as string type which serves as user id
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        if user.original_image is not None:
            delete_image(user.original_image)
        if user.processed_image is not None:
            delete_image(user.processed_image)
        return True
    except DoesNotExist:
        return False
