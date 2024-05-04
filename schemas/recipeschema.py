from marshmallow import Schema, fields
from collections import OrderedDict


class RecipeSchema(Schema):
    id = fields.Integer(dump_only=True)
    author_id = fields.Integer()
    title = fields.String()
    description = fields.String()
    nutriscore = fields.Integer()
    cooktime = fields.Integer()
    complexity = fields.String()
    servings = fields.Integer()
    budget = fields.String()
    instruction = fields.String()
    view_count = fields.Integer()

    categories = fields.List(fields.String())
    type = fields.String()
    origin = fields.String()
    tags = fields.List(fields.String())

    attachment = fields.String()

    # Ingredient group
    ingredients = fields.List(fields.List(fields.String()))

    # Nutrition group
    serving_per_container = fields.Integer()
    serving_size = fields.String()

    calories = fields.Decimal(places=2, rounding=None)
    total_fat = fields.Decimal(places=2, rounding=None)
    total_carbohydrate = fields.Decimal(places=2, rounding=None)
    total_sugar = fields.Decimal(places=2, rounding=None)
    cholesterol = fields.Decimal(places=2, rounding=None)
    protein = fields.Decimal(places=2, rounding=None)
    vitamin_d = fields.Decimal(places=2, rounding=None)

    sodium = fields.Decimal(places=2, rounding=None)
    calcium = fields.Decimal(places=2, rounding=None)
    potassium = fields.Decimal(places=2, rounding=None)
    iron = fields.Decimal(places=2, rounding=None)

    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")

    # class Meta:
    #     ordered = True


class RecipePlusPlusSchema(Schema):
    id = fields.Integer(dump_only=True)
    author_id = fields.Integer()
    title = fields.String()
    description = fields.String()
    nutriscore = fields.Integer()
    cooktime = fields.Integer()
    complexity = fields.String()
    servings = fields.Integer()
    budget = fields.String()
    instruction = fields.String()
    view_count = fields.Integer()

    categories = fields.List(fields.String())
    type = fields.String()
    origin = fields.String()
    tags = fields.List(fields.String())

    attachment = fields.String()

    # Ingredient group
    ingredients = fields.List(fields.List(fields.String()))

    # Nutrition group
    serving_per_container = fields.Integer()
    serving_size = fields.String()

    calories = fields.Decimal(places=2, rounding=None)
    total_fat = fields.Decimal(places=2, rounding=None)
    total_carbohydrate = fields.Decimal(places=2, rounding=None)
    total_sugar = fields.Decimal(places=2, rounding=None)
    cholesterol = fields.Decimal(places=2, rounding=None)
    protein = fields.Decimal(places=2, rounding=None)
    vitamin_d = fields.Decimal(places=2, rounding=None)

    sodium = fields.Decimal(places=2, rounding=None)
    calcium = fields.Decimal(places=2, rounding=None)
    potassium = fields.Decimal(places=2, rounding=None)
    iron = fields.Decimal(places=2, rounding=None)

    likes = fields.Integer()
    rating = fields.Decimal(places=2, rounding=None)

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
