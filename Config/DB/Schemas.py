from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, ValidationError
from flask_marshmallow import Marshmallow
from Config.DB.Models import User

ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    # role = fields.Nested(UserRoleSchema, dump_only=True)
    # lab_accesses = fields.Nested(UserLabAccessSchema, many=True, dump_only=True)

    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        exclude = ["password"]


class UserForAISchema(ma.SQLAlchemyAutoSchema):
    # role = fields.Nested(UserRoleSchema, dump_only=True)
    # lab_accesses = fields.Nested(UserLabAccessSchema, many=True, dump_only=True)

    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        exclude = ["email", "password", "location_lat", "location_lng"]
