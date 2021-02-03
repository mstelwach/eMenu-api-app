from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from eMenu.api.serializers import CardSerializer, DishSerializer
from eMenu.api.filters import CardOrderingFilter, CardFilter, DishFilter
from eMenu.models import Card, Dish


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, CardOrderingFilter, )
    filterset_class = CardFilter
    ordering_fields = ('name', 'dishes_count', )

    def get_queryset(self):
        queryset = Card.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.exclude(dishes__isnull=True)

        # Optionally filtering against a field query parameter in the URL.
        # name = self.request.query_params.get('name', None)
        # created = self.request.query_params.get('created', None)
        # updated = self.request.query_params.get('updated', None)
        #
        # if name is not None:
        #     queryset = queryset.filter(name__contains=name)
        # if created is not None:
        #     queryset = queryset.filter(created__date__gte=created)
        # if updated is not None:
        #     queryset = queryset.filter(updated__date__gte=updated)

        return queryset


class DishViewSet(ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, OrderingFilter, )
    filterset_class = DishFilter
    ordering_fields = ('name', 'price', 'preparation_time', )