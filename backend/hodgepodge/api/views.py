from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsOwnerOrAdminOrReadOnly
from api.serializers import (IngredientSerializer, RecipeListSerializer,
                             RecipeSmallSerializer, RecipeWriteSerializer,
                             TagSerializer)
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)

from .utils import delete, post


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """ViewSet for Tag model."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """ViewSet for Ingredient model."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filterset_class = (IngredientFilter, )
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet for Recipe model: [GET, POST, DELETE, PATCH]."""
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    pagination_class = CustomPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeWriteSerializer

    @action(detail=True, methods=['POST', 'DELETE'],)
    def favorite(self, request, pk):
        if self.request.method == 'POST':
            return post(request, pk, Favorite, RecipeSmallSerializer)
        return delete(request, pk, Favorite)

    @action(detail=True, methods=['POST', 'DELETE'],)
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return post(request, pk, ShoppingCart, RecipeSmallSerializer)
        return delete(request, pk, ShoppingCart)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = self.request.user
        shopping_cart = user.cart.all()
        catlg = {}
        for item in shopping_cart:
            recipe = item.recipe
            ingredients = IngredientAmount.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in catlg:
                    catlg[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    catlg[name]['amount'] = (
                        catlg[name]['amount'] + amount
                    )
        shopping_list = [
            f'{item} - {value["amount"]} {catlg[item]["measurement_unit"]} \n'
            for item, value in catlg.items()
        ]
        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
        return response
