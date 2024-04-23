from marshmallow import Schema, fields


class ToolModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    tool = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
