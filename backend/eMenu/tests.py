from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from eMenu.models import Dish, Card


class CardCRUDTest(TestCase):
    """Test suite for the api model card."""

    def setUp(self):
        """Define the test card and dish model."""
        self.dish = Dish.objects.create(name='TestNameDish',
                                        description='TestDescriptionDish',
                                        price=19.99,
                                        preparation_time=45,
                                        is_vege=True)
        self.dish.save()

        self.card = Card.objects.create(name='TestNameCard', description='TestDescriptionCard')
        self.card.save()
        self.card.dishes.add(self.dish)

    def test_create_card(self):
        """Test the api has card model creation capability."""
        self.assertIn(self.card, Card.objects.all())

    def test_retrieve_card(self):
        """Test the api can get a given card model."""
        self.assertEqual(self.card.name, 'TestNameCard')
        self.assertEqual(self.card.description, 'TestDescriptionCard')
        self.assertIn(self.dish, self.card.dishes.all())

    def test_update_card_name(self):
        """Test the api can update name a given card model."""
        self.card.name = 'TestNewNameCard'
        self.card.save()
        self.assertEqual(self.card.name, 'TestNewNameCard')

    def test_update_card_description(self):
        """Test the api can update description a given card model."""
        self.card.description = 'TestNewDescriptionCard'
        self.card.save()
        self.assertEqual(self.card.description, 'TestNewDescriptionCard')

    def tearDown(self):
        self.card.delete()
        self.dish.delete()


class DishCRUDTestCase(TestCase):
    """Test suite for the api model dish."""

    def setUp(self):
        """Define the test dish model."""
        self.dish = Dish.objects.create(name='TestNameDish',
                                        description='TestDescriptionDish',
                                        price=19.99,
                                        preparation_time=45,
                                        is_vege=True)
        self.dish.save()

    def test_create_dish(self):
        """Test the api has dish model creation capability."""
        self.assertIn(self.dish, Dish.objects.all())

    def test_retrieve_dish(self):
        """Test the api can get a given dish model."""
        self.assertEqual(self.dish.name, 'TestNameDish')
        self.assertEqual(self.dish.description, 'TestDescriptionDish')
        self.assertEqual(self.dish.price, 19.99)
        self.assertEqual(self.dish.preparation_time, 45)
        self.assertTrue(self.dish.is_vege)

    def test_update_dish_name(self):
        """Test the api can update name a given dish model."""
        self.dish.name = 'TestNewNameDish'
        self.dish.save()
        self.assertEqual(self.dish.name, 'TestNewNameDish')

    def test_update_dish_description(self):
        """Test the api can update description a given dish model."""
        self.dish.description = 'TestNewDescriptionDish'
        self.dish.save()
        self.assertEqual(self.dish.description, 'TestNewDescriptionDish')

    def test_update_dish_price(self):
        """Test the api can update price a given dish model."""
        self.dish.price = 29.99
        self.dish.save()
        self.assertEqual(self.dish.price, 29.99)

    def test_update_dish_preparation_time(self):
        """Test the api can update preparation time a given dish model."""
        self.dish.preparation_time = 30
        self.dish.save()
        self.assertEqual(self.dish.preparation_time, 30)

    def test_update_dish_is_vege(self):
        """Test the api can update is_vege a given dish model."""
        self.dish.is_vege = False
        self.dish.save()
        self.assertFalse(self.dish.is_vege)

    def tearDown(self):
        self.dish.delete()


