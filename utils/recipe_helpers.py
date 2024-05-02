from models import (
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


def find_category(recipe_id):
    recipe_categories = RecipeCategoryRelationModel.query.filter_by(
        recipe_id=recipe_id
    ).all()
    categories = [
        CategoryModel.query.get(recipe_category.category_id).category
        for recipe_category in recipe_categories
    ]
    return categories


def find_type(recipe_id):
    recipe_type = RecipeTypeRelationModel.query.filter_by(recipe_id=recipe_id).first()
    if recipe_type:
        type = TypeModel.query.get(recipe_type.type_id)
        return type.type
    else:
        return None


def find_origin(recipe_id):
    recipe_origin = RecipeOriginRelationModel.query.filter_by(
        recipe_id=recipe_id
    ).first()
    if recipe_origin:
        origin = OriginModel.query.get(recipe_origin.origin_id)
        return origin.origin
    else:
        return None


def find_tag(recipe_id):
    recipe_tags = RecipeTagRelationModel.query.filter_by(recipe_id=recipe_id).all()
    tags = [TagModel.query.get(recipe_tag.tag_id).tagname for recipe_tag in recipe_tags]
    return tags


def increment_view(recipe):
    recipe.view_count += 1
    db.session.commit()
