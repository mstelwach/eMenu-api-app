from django.db.models import Count
from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet
from rest_framework.filters import OrderingFilter

from eMenu.models import Card, Dish


class CardOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            queryset = queryset.annotate(dishes_count=Count('dishes'))
            return queryset.order_by(*ordering)

        return queryset


class CardFilter(FilterSet):
    start_created = filters.DateTimeFilter(field_name='created', lookup_expr='date__gte', label='Start Created Date')
    end_created = filters.DateTimeFilter(field_name='created', lookup_expr='date__lte', label='End Created Date')
    start_updated = filters.DateTimeFilter(field_name='updated', lookup_expr='date__gte', label='Start Updated Date')
    end_updated = filters.DateTimeFilter(field_name='updated', lookup_expr='date__lte', label='End Updated Date')

    # def get_date_filter(self, queryset, field_name, value):
    #     return queryset.filter(**{field_name: value})

    class Meta:
        model = Card
        fields = ('name', 'start_created', 'end_created', 'start_updated', 'end_updated', )


class DishFilter(FilterSet):
    start_price = filters.NumberFilter(field_name='price', lookup_expr='gte', label='Start Price')
    end_price = filters.NumberFilter(field_name='price', lookup_expr='lte', label='End Price')
    start_preparation_time = filters.NumberFilter(field_name='preparation_time',
                                                  lookup_expr='gte',
                                                  label='Start Preparation Time')
    end_preparation_time = filters.NumberFilter(field_name='preparation_time',
                                                lookup_expr='lte',
                                                label='End Preparation Time')

    class Meta:
        model = Dish
        fields = ('name', 'start_price', 'end_price', 'start_preparation_time', 'end_preparation_time', 'is_vege', )
