from marshmallow import Schema, fields
from collections import OrderedDict


class LikeSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    recipe_id = fields.Integer()


class RateSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    recipe_id = fields.Integer()
    value = fields.Integer(required=True)


class RateSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    recipe_id = fields.Integer()
    message = fields.String()
