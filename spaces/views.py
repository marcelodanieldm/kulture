from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def exportar_balance_pdf(request):
	# Obtener datos del balance económico
	space_profile = SpaceProfile.objects.filter(user=request.user).first()
	eventos = Event.objects.filter(space=space_profile)
	import calendar
	from collections import defaultdict
	balance_mensual = []
	eventos_por_mes = defaultdict(list)
	for evento in eventos:
		mes = evento.date.strftime('%Y-%m')
		eventos_por_mes[mes].append(evento)
	for mes, eventos_mes in eventos_por_mes.items():
		nombre_mes = calendar.month_name[int(mes.split('-')[1])] + ' ' + mes.split('-')[0]
		entradas_vendidas = sum(e.total_seats - e.available_seats for e in eventos_mes)
		asistentes = entradas_vendidas
		lugares_libres = sum(e.available_seats for e in eventos_mes)
		gastos = sum(sum(exp.amount for exp in Expense.objects.filter(event=e)) for e in eventos_mes)
		ganancia_neta = sum((e.price * (e.total_seats - e.available_seats)) for e in eventos_mes) - gastos
		balance_mensual.append({
			'nombre': nombre_mes,
			'entradas_vendidas': entradas_vendidas,
			'asistentes': asistentes,
			'lugares_libres': lugares_libres,
			'gastos': gastos,
			'ganancia_neta': ganancia_neta
		})
	# Generar PDF
	buffer = io.BytesIO()
	p = canvas.Canvas(buffer, pagesize=letter)
	p.setFont("Helvetica-Bold", 16)
	p.drawString(50, 750, "Balance Económico")
	y = 720
	p.setFont("Helvetica", 11)
	for mes in balance_mensual:
		p.drawString(50, y, f"{mes['nombre']}: Entradas vendidas: {mes['entradas_vendidas']}, Asistentes: {mes['asistentes']}, Libres: {mes['lugares_libres']}, Gastos: ${mes['gastos']}, Ganancia neta: ${mes['ganancia_neta']}")
		y -= 22
		if y < 60:
			p.showPage()
			y = 750
	p.save()
	buffer.seek(0)
	return HttpResponse(buffer, content_type='application/pdf')
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
def espacio_list(request):
	espacios = SpaceProfile.objects.all()
	ciudad = request.GET.get('ciudad', '')
	pais = request.GET.get('pais', '')
	actividades = request.GET.get('actividades', '')
	puntaje_min = request.GET.get('puntaje_min', '')
	puntaje_max = request.GET.get('puntaje_max', '')

	if ciudad:
		espacios = espacios.filter(ciudad__icontains=ciudad)
	if pais:
		espacios = espacios.filter(pais__icontains=pais)
	if actividades == 'paga':
		espacios = espacios.filter(actividades__icontains='paga')
	elif actividades == 'gratuita':
		espacios = espacios.filter(actividades__icontains='gratuita')
	if puntaje_min:
		espacios = espacios.filter(puntaje__gte=puntaje_min)
	if puntaje_max:
		espacios = espacios.filter(puntaje__lte=puntaje_max)

	paginator = Paginator(espacios, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'espacio_list.html', {
		'espacios': page_obj.object_list,
		'page_obj': page_obj,
		'ciudad': ciudad,
		'pais': pais,
		'actividades': actividades,
		'puntaje_min': puntaje_min,
		'puntaje_max': puntaje_max,
	})
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .models import SpaceProfile
from events.models import Event
from events.models_ticket import Ticket
from events.models_expense import Expense

