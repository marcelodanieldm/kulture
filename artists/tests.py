from django.test import TestCase


from django.test import TestCase, Client
from users.models import CustomUser
from .models import ArtistProfile

class ArtistFlowTest(TestCase):
	def setUp(self):
		self.user = CustomUser.objects.create_user(username='artista', email='artista@kulture.com', password='artista123', user_type='artist')
		self.artist_profile = ArtistProfile.objects.create(user=self.user, description='Artista de prueba', sectors=['Musica'], website='https://artista.com')
		self.client = Client()

	def test_login_access_logout(self):
		login = self.client.login(username='artista', password='artista123')
		self.assertTrue(login)
		response = self.client.get('/artista/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Artista de prueba')
		# Logout
		response = self.client.get('/logout/')
		self.assertEqual(response.status_code, 302)
		self.assertIn('/', response.url)
		# Acceso denegado tras logout
		response = self.client.get('/artista/')
		self.assertEqual(response.status_code, 302)
		self.assertIn('/login/', response.url)
