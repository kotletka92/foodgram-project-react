from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.utils import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from users.serializers import UserSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    """Converts Favorite's data."""
    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True)
    image = serializers.ImageField(
        source='recipe.image',
        read_only=True)
    coocking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'coocking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Converts Cart's data."""
    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True)
    image = serializers.ImageField(
        source='recipe.image',
        read_only=True)
    coocking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'coocking_time')


class IngredientSerializer(serializers.ModelSerializer):
    """Converts Ingredient's data."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = '__all__',


class TagSerializer(serializers.ModelSerializer):
    """Serializer для модели Tag."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = '__all__',


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Serializer for intermidiate Recipe and Ingredient model."""
    id = serializers.ReadOnlyField(
        source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model: reading data."""
    author = UserSerializer()
    tags = TagSerializer(
        many=True,
        read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='amount',
        read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        favorite = request.user.favorites.filter(recipe=obj)
        return favorite.exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        shopping_cart = request.user.cart.filter(recipe=obj)
        return shopping_cart.exists()


class IngredientAddSerializer(serializers.ModelSerializer):
    """Converts 'ingredient' field in Recipe model."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeSmallSerializer(serializers.ModelSerializer):
    """Serialiser to display a recipe in FollowSerializer."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model: all actions."""
    ingredients = IngredientAddSerializer(
        many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    image = Base64ImageField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', 'author')

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError(
                {'ingredients': 'You should choose the ingredient!'})
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(Ingredient, name=item['id'])
            if ingredient in ingredients_list:
                raise ValidationError(
                    {'ingredients': 'Indredients are the same!'})
            if int(item['amount']) <= 0:
                raise ValidationError(
                    {'amount': 'Amount should be more than 0!'})
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError(
                {'tags': 'You should choose the tag!'})
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError(
                    {'tags': 'Tags are the same!'})
            tags_list.append(tag)
        return value

    def to_representation(self,instance):
        context = {'request': self.context.get('request')}
        return RecipeListSerializer(instance, context=context).data

    def add_tags_ingredients(self, ingredients, tags, model):
        for ingredient in ingredients:
            IngredientAmount.objects.update_or_create(
                recipe=model,
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
        model.tags.set(tags)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        self.add_tags_ingredients(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.add_tags_ingredients(ingredients, tags, instance)
        return super().update(instance, validated_data)
