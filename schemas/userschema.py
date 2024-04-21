from marshmallow import Schema, fields


class UserRegisterSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    reset_password_question = fields.String(required=True)
    reset_password_answer = fields.String(required=True)
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class UserLoginSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    email = fields.String(required=False)
    password = fields.String(required=True, load_only=True)
