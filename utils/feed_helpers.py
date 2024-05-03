from models import (
    RecipeModel,
    CategoryModel,
    TypeModel,
    OriginModel,
    TagModel,
    RecipeCategoryRelationModel,
    RecipeTypeRelationModel,
    RecipeOriginRelationModel,
    RecipeTagRelationModel,
)

from db import db


def find_all_category(recipe_id):
    recipe_category = RecipeCategoryRelationModel.query.filter_by(
        recipe_id=recipe_id
    ).all()
    if recipe_category:
        category = CategoryModel.query.get(recipe_category.category_id)
        return category.category
    else:
        return None


def find_all_type(recipe_id):
    recipe_type = RecipeTypeRelationModel.query.filter_by(recipe_id=recipe_id).all()
    if recipe_type:
        type = TypeModel.query.get(recipe_type.type_id)
        return type.type
    else:
        return None


def find_all_origin(recipe_id):
    recipe_origin = RecipeOriginRelationModel.query.filter_by(recipe_id=recipe_id).all()
    if recipe_origin:
        origin = OriginModel.query.get(recipe_origin.origin_id)
        print(origin)
        return origin.origin
    else:
        return None


def find_all_tag(recipe_id):
    recipe_tags = RecipeTagRelationModel.query.filter_by(recipe_id=recipe_id).all()
    tags = [TagModel.query.get(recipe_tag.tag_id).tagname for recipe_tag in recipe_tags]
    return tags
