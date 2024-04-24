from marshmallow import Schema, fields


class UserModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    reset_password_question = fields.String()
    reset_password_answer = fields.String()
    image = fields.String()
    role = fields.String()
    bio = fields.String()
    location = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    author_id = fields.Integer()
    title = fields.String()
    description = fields.String()
    cooktime = fields.String()
    complexity = fields.String()
    servings = fields.Integer()
    budget = fields.Decimal()
    instructions = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class CommentModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    recipe_id = fields.Integer()
    user_id = fields.Integer()
    message = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class ToolModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    tool = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class FollowingModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    follower_id = fields.Integer()
    followee_id = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class CategoryModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    category = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class OriginModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    origin = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class TypeModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class IngredientModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    ingredient = fields.String()
    unit = fields.String()
    calories_per_unit = fields.Decimal()
    fat_per_unit = fields.Decimal()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class LikeModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    recipe_id = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class NutritionModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    recipe_id = fields.Integer()
    serving_per_container = fields.Integer()
    serving_size = fields.String()
    calories = fields.Decimal()
    total_fat = fields.Decimal()
    total_carbohydrate = fields.Decimal()
    total_sugar = fields.Decimal()
    cholesterol = fields.Decimal()
    protein = fields.Decimal()
    vitamin_d = fields.Decimal()
    sodium = fields.Decimal()
    calcium = fields.Decimal()
    potassium = fields.Decimal()
    iron = fields.Decimal()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RateModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    recipe_id = fields.Integer()
    value = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class AttachmentModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    recipe_id = fields.Integer()
    attachment_link = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeCategoryRelationModelSchema(Schema):
    id = fields.Integer(dump_only=True)
    recipe_id = fields.Integer()
    category_id = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeIngredientRelationModelSchema(Schema):
    id = fields.Integer()
    recipe_id = fields.Integer()
    ingredient_id = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeOriginRelationModelSchema(Schema):
    id = fields.Integer()
    recipe_id = fields.Integer()
    origin_id = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeTagRelationModelSchema(Schema):
    id = fields.Integer()
    recipe_id = fields.Integer()
    tag_id = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeToolRelationModelSchema(Schema):
    id = fields.Integer()
    recipe_id = fields.Integer()
    tool_id = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class RecipeTypeRelationModelSchema(Schema):
    id = fields.Integer()
    recipe_id = fields.Integer()
    type_id = fields.Integer()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class SocialModelSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    phone = fields.String()
    facebook = fields.String()
    instagram = fields.String()
    tiktok = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")


class TagModelSchema(Schema):
    id = fields.Integer()
    tagname = fields.String()
    created_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = fields.Str(dump_only=True, format="%Y-%m-%d %H:%M:%S")
