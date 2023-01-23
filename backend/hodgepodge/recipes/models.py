from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Represents Ingredients."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [models.UniqueConstraint(
            fields=['name', 'measurement_unit'],
            name='unique_ingredient')
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Represents Tags."""

    CHOICES = (
        ('#d6bbcb', 'Розовый'),
        ('#5e00ff', 'Сиреневый'),
        ('#81b0fd', 'Синий'),
        ('#c90076', 'Бордо'),
        ('#6dc066', 'Зеленый'),
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        verbose_name='Кодировка в HEX',
        max_length=16,
        unique=True,
        default='#800080',
        choices=CHOICES
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug для тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Represents Recipes."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное время приготовления 1 минута'),),
        verbose_name='Время приготовления')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(fields=['author', 'name'],
                                    name='unique_author_name')
        ]

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Intermediate Model for Recipes and Ingredients."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='amount'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='amount'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное количество ингредиентов 1'),
        )
    )

    class Meta:
        verbose_name = 'Состав рецепта'
        verbose_name_plural = 'Состав рецепта'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_recipe_ingredient')
        ]


class Favorite(models.Model):
    """Represents Favourite Recipes."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт из списка избранного'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['author', 'recipe'],
                                    name='favorite_recipies')
        ]


class ShoppingCart(models.Model):
    """Represents Ingredients in the Shopping Cart."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='customers',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(fields=['author', 'recipe'],
                                    name='unique_cart_user')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.author}'
