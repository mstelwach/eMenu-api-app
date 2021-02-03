from django.core.validators import MinValueValidator
from django.db import models


# class Restaurant(models.Model):
#     name = models.CharField(max_length=128)
#     address = models.CharField(max_length=128)
#     city = models.CharField(max_length=32)
#     phone = models.CharField(max_length=16)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return 'Restaurant: {} : Phone: {}'.format(self.name, self.phone)


class Card(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    dishes = models.ManyToManyField('Dish', blank=True, related_name='dishes')

    def __str__(self):
        return 'Card menu: {}'.format(self.name)


class Dish(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    preparation_time = models.PositiveIntegerField()
    is_vege = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Dish: {} | Price: {}'.format(self.name, self.price)

