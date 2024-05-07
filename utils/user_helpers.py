from models import (
    FollowingModel,
)


def count_following(user_id):
    total_following = FollowingModel.query.filter_by(follower_id=user_id).count()
    return total_following


def count_follower(user_id):
    total_follower = FollowingModel.query.filter_by(followed_id=user_id).count()
    return total_follower
