from django.test import TestCase, Client
from django.urls import reverse
from .models import DeliveryLocation, User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_login(self):
        # Test user login view
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect
        self.assertTrue(response.url.endswith(reverse('delivery-location-list')))  # Check if redirected to correct page

    def test_save_delivery_location(self):
        # Test save delivery location view
        self.client.force_login(self.user)
        response = self.client.post(reverse('save_delivery_location'), {'address': 'Test Address', 'latitude': 123, 'longitude': 456})
        self.assertEqual(response.status_code, 200)  # Check if the response is successful
        self.assertIn('message', response.json())  # Check if response contains 'message' key

    def test_delivery_location_list(self):
        # Test delivery location list view
        self.client.force_login(self.user)
        response = self.client.get(reverse('delivery-location-list'))
        self.assertEqual(response.status_code, 200)  # Check if the response is successful

    def test_logout_user(self):
        # Test logout user view
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect
        self.assertEqual(response.url, '/')  # Check if redirected to correct page
        

class APITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_age_group_distribution(self):
        # Test AgeGroupDistribution APIView
        url = reverse('age_group_distribution')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response contains 'data' and 'image' keys
        self.assertIn('data', response.data)
        self.assertIn('image', response.data)

        # Add more assertions based on expected response data
        data = response.data['data']
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)
        
        # Check if each item in 'data' contains 'age_group' and 'count' keys
        for item in data:
            self.assertIn('age_group', item)
            self.assertIn('count', item)


