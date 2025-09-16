from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Dashboard para usuarios tipo evento
@login_required
def home_evento(request):
	# Puedes personalizar la lógica y el contexto según lo que necesite mostrar el dashboard de evento
	return render(request, 'home_evento.html', {})
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
# Lista de eventos por venir con paginación, edición y eliminación
@login_required
def eventos_por_venir(request):
	eventos = Event.objects.filter(date__gte=timezone.now()).order_by('date')
	paginator = Paginator(eventos, 5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'eventos_por_venir.html', {'eventos': page_obj, 'page_obj': page_obj})

@login_required
def editar_evento(request, event_id):
	evento = get_object_or_404(Event, id=event_id)
	if request.method == 'POST':
		form = EventForm(request.POST, request.FILES, instance=evento)
		if form.is_valid():
			form.save()
			return redirect('eventos_por_venir')
	else:
		form = EventForm(instance=evento)
	return render(request, 'editar_evento.html', {'form': form, 'evento': evento})

@login_required
def eliminar_evento(request, event_id):
	evento = get_object_or_404(Event, id=event_id)
	if request.method == 'POST':
		evento.delete()
		return redirect('eventos_por_venir')
	return render(request, 'eliminar_evento.html', {'evento': evento})

# --- QR y descargas ---
import qrcode
import io
import base64
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def detalle_evento(request, event_id):
	from django.shortcuts import get_object_or_404
	evento = get_object_or_404(Event, id=event_id)
	qr_data = f"Evento: {evento.name}\nFecha: {evento.date}\nLugar: {evento.space}\nCiudad: {evento.ciudad}\nPaís: {evento.pais}"
	qr_img = qrcode.make(qr_data)
	buffer = io.BytesIO()
	qr_img.save(buffer, format='PNG')
	qr_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')
	whatsapp_url = f"https://wa.me/?text=Evento%20{evento.name}%20{request.build_absolute_uri()}"
	return render(request, 'detalle_evento.html', {'evento': evento, 'qr_bytes': qr_bytes, 'whatsapp_url': whatsapp_url})

def descargar_qr_png(request, event_id):
	from django.shortcuts import get_object_or_404
	evento = get_object_or_404(Event, id=event_id)
	qr_data = f"Evento: {evento.name}\nFecha: {evento.date}\nLugar: {evento.space}\nCiudad: {evento.ciudad}\nPaís: {evento.pais}"
	qr_img = qrcode.make(qr_data)
	buffer = io.BytesIO()
	qr_img.save(buffer, format='PNG')
	buffer.seek(0)
	return FileResponse(buffer, as_attachment=True, filename=f"evento_{evento.id}_qr.png")

def descargar_qr_pdf(request, event_id):
	from django.shortcuts import get_object_or_404
	evento = get_object_or_404(Event, id=event_id)
	qr_data = f"Evento: {evento.name}\nFecha: {evento.date}\nLugar: {evento.space}\nCiudad: {evento.ciudad}\nPaís: {evento.pais}"
	qr_img = qrcode.make(qr_data)
	img_buffer = io.BytesIO()
	qr_img.save(img_buffer, format='PNG')
	img_buffer.seek(0)
	pdf_buffer = io.BytesIO()
	c = canvas.Canvas(pdf_buffer, pagesize=letter)
	c.drawString(100, 700, f"Evento: {evento.name}")
	c.drawString(100, 680, f"Fecha: {evento.date}")
	c.drawString(100, 660, f"Lugar: {evento.space}")
	c.drawString(100, 640, f"Ciudad: {evento.ciudad}")
	c.drawString(100, 620, f"País: {evento.pais}")
	from reportlab.lib.utils import ImageReader
	c.drawImage(ImageReader(img_buffer), 100, 400, width=200, height=200)
	c.showPage()
	c.save()
	pdf_buffer.seek(0)
	return FileResponse(pdf_buffer, as_attachment=True, filename=f"evento_{evento.id}_qr.pdf")
def detalle_evento(request, event_id):
	import qrcode
	import io
	from django.core.files.base import ContentFile
	evento = get_object_or_404(Event, id=event_id)
	qr_data = f"Evento: {evento.name}\nFecha: {evento.date}\nLugar: {evento.ciudad}, {evento.pais}\nEntradas disponibles: {evento.available_seats}"
	qr_img = qrcode.make(qr_data)
	buf = io.BytesIO()
	qr_img.save(buf, format='PNG')
	qr_bytes = buf.getvalue()
	qr_base64 = qr_bytes.hex()
	return render(request, 'detalle_evento.html', {'evento': evento, 'qr_bytes': qr_bytes})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .models_ticket import Ticket
from .forms import EventForm
def crear_evento(request):
	if request.method == 'POST':
		form = EventForm(request.POST, request.FILES)
		if form.is_valid():
			evento = form.save(commit=False)
			# Asignar organizador actual si corresponde
			evento.organizer = request.user
			evento.save()
			return redirect('detalle_evento', event_id=evento.id)
	else:
		form = EventForm()
	return render(request, 'crear_evento.html', {'form': form})

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
