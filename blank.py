# recipe_origin = RecipeOriginRelationModel.query.filter_by(
#     recipe_id=recipe_in_details_by_id
# ).first()

# if recipe_origin:
#     origin = OriginModel.query.get(recipe_origin.origin_id)
#     if origin:
#         recipe.origin = origin.origin
#     else:
#         recipe.origin = None  # or any default value if needed
# else:
#     recipe.origin = None
