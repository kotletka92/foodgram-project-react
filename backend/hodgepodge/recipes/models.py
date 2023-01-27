from django.core import validators
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Represents Ingredients."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        db_index=True,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Represents Tags."""

    CHOICES = (
        ('#c90076', 'Розовый'),
        ('#7c12e1', 'Сиреневый'),
        ('#068cf1', 'Синий'),
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
        verbose_name='Название',
        db_index=True
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
    created = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        help_text="Автоматически устанавливается текущая дата и время",
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipe'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe')]

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Intermediate Model for Recipes and Ingredients."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
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
        ordering = ['ingredient']
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
        verbose_name='Автор',
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт из списка избранного'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe'],
            name='favorite_unique')]

    def __str__(self):
        return f'{self.recipe}'


class ShoppingCart(models.Model):
    """Represents Ingredients in the Shopping Cart."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_cart')]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.author}'
