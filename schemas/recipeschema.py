from marshmallow import Schema, fields


class RecipeSchema(Schema):
    id = fields.Integer(dump_only=True)
    author_id = fields.Integer()
    title = fields.String()
    description = fields.String()
    nutriscore = fields.Integer()
    cooktime = fields.String()
    complexity = fields.String()
    servings = fields.Integer()
    budget = fields.Decimal()
    instructions = fields.String()
    view_count = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    recipe_id = fields.Integer()
    attachment_link = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeInstructionSchema(Schema):
    id = fields.Integer(dump_only=True)
    order = fields.Integer()
    instruction = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
