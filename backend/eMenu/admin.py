from django.contrib import admin
from .models import Card, Dish


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'updated',)
    list_filter = ('name', 'created', 'updated',)


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'preparation_time', 'is_vege',)
    list_filter = ('name', 'price', 'preparation_time', 'is_vege')


admin.site.register(Card, CardAdmin)
admin.site.register(Dish, DishAdmin)