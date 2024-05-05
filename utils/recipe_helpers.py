from models import (
    CategoryModel,
    TypeModel,
    OriginModel,
    TagModel,
    IngredientModel,
    RecipeCategoryRelationModel,
    RecipeTypeRelationModel,
    RecipeOriginRelationModel,
    RecipeTagRelationModel,
    RecipeIngredientRelationModel,
    AttachmentModel,
    NutritionModel,
    LikeModel,
    RateModel,
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


def find_ingredient(recipe_id):
    ingredients = []
    recipe_ingredients = RecipeIngredientRelationModel.query.filter_by(
        recipe_id=recipe_id
    ).all()

    for recipe_ingredient in recipe_ingredients:
        ingredient_member = []
        ingredient_member.append(
            IngredientModel.query.get(recipe_ingredient.ingredient_id).ingredient
        )
        ingredient_member.append(recipe_ingredient.amount)
        ingredients.append(ingredient_member)

    return ingredients


def find_attachment(recipe_id):
    attachment = AttachmentModel.query.filter_by(recipe_id=recipe_id).first()
    if attachment:
        return attachment.attachment_link
    else:
        return None


# Nutrition group
def find_serving_per_container(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.serving_per_container
    return None


def find_serving_size(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.serving_size
    return None


def find_calories(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.calories
    return None


def find_total_fat(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.total_fat
    return None


def find_total_carbohydrate(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.total_carbohydrate
    return None


def find_total_sugar(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.total_sugar
    return None


def find_cholesterol(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.cholesterol
    return None


def find_protein(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.protein
    return None


def find_vitamin_d(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.vitamin_d
    return None


def find_sodium(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.sodium
    return None


def find_calcium(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.calcium
    return None


def find_potassium(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.potassium
    return None


def find_iron(recipe_id):
    nutrition = NutritionModel.query.filter_by(recipe_id=recipe_id).first()
    if nutrition:
        return nutrition.iron
    return None


def increment_view(recipe):
    recipe.view_count += 1
    db.session.commit()


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
