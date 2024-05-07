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
    FollowingModel,
)

from db import db


def count_following(user_id):
    print("-------- reach count following")
    total_following = FollowingModel.query.filter_by(follower_id=user_id).count()
    print(total_following)
    return total_following


def count_follower(user_id):
    print("-------- reach count follower")
    total_follower = FollowingModel.query.filter_by(followed_id=user_id).count()
    print(total_follower)
    return total_follower
