"""Module for interacting with database.

"""

import os
from pymodm import fields, MongoModel, connect
from pymodm.errors import DoesNotExist
from passlib.hash import pbkdf2_sha256
import logging
from logging_config import config


logging.basicConfig(**config)
logger = logging.getLogger(__name__)

connect("mongodb://mongo:27017/database")


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
        logger.debug('New user added: username {0}'.format(username))


def get_user(username):
    """Gets user by unique username
        :param username: user email as string type which serves as user id
        :returns: user information
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        return user
    except DoesNotExist:
        logger.warning('User does not exist')
        return None


def delete_user(username):
    """Deletes user from mongo database
        :param username: user email as string type which serves as user id
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        user.delete()
        logger.debug('User ({0}) deleted'.format(username))
    except DoesNotExist:
        logger.warning('User does not exist, cannot be deleted')
        pass

    return False


def login_user(username, password):
    """Returns true if user exists and has the correct password
        :param username: user email as string type which serves as user id
        :param password: user password as string type
        :returns: True if password is correct, False if incorrect
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        if user.password and pbkdf2_sha256.verify(password, user.password):
            logger.info('Correct username and password. '
                        'Successful user login')
            return True
    except DoesNotExist:
        logger.warning('User does not exist')
        pass
    logger.debug('Incorrect Username or password. Login unsuccessful')
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
        logger.debug('Original image with uuid {0} saved'.format(uuid))
    except DoesNotExist:
        logger.warning('User does not exist')
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
        logger.debug('Processed image with uuid {0} saved'.format(uuid))
    except DoesNotExist:
        logger.warning('User does not exist')
        return None


def get_original_image(username):
    """Gets the original image uuid for a user
        :param username: user email as string type which serves as user id
        :returns: uuid of user's original image as a string
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        logger.debug('Retrieve original image uuid {0}'
                     .format(user.original_image))
        return user.original_image
    except DoesNotExist:
        logger.warning('User does not exist')
        return None


def get_processed_image(username):
    """Gets the processed image uuid for a user
        :param username: user email as string type which serves as user id
        :returns: uuid of user's processed image as a string
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        logger.debug('Retrieve processed image uuid {}'
                     .format(user.processed.image))
        return user.processed_image
    except DoesNotExist:
        logger.warning('User does not exist')
        return None


def delete_image(name):
    """Deletes image stored in server
        :param name: name (uuid) of an image stored in the VM server
    """
    for f in os.listdir('images/'):
        if f.startswith(name):
            os.remove('images/' + f)
            logger.debug('Image with uuid {} deleted'.format(name))
            return


def remove_images(username):
    """Removes all images associated with a user
        :param username: user email as string type which serves as user id
    """
    try:
        user = User.objects.raw({'_id': username}).first()
        if user.original_image is not None:
            delete_image(user.original_image)
            logger.debug('Original image with uuid {} removed'
                         .format(user.original_image))
        if user.processed_image is not None:
            delete_image(user.processed_image)
            logger.debug('Processed image with uuid {} removed'
                         .format(user.processed_image))
        return True
    except DoesNotExist:
        logger.warning('User does not exist')
        return False
