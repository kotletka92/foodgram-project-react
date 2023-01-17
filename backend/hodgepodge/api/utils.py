from recipes.models import IngredientAmount


def create_ingredients(ingredients, recipe):
    list = []
    for ingredient in ingredients:
        ingredient_id = ingredient['id']
        amount = ingredient['amount']
        recipe_ingredient = IngredientAmount(
            recipe=recipe,
            ingredient=ingredient_id,
            amount=amount
        )
        list.append(recipe_ingredient)
    IngredientAmount.objects.bulk_create(list)
