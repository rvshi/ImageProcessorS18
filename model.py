from pymodm import fields, MongoModel


class User(MongoModel):
        email = fields.EmailField(primary_key=True)
        password = fields.CharField()
        origImageLink = fields.URLField()
        currentImageLink = fields.URLField()
