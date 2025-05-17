from Config.DB.Models import User
from Config.DB.Schemas import UserSchema


class Tables:
    User = User


class Schemas:
    User = UserSchema()
    Users = UserSchema(many=True)
