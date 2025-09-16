
from django.test import TestCase, Client
from users.models import CustomUser
from artists.models import ArtistProfile
from spaces.models import SpaceProfile
from events.models import Event
from events.models_ticket import Ticket
from events.models_expense import Expense


class TicketPurchaseBalanceTest(TestCase):
	def setUp(self):
		self.artist_user = CustomUser.objects.create_user(username='artista', email='artista@kulture.com', password='artista123', user_type='artist')
		self.artist_profile = ArtistProfile.objects.create(user=self.artist_user, description='Artista test', sectors=['Musica'], website='https://artista.com')
		self.space_user = CustomUser.objects.create_user(username='espacio', email='espacio@kulture.com', password='espacio123', user_type='space')
		self.space_profile = SpaceProfile.objects.create(user=self.space_user, description='Espacio test', members='Juan, Ana', sectors=['Teatro'], total_seats=100, available_seats=100)
		self.event = Event.objects.create(
			name='Concierto Test',
			organizer=self.artist_user,
			artist=self.artist_profile,
			space=self.space_profile,
			date='2025-09-30T20:00',
			description='Evento de prueba',
			sectors=['General'],
			total_seats=50,
			available_seats=50,
			price=100.00
		)
		self.client = Client()

	def test_ticket_purchase_and_balance(self):
		# Compra de 2 tickets
		response = self.client.post(f'/comprar-ticket/{self.event.id}/', {
			'buyer_name': 'Cliente Uno',
			'buyer_email': 'cliente1@test.com',
			'seats_reserved': 2
		})
		self.assertEqual(response.status_code, 302)  # Redirige a éxito
		self.event.refresh_from_db()
		self.assertEqual(self.event.available_seats, 48)
		ticket = Ticket.objects.filter(event=self.event).first()
		self.assertIsNotNone(ticket)
		self.assertEqual(ticket.amount_paid, 200.00)

		# Registrar gasto
		Expense.objects.create(event=self.event, concept='Sonido', amount=50.00)
		Expense.objects.create(event=self.event, concept='Luces', amount=30.00)

		# Validar balance
		total_ventas = sum(t.amount_paid for t in Ticket.objects.filter(event=self.event))
		total_gastos = sum(e.amount for e in Expense.objects.filter(event=self.event))
		total_ganancia = total_ventas - total_gastos
		self.assertEqual(total_ventas, 200.00)
		self.assertEqual(total_gastos, 80.00)
		self.assertEqual(total_ganancia, 120.00)

		# Compra que excede asientos
		response = self.client.post(f'/comprar-ticket/{self.event.id}/', {
			'buyer_name': 'Cliente Dos',
			'buyer_email': 'cliente2@test.com',
			'seats_reserved': 100
		})
		self.assertContains(response, 'No hay suficientes asientos disponibles.', status_code=200)

	def test_multiple_ticket_purchases_and_gastos(self):
		# Compra de 1 ticket
		self.client.post(f'/comprar-ticket/{self.event.id}/', {
			'buyer_name': 'Cliente A',
			'buyer_email': 'a@test.com',
			'seats_reserved': 1
		})
		# Compra de 3 tickets
		self.client.post(f'/comprar-ticket/{self.event.id}/', {
			'buyer_name': 'Cliente B',
			'buyer_email': 'b@test.com',
			'seats_reserved': 3
		})
		self.event.refresh_from_db()
		self.assertEqual(self.event.available_seats, 46)
		tickets = Ticket.objects.filter(event=self.event)
		self.assertEqual(tickets.count(), 2)
		self.assertEqual(sum(t.seats_reserved for t in tickets), 4)
		self.assertEqual(sum(t.amount_paid for t in tickets), 400.00)

		# Registrar gastos
		Expense.objects.create(event=self.event, concept='Publicidad', amount=60.00)
		Expense.objects.create(event=self.event, concept='Staff', amount=20.00)
		total_gastos = sum(e.amount for e in Expense.objects.filter(event=self.event))
		self.assertEqual(total_gastos, 80.00)
		total_ganancia = sum(t.amount_paid for t in tickets) - total_gastos
		self.assertEqual(total_ganancia, 320.00)

	def test_invalid_ticket_reservation(self):
		# Intentar reservar 0 asientos
		response = self.client.post(f'/comprar-ticket/{self.event.id}/', {
			'buyer_name': 'Cliente Inválido',
			'buyer_email': 'inv@test.com',
			'seats_reserved': 0
		})
		self.assertContains(response, 'Debes reservar al menos un asiento.', status_code=200)

	def test_negative_expense(self):
		# Registrar gasto negativo
		Expense.objects.create(event=self.event, concept='Error', amount=-50.00)
		total_gastos = sum(e.amount for e in Expense.objects.filter(event=self.event))
		self.assertEqual(total_gastos, -50.00)
		# El balance debe sumar el negativo
		Ticket.objects.create(event=self.event, buyer_name='Cliente', buyer_email='c@test.com', seats_reserved=1, amount_paid=100.00)
		from decimal import Decimal
		total_ventas = sum(t.amount_paid for t in Ticket.objects.filter(event=self.event))
		total_ganancia = Decimal(str(total_ventas)) - Decimal(str(total_gastos))
		self.assertEqual(total_ganancia, Decimal('150.00'))
