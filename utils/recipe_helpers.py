import random

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
    CommentModel,
    UserModel,
    RecipeModel,
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
        ingredient_member.append(
            IngredientModel.query.get(recipe_ingredient.ingredient_id).ingredient_image
        )

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


# def get_comments(recipe_id):
#     comments = []
#     recipe_comments = CommentModel.query.filter_by(recipe_id=recipe_id).all()

#     if not recipe_comments:
#         return comments

#     for comment in recipe_comments:
#         comment_member = []
#         commenter = UserModel.query.filter_by(id=comment.user_id).first()
#         commenter_name = commenter.first_name + " " + commenter.last_name

#         comment_member.append(commenter_name)
#         comment_member.append(comment.message)
#         comments.append(comment_member)

#     return comments


def get_comments(recipe_id):
    comments = CommentModel.query.filter_by(recipe_id=recipe_id).all()
    return comments


def chef_recipe_check(recipe_id):
    recipe = RecipeModel.query.filter_by(id=recipe_id).first()
    user = UserModel.query.filter_by(id=recipe.author_id).first()

    if user.role.value == "chef":
        return True
    else:
        return False


ingredient_default_images = [
    "https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-indian-cuisine-spice-mix-curry-powder-food-age-reversing-nutrition-ayurveda-creating-radi-5b7ba6e00461f8.418255421534830304018.png",
    "https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-herbalism-therapy-herbal-tonic-medicine-spice-5abb76950594b8.6884587515222350290229.png",
    "https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-organic-food-vegetable-carrot-5ae2b63ea38993.9311661015248072306699.png",
    "https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-spice-masala-indian-cuisine-nutmeg-turmeric-spices-5b17857fbed319.5587043615282681597816.png",
    "https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-vegetable-portable-network-graphics-fruit-clip-art-baking-needs-5cbf3c93326f43.1363482015560367552066.png",
    "https://lwgscyxqeipmjzaxphkv.supabase.co/storage/v1/object/public/ingredients_image/images/default/kisspng-allspice-herb-food-spice-mix-spices-5abd2b9718b375.3009980215223469031012.png",
]

selected_ingredient_image = random.choice(ingredient_default_images)


def increment_view(user_or_recipe):
    user_or_recipe.view_count += 1
    db.session.commit()


def get_author_name(recipe_id):
    author_id = RecipeModel.query.filter_by(id=recipe_id).first().author_id
    author_name = UserModel.query.filter_by(id=author_id).first().username
    return author_name