class CardPublicViewTest(APITestCase):
    """Test suite for the api card public view."""

    def setUp(self):
        """Define the test card and dish model."""
        self.dish = Dish.objects.create(name='TestViewNameDish',
                                        description='TestViewDescriptionDish',
                                        price=19.99,
                                        preparation_time=45,
                                        is_vege=True)
        self.dish.save()

        self.card = Card.objects.create(name='TestViewNameCard', description='TestViewDescriptionCard')
        self.card.save()
        self.card.dishes.add(self.dish)

    def test_retrieve_public_view_card(self):
        """Test the api can get a given card list and card detail."""
        response_card_list = self.client.get(
            reverse('card-list'),
            format='json'
        )
        response_card_detail = self.client.get(
            reverse('card-detail', kwargs={'pk': self.card.pk})
        )
        self.assertEqual(response_card_list.status_code, status.HTTP_200_OK)
        self.assertEqual(response_card_detail.status_code, status.HTTP_200_OK)

    def test_authorization_public_view_card(self):
        """Test that the api view no authorization."""
        response = self.client.post(
            reverse('card-list'),
            {'name': 'TestPrivateViewNameCard', 'description': 'TestPrivateViewDescriptionCard'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.card.delete()
        self.dish.delete()


class DishPublicViewTest(APITestCase):
    """Test suite for the api dish public view."""

    def setUp(self):
        """Define the test dish model."""
        self.dish = Dish.objects.create(name='TestViewNameDish',
                                        description='TestViewDescriptionDish',
                                        price=19.99,
                                        preparation_time=45,
                                        is_vege=True)
        self.dish.save()

    def test_retrieve_public_view_dish(self):
        """Test the api can get a given dish list and dish detail."""
        response_dish_list = self.client.get(
            reverse('dish-list'),
            format='json'
        )
        response_dish_detail = self.client.get(
            reverse('dish-detail', kwargs={'pk': self.dish.pk})
        )
        self.assertEqual(response_dish_list.status_code, status.HTTP_200_OK)
        self.assertEqual(response_dish_detail.status_code, status.HTTP_200_OK)

    def test_authorization_public_view_dish(self):
        """Test that the api view no authorization."""
        response = self.client.post(
            reverse('dish-list'),
            {'name': 'TestPrivateViewNameCard', 'description': 'TestPrivateViewDescriptionCard'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.dish.delete()


class CardPrivateViewCRUDTest(APITestCase):
    """Test suite for the api card private view."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = get_user_model().objects.create_user(username='TestUsername',
                                                         password='TestPassword',
                                                         email='TestEmail@test.com')

        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Since user model instance is not serializable, use its Id/PK
        self.response = self.client.post(
            reverse('card-list'),
            {'name': 'TestPrivateViewNameCard', 'description': 'TestPrivateViewDescriptionCard'},
            format='json'
        )

    def test_create_private_view_card(self):
        """Test the api has card creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_private_view_card(self):
        """Test the api can get a given card list and card detail."""
        card = Card.objects.get()
        response_card_list = self.client.get(
            reverse('card-list'),
            format='json'
        )
        response_card_detail = self.client.get(
            reverse('card-detail', kwargs={'pk': card.pk}),
            format='json'
        )
        self.assertEqual(response_card_list.status_code, status.HTTP_200_OK)
        self.assertEqual(response_card_detail.status_code, status.HTTP_200_OK)

    def test_update_private_view_card(self):
        """Test the api can update a given card."""
        card = Card.objects.get()
        response = self.client.put(
            reverse('card-detail', kwargs={'pk': card.pk}),
            {'name': 'TestPrivateViewNewNameCard'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_private_view_card(self):
        """Test the api can delete a card."""
        card = Card.objects.get()
        response = self.client.delete(
            reverse('card-detail', kwargs={'pk': card.pk}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authorization_private_view_card(self):
        """Test that the api has user authorization."""
        client = APIClient()
        response = client.post(
            reverse('card-list'),
            {'name': 'TestPrivateViewNameCard', 'description': 'TestPrivateViewDescriptionCard'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.user.delete()


class DishPrivateViewCRUDTest(APITestCase):
    """Test suite for the api dish private view."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = get_user_model().objects.create_user(username='TestUsername',
                                                         password='TestPassword',
                                                         email='TestEmail@test.com')

        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Since user model instance is not serializable, use its Id/PK
        self.response = self.client.post(
            reverse('dish-list'),
            {
                'name': 'TestPrivateViewNameDish',
                'description': 'TestPrivateViewDescriptionDish',
                'price': 19.99,
                'preparation_time': 30,
                'is_vege': False,
            },
            format='json'
        )

    def test_create_private_view_dish(self):
        """Test the api has dish creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_private_view_dish(self):
        """Test the api can get a given dish list and dish detail."""
        dish = Dish.objects.get()
        response_dish_list = self.client.get(
            reverse('dish-list'),
            format='json'
        )
        response_dish_detail = self.client.get(
            reverse('dish-detail', kwargs={'pk': dish.pk}),
            format='json'
        )
        self.assertEqual(response_dish_list.status_code, status.HTTP_200_OK)
        self.assertEqual(response_dish_detail.status_code, status.HTTP_200_OK)

    def test_update_private_view_dish(self):
        """Test the api can update a given dish."""
        dish = Dish.objects.get()
        response = self.client.put(
            reverse('dish-detail', kwargs={'pk': dish.pk}),
            {
                'name': 'TestPrivateViewNewNameDish',
                'price': 29.99,
                'preparation_time': 15,
                'is_vege': True
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_private_view_dish(self):
        """Test the api can delete a dish."""
        dish = Dish.objects.get()
        response = self.client.delete(
            reverse('dish-detail', kwargs={'pk': dish.pk}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authorization_private_view_dish(self):
        """Test that the api has user authorization."""
        client = APIClient()
        response = client.post(
            reverse('card-list'),
            {'name': 'TestPrivateViewNameCard', 'description': 'TestPrivateViewDescriptionCard'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.user.delete()


class UserTestCase(TestCase):
    """Test suite for the api model user"""

    def setUp(self):
        """Define the test user model"""
        self.user = get_user_model().objects.create_user(username='TestUsername',
                                                         password='TestPassword',
                                                         email='TestEmail@test.com')
        self.user.save()

    def test_correct_user(self):
        user = authenticate(username='TestUsername', password='TestPassword')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='Wrong', password='TestPassword')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='TestUsername', password='Wrong')
        self.assertFalse(user is not None and user.is_authenticated)

    def tearDown(self):
        self.user.delete()