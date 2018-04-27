from model import User
from pymodm import fields, MongoModel, connect
from pymodm.errors import DoesNotExist

connect("mongodb://localhost:27017/database")


class User(MongoModel):
    email = fields.EmailField(primary_key=True)
    password = fields.CharField()
