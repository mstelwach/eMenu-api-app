from rest_framework.serializers import ModelSerializer

from eMenu.models import Card, Dish


class DishSerializer(ModelSerializer):

    class Meta:
        model = Dish
        fields = ('pk', 'name', 'description', 'price', 'preparation_time', 'is_vege', 'created', 'updated', )
        extra_kwargs = {
            'created': {
                'required': False
            },
            'updated': {
                'required': False
            }
        }


class CardSerializer(ModelSerializer):
    # dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = ('pk', 'name', 'description', 'created', 'updated', 'dishes', )
        extra_kwargs = {
            'created': {
                'required': False
            },
            'updated': {
                'required': False
            },
        }

    def to_representation(self, instance):
        card = super(CardSerializer, self).to_representation(instance)
        card['dishes'] = DishSerializer(instance.dishes.all(), many=True).data
        return card