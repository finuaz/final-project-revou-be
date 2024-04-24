from marshmallow import Schema, fields


class UserSocialsSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    facebook = fields.String()
    instagram = fields.String()
    tiktok = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class UserFacebookSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    facebook = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class UserInstagramSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    instagram = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class UserTiktokSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    tiktok = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
