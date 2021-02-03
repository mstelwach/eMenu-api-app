from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('cards', views.CardViewSet, 'card')
router.register('dishes', views.DishViewSet, 'dish')

urlpatterns = [
   path('', include(router.urls)),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
