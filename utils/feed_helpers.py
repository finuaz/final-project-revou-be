from models import (
    CategoryModel,
    TypeModel,
    OriginModel,
    TagModel,
    RecipeCategoryRelationModel,
    RecipeTypeRelationModel,
    RecipeOriginRelationModel,
    RecipeTagRelationModel,
    RateModel,
    LikeModel,
)


def find_all_category(recipe_id):
    categories = []
    recipe_categories = RecipeCategoryRelationModel.query.filter_by(
        recipe_id=recipe_id
    ).all()
    for recipe_category in recipe_categories:
        category = CategoryModel.query.get(recipe_category.category_id)
        categories.append(category.category)
    return categories if categories else None


def find_all_type(recipe_id):
    recipe_type = RecipeTypeRelationModel.query.filter_by(recipe_id=recipe_id).first()
    if recipe_type:
        type = TypeModel.query.get(recipe_type.type_id)
        return type.type if type else None


def find_all_origin(recipe_id):
    recipe_origin = RecipeOriginRelationModel.query.filter_by(
        recipe_id=recipe_id
    ).first()
    if recipe_origin:
        origin = OriginModel.query.get(recipe_origin.origin_id)
        return origin.origin if origin else None
    # else:
    #     return None


def find_all_tag(recipe_id):
    tags = []
    recipe_tags = RecipeTagRelationModel.query.filter_by(recipe_id=recipe_id).all()
    for recipe_tag in recipe_tags:
        tag = TagModel.query.get(recipe_tag.tag_id)
        tags.append(tag.tagname)
    return tags if tags else None


def get_likes(recipe_id):
    like_count = LikeModel.query.filter_by(recipe_id=recipe_id).count()
    return like_count


def get_rating(recipe_id):
    rates = RateModel.query.filter_by(recipe_id=recipe_id).all()
    total_value = 0
    for rate in rates:
        total_value += rate.value

    if not rates:
        return 0.0

    avg_rate = total_value / len(rates)
    return avg_rate
