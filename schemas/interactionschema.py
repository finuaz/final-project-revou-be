from marshmallow import Schema, fields
from collections import OrderedDict


class LikeSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    recipe_id = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RateSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    recipe_id = fields.Integer()
    value = fields.Integer(required=True)
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
