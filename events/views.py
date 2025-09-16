from django.shortcuts import render
from .models import Event
from .models_ticket import Ticket

from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv

def lista_eventos(request):
	eventos = Event.objects.all()
	# Filtros
	q = request.GET.get('q', '').strip()
	fecha = request.GET.get('fecha', '').strip()
	precio_min = request.GET.get('precio_min', '').strip()
	precio_max = request.GET.get('precio_max', '').strip()
	artista = request.GET.get('artista', '').strip()
	espacio = request.GET.get('espacio', '').strip()
	ordenar = request.GET.get('ordenar', 'fecha')
	exportar = request.GET.get('exportar', '')

	if q:
		eventos = eventos.filter(name__icontains=q)
	if fecha:
		eventos = eventos.filter(date__date=fecha)
	if precio_min:
		eventos = eventos.filter(price__gte=precio_min)
	if precio_max:
		eventos = eventos.filter(price__lte=precio_max)
	if artista:
		eventos = eventos.filter(artist__user__username__icontains=artista)
	if espacio:
		eventos = eventos.filter(space__user__username__icontains=espacio)
	if ordenar == 'fecha':
		eventos = eventos.order_by('date')
	elif ordenar == 'precio':
		eventos = eventos.order_by('price')
	else:
		eventos = eventos.order_by('-date')

	# Exportar CSV
	if exportar == 'csv':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="eventos.csv"'
		writer = csv.writer(response)
		writer.writerow(['Nombre', 'Fecha', 'Descripción', 'Precio', 'Artista', 'Espacio', 'Asientos disponibles'])
		for e in eventos:
			writer.writerow([
				e.name,
				e.date,
				e.description,
				e.price,
				e.artist.user.username if e.artist else '',
				e.space.user.username if e.space else '',
				e.available_seats
			])
		return response

	# Paginación
	paginator = Paginator(eventos, 6)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'lista_eventos.html', {
		'eventos': page_obj,
		'q': q,
		'fecha': fecha,
		'precio_min': precio_min,
		'precio_max': precio_max,
		'artista': artista,
		'espacio': espacio,
		'ordenar': ordenar,
		'page_obj': page_obj
	})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .models_ticket import Ticket

def comprar_ticket(request, event_id):
	event = get_object_or_404(Event, id=event_id)
	error = None
	if request.method == 'POST':
		buyer_name = request.POST.get('buyer_name')
		buyer_email = request.POST.get('buyer_email')
		seats_reserved = int(request.POST.get('seats_reserved', 1))
		if seats_reserved > event.available_seats:
			error = 'No hay suficientes asientos disponibles.'
		elif seats_reserved <= 0:
			error = 'Debes reservar al menos un asiento.'
		else:
			amount_paid = event.price * seats_reserved
			Ticket.objects.create(
				event=event,
				buyer_name=buyer_name,
				buyer_email=buyer_email,
				seats_reserved=seats_reserved,
				amount_paid=amount_paid
			)
			event.available_seats -= seats_reserved
			event.save()
			return redirect('ticket_exito', event_id=event.id)
	return render(request, 'comprar_ticket.html', {
		'event': event,
		'error': error
	})

def ticket_exito(request, event_id):
	event = get_object_or_404(Event, id=event_id)
	return render(request, 'ticket_exito.html', {'event': event})