@login_required
def home_espacio_cultural(request):
	# Validar usuario y obtener perfil antes de usarlo
	if not hasattr(request.user, 'user_type') or request.user.user_type != 'space':
		return redirect('home')
	space_profile = SpaceProfile.objects.filter(user=request.user).first()
	if not space_profile:
		return redirect('home')
	# Balance económico mensual
	import calendar
	from collections import defaultdict
	from events.models import Event
	balance_mensual = []
	eventos_por_mes = defaultdict(list)
	eventos = Event.objects.filter(space=space_profile)
	for evento in eventos:
		mes = evento.date.strftime('%Y-%m')
		eventos_por_mes[mes].append(evento)
	for mes, eventos_mes in eventos_por_mes.items():
		nombre_mes = calendar.month_name[int(mes.split('-')[1])] + ' ' + mes.split('-')[0]
		entradas_vendidas = sum(e.total_seats - e.available_seats for e in eventos_mes)
		asistentes = entradas_vendidas  # Asumimos 1 entrada = 1 asistente
		lugares_libres = sum(e.available_seats for e in eventos_mes)
		gastos = sum(sum(exp.amount for exp in Expense.objects.filter(event=e)) for e in eventos_mes)
		ganancia_neta = sum((e.price * (e.total_seats - e.available_seats)) for e in eventos_mes) - gastos
		balance_mensual.append({
			'nombre': nombre_mes,
			'entradas_vendidas': entradas_vendidas,
			'asistentes': asistentes,
			'lugares_libres': lugares_libres,
			'gastos': gastos,
			'ganancia_neta': ganancia_neta
		})
	from django.core.paginator import Paginator
	eventos = Event.objects.filter(space=space_profile)
	eventos_por_venir_qs = eventos.filter(date__gte=timezone.now()).order_by('date')
	paginator = Paginator(eventos_por_venir_qs, 5)
	page_number = request.GET.get('page')
	eventos_por_venir = paginator.get_page(page_number)
	sala_llena = space_profile.is_full if space_profile else False
	# Ventas y balance
	tickets = Ticket.objects.filter(event__space=space_profile)
	expenses = Expense.objects.filter(event__space=space_profile)
	total_ventas = sum(t.amount_paid for t in tickets)
	total_gastos = sum(e.amount for e in expenses)
	total_ganancia = total_ventas - total_gastos
	if request.method == 'POST' and space_profile:
		if 'add_expense' in request.POST:
			concept = request.POST.get('concept')
			amount = request.POST.get('amount')
			if concept and amount:
				event = eventos.first() if eventos.exists() else None
				if event:
					Expense.objects.create(event=event, concept=concept, amount=amount)
		elif 'nombre' in request.POST:
			nombre = request.POST.get('nombre')
			descripcion = request.POST.get('descripcion')
			fecha_hora = request.POST.get('fecha_hora')
			horario = request.POST.get('horario')
			duracion = request.POST.get('duracion')
			precio = request.POST.get('precio')
			moneda = request.POST.get('moneda')
			codigo_promocion = request.POST.get('codigo_promocion')
			porcentaje_descuento = request.POST.get('porcentaje_descuento')
			comentario_novedades = request.POST.get('comentario_novedades')
			cantidad_entradas = request.POST.get('cantidad_entradas')
			categoria_arte = request.POST.get('categoria_arte')
			ciudad = request.POST.get('ciudad')
			pais = request.POST.get('pais')
			tags = request.POST.get('tags')
			fotos = request.FILES.get('fotos')
			from events.models import Event
			event = Event.objects.create(
				name=nombre,
				organizer=request.user,
				space=space_profile,
				date=fecha_hora,
				horario=horario,
				description=descripcion,
				total_seats=cantidad_entradas or 0,
				available_seats=cantidad_entradas or 0,
				price=precio or 0,
				fotos=fotos,
				tags=tags,
				categoria_arte=categoria_arte,
				ciudad=ciudad,
				pais=pais,
				codigo_promocion=codigo_promocion,
				porcentaje_descuento=porcentaje_descuento or 0,
				comentario_novedades=comentario_novedades,
			)
			# Generar QR y URLs
			import qrcode
			from io import BytesIO
			import base64
			qr_data = f"Evento: {nombre}\nLugar: {space_profile.user.username}\nFecha: {fecha_hora}\nEntradas: {cantidad_entradas}"
			qr_img = qrcode.make(qr_data)
			buffer = BytesIO()
			qr_img.save(buffer, format="PNG")
			qr_png = base64.b64encode(buffer.getvalue()).decode()
			event.qr_url = f"data:image/png;base64,{qr_png}"
			# Para PDF, se puede usar una librería como reportlab (no implementado aquí)
			event.qr_url_png = event.qr_url
			event.qr_url_pdf = "#"  # Placeholder
			evento_creado = event
			return render(request, 'home_espacio_cultural.html', {
				'space': space_profile,
				'eventos': eventos,
				'sala_llena': sala_llena,
				'tickets': tickets,
				'expenses': expenses,
				'total_ventas': total_ventas,
				'total_ganancia': total_ganancia,
				'evento_creado': evento_creado
			})
		else:
			total_seats = int(request.POST.get('total_seats', space_profile.total_seats))
			space_profile.total_seats = total_seats
			space_profile.available_seats = int(request.POST.get('available_seats', space_profile.available_seats))
			space_profile.save()
	return render(request, 'home_espacio_cultural.html', {
	'space': space_profile,
	'eventos': eventos,
	'sala_llena': sala_llena,
	'tickets': tickets,
	'expenses': expenses,
	'total_ventas': total_ventas,
	'total_ganancia': total_ganancia,
	'eventos_por_venir': eventos_por_venir,
	'balance_mensual': balance_mensual
	})
