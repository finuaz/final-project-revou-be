from marshmallow import Schema, fields


class RecipeSchema(Schema):
    id = fields.Integer(dump_only=True)
    author_id = fields.Integer()
    title = fields.String()
    description = fields.String()
    cooktime = fields.String()
    complexity = fields.String()
    servings = fields.Integer()
    budget = fields.Decimal()
    instructions = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
