from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Subscription, User

from .filters import IngredientFilter, RecipeFilter
from .mixins import ActionMixin
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, ShowSubscriptionsSerializer,
                          SubscriptionSerializer, TagSerializer)


class BaseActionView(ActionMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        data = {'user': request.user.id, self.related_field: id}
        return self.action_add(request, data, self.model_class,
                               self.serializer_class, self.success_status)

    def delete(self, request, id):
        data = {'user': request.user.id, self.related_field: id}
        return self.delete_action(request, self.model_class, data)


class SubscribeView(BaseActionView):
    """ Операция подписки/отписки. """

    model_class = Subscription
    serializer_class = SubscriptionSerializer
    success_status = status.HTTP_201_CREATED
    related_field = 'author'


class FavoriteView(BaseActionView):
    """ Добавление/удаление рецепта из избранного. """

    model_class = Favorite
    serializer_class = FavoriteSerializer
    success_status = status.HTTP_201_CREATED
    related_field = 'recipe'
    pagination_class = CustomPagination


class ShoppingCartView(BaseActionView):
    """ Добавление рецепта в корзину или его удаление. """

    model_class = ShoppingCart
    serializer_class = ShoppingCartSerializer
    success_status = status.HTTP_201_CREATED
    related_field = 'recipe'


class ShowSubscriptionsView(ListAPIView):
    """ Отображение подписок. """

    permission_classes = [IsAuthenticated]
    serializer_class = ShowSubscriptionsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(author__user=user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Отображение тегов. """

    permission_classes = [AllowAny, ]
    pagination_class = None
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Отображение ингредиентов. """

    permission_classes = [AllowAny, ]
    pagination_class = None
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [IngredientFilter, ]
    search_fields = ['^name', ]


class RecipeViewSet(viewsets.ModelViewSet):
    """ Операции с рецептами: добавление/изменение/удаление/просмотр. """

    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    pagination_class = CustomPagination
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


@api_view(['GET'])
def download_shopping_cart(request):
    ingredient_list = "Cписок покупок:"
    ingredients = RecipeIngredient.objects.filter(
        recipe__shopping_cart__user=request.user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(recipe__amount=Sum('amount'))
    for num, i in enumerate(ingredients):
        ingredient_list += (
            f"\n{i['ingredient__name']} - "
            f"{i['recipe__amount']} {i['ingredient__measurement_unit']}"
        )
        if num < ingredients.count() - 1:
            ingredient_list += ', '
    file = 'shopping_list'
    response = HttpResponse(ingredient_list, 'Content-Type: application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
    return response
