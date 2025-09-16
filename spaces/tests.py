from django.test import TestCase


from django.test import TestCase, Client
from users.models import CustomUser
from .models import SpaceProfile

class EspacioCulturalFlowTest(TestCase):
	def setUp(self):
		self.user = CustomUser.objects.create_user(username='espacio', email='espacio@kulture.com', password='espacio123', user_type='space')
		self.space_profile = SpaceProfile.objects.create(user=self.user, description='Espacio de prueba', members='Juan, Ana', sectors=['Teatro'], total_seats=100, available_seats=100)
		self.client = Client()

	def test_login_and_home_espacio(self):
		login = self.client.login(username='espacio', password='espacio123')
		self.assertTrue(login)
		response = self.client.get('/espacio/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Espacio de prueba')
		self.assertContains(response, 'Juan, Ana')
		self.assertContains(response, '100')
		# Probar logout
		response = self.client.get('/logout/')
		self.assertEqual(response.status_code, 302)  # Redirige al home
