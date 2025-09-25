from django.test import TestCase


from django.test import TestCase
from .models import CustomUser


from django.test import TestCase, Client
from .models import CustomUser

class CustomUserTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		CustomUser.objects.create_user(username='evento', email='evento@kulture.com', password='evento123', user_type='super')
		CustomUser.objects.create_user(username='espacio', email='espacio@kulture.com', password='espacio123', user_type='space')
		CustomUser.objects.create_user(username='admin', email='admin@kulture.com', password='admin123', user_type='super', is_staff=True, is_superuser=True)
		CustomUser.objects.create_user(username='artista', email='artista@kulture.com', password='artista123', user_type='artist')
		CustomUser.objects.create_user(username='colaborador', email='colaborador@kulture.com', password='colaborador123', user_type='collaborator')

	def test_users_created(self):
		self.assertTrue(CustomUser.objects.filter(username='evento').exists())
		self.assertTrue(CustomUser.objects.filter(username='espacio').exists())
		self.assertTrue(CustomUser.objects.filter(username='admin').exists())
		self.assertTrue(CustomUser.objects.filter(username='artista').exists())
		self.assertTrue(CustomUser.objects.filter(username='colaborador').exists())

	def test_login_superuser_redirect(self):
		response = self.client.post('/login/', {'username': 'admin', 'password': 'admin123'})
		self.assertEqual(response.status_code, 302)
		self.assertIn('/superusuario/', response.url)

	def test_login_espacio_redirect(self):
		response = self.client.post('/login/', {'username': 'espacio', 'password': 'espacio123'})
		self.assertEqual(response.status_code, 302)
		self.assertIn('/espacio/', response.url)

	def test_login_artista_redirect(self):
		response = self.client.post('/login/', {'username': 'artista', 'password': 'artista123'})
		self.assertEqual(response.status_code, 302)
		self.assertIn('/artista/', response.url)

	def test_login_colaborador_redirect(self):
		response = self.client.post('/login/', {'username': 'colaborador', 'password': 'colaborador123'})
		self.assertEqual(response.status_code, 302)
		self.assertIn('/blog/colaborador/', response.url)

	def test_login_evento_redirect(self):
		response = self.client.post('/login/', {'username': 'evento', 'password': 'evento123'})
		self.assertEqual(response.status_code, 302)
		self.assertIn('/admin/', response.url)
