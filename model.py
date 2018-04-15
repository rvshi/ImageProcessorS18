from pymodm import fields, MongoModel


class User(MongoModel):
        email = fields.EmailField(primary_key=True)
        password = fields.CharField()
        currentImage = fields.ImageField()
