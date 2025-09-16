
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

# API: Listar eventos del artista
@login_required
def api_eventos_list(request):
	artist_profile = ArtistProfile.objects.filter(user=request.user).first()
	eventos = Event.objects.filter(artist=artist_profile)
	data = [
		{
			'id': e.id,
			'name': e.name,
			'date': str(e.date),
			'description': e.description,
			'price': float(e.price),
			'seats': e.total_seats
		} for e in eventos
	]
	return JsonResponse({'eventos': data})

# API: Crear evento
@csrf_exempt
@login_required
def api_eventos_create(request):
	if request.method == 'POST':
		artist_profile = ArtistProfile.objects.filter(user=request.user).first()
		data = json.loads(request.body)
		name = data.get('name')
		date = data.get('date')
		description = data.get('description')
		price = data.get('price', 0)
		seats = data.get('seats')
		if name and date and seats:
			e = Event.objects.create(
				name=name,
				artist=artist_profile,
				date=date,
				description=description,
				price=price or 0,
				total_seats=seats,
				available_seats=seats
			)
			return JsonResponse({'success': True, 'id': e.id})
	return JsonResponse({'success': False})

# API: Editar evento
@csrf_exempt
@login_required
def api_eventos_edit(request, event_id):
	if request.method == 'POST':
		artist_profile = ArtistProfile.objects.filter(user=request.user).first()
		event = Event.objects.filter(id=event_id, artist=artist_profile).first()
		if event:
			data = json.loads(request.body)
			event.name = data.get('name', event.name)
			event.date = data.get('date', event.date)
			event.description = data.get('description', event.description)
			event.price = data.get('price', event.price)
			event.total_seats = data.get('seats', event.total_seats)
			event.available_seats = data.get('seats', event.available_seats)
			event.save()
			return JsonResponse({'success': True})
	return JsonResponse({'success': False})

# API: Eliminar evento
@csrf_exempt
@login_required
def api_eventos_delete(request, event_id):
	if request.method == 'POST':
		artist_profile = ArtistProfile.objects.filter(user=request.user).first()
		Event.objects.filter(id=event_id, artist=artist_profile).delete()
		return JsonResponse({'success': True})
	return JsonResponse({'success': False})

# API: Listar gastos
@login_required
def api_gastos_list(request):
	artist_profile = ArtistProfile.objects.filter(user=request.user).first()
	expenses = Expense.objects.filter(event__artist=artist_profile)
	data = [
		{
			'id': e.id,
			'concept': e.concept,
			'amount': float(e.amount),
			'date': str(e.date)
		} for e in expenses
	]
	return JsonResponse({'expenses': data})

# API: Crear gasto
@csrf_exempt
@login_required
def api_gastos_create(request):
	if request.method == 'POST':
		artist_profile = ArtistProfile.objects.filter(user=request.user).first()
		eventos = Event.objects.filter(artist=artist_profile)
		event = eventos.first() if eventos.exists() else None
		data = json.loads(request.body)
		concept = data.get('concept')
		amount = data.get('amount')
		if concept and amount and event:
			e = Expense.objects.create(event=event, concept=concept, amount=amount)
			return JsonResponse({'success': True, 'id': e.id})
	return JsonResponse({'success': False})
from django.core.paginator import Paginator
def artist_list(request):
	artistas = ArtistProfile.objects.all()
	tipo_arte = request.GET.get('tipo_arte', '')
	ranking_min = request.GET.get('ranking_min', '')
	ranking_max = request.GET.get('ranking_max', '')
	ciudad = request.GET.get('ciudad', '')
	pais = request.GET.get('pais', '')

	if tipo_arte:
		artistas = artistas.filter(sectors__contains=[tipo_arte])
	if ranking_min:
		artistas = artistas.filter(ranking__gte=ranking_min)
	if ranking_max:
		artistas = artistas.filter(ranking__lte=ranking_max)
	if ciudad:
		artistas = artistas.filter(user__city__icontains=ciudad)
	if pais:
		artistas = artistas.filter(user__country__icontains=pais)

	paginator = Paginator(artistas, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'artist_list.html', {
		'artistas': page_obj.object_list,
		'page_obj': page_obj,
		'tipo_arte': tipo_arte,
		'ranking_min': ranking_min,
		'ranking_max': ranking_max,
		'ciudad': ciudad,
		'pais': pais,
	})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .models import ArtistProfile
from events.models import Event
from events.models_ticket import Ticket
from events.models_expense import Expense

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@login_required(login_url='/login/')
def home_artista(request):
	edit_event = None
	edit_blog_idx = None
	edit_blog_value = ''
	if not hasattr(request.user, 'user_type') or request.user.user_type != 'artist':
		return redirect('home')
	artist_profile = ArtistProfile.objects.filter(user=request.user).first()
	blog = request.session.get('artist_blog', [])
	# Detectar edición de evento
	if request.method == 'GET' and 'edit_event' in request.GET:
		event_id = request.GET.get('edit_event')
		edit_event = Event.objects.filter(id=event_id, artist=artist_profile).first()
	# Detectar edición de anuncio
	if request.method == 'GET' and 'edit_blog' in request.GET:
		edit_blog_idx = int(request.GET.get('edit_blog'))
		if 0 <= edit_blog_idx < len(blog):
			edit_blog_value = blog[edit_blog_idx]
	# Blog CRUD
	if request.method == 'POST':
		if 'description' in request.POST and artist_profile:
			artist_profile.description = request.POST.get('description', artist_profile.description)
			artist_profile.save()
		if 'blog_post' in request.POST:
			blog.append(request.POST['blog_post'])
			request.session['artist_blog'] = blog
		if 'delete_blog' in request.POST:
			idx = int(request.POST['delete_blog'])
			if 0 <= idx < len(blog):
				blog.pop(idx)
				request.session['artist_blog'] = blog
		if 'edit_blog_idx' in request.POST:
			idx = int(request.POST['edit_blog_idx'])
			new_value = request.POST.get('edit_blog_value')
			if 0 <= idx < len(blog):
				blog[idx] = new_value
				request.session['artist_blog'] = blog
		# Crear evento
		if 'new_event' in request.POST:
			name = request.POST.get('event_name')
			date = request.POST.get('event_date')
			description = request.POST.get('event_description')
			price = request.POST.get('event_price')
			seats = request.POST.get('event_seats')
			if name and date and seats:
				Event.objects.create(
					name=name,
					artist=artist_profile,
					date=date,
					description=description,
					price=price or 0,
					total_seats=seats,
					available_seats=seats
				)
		# Eliminar evento
		if 'delete_event' in request.POST:
			event_id = request.POST.get('delete_event')
			Event.objects.filter(id=event_id, artist=artist_profile).delete()
		# Editar evento
		if 'edit_event_id' in request.POST:
			event_id = request.POST.get('edit_event_id')
			event = Event.objects.filter(id=event_id, artist=artist_profile).first()
			if event:
				event.name = request.POST.get('event_name', event.name)
				event.date = request.POST.get('event_date', event.date)
				event.description = request.POST.get('event_description', event.description)
				event.price = request.POST.get('event_price', event.price)
				event.total_seats = request.POST.get('event_seats', event.total_seats)
				event.available_seats = request.POST.get('event_seats', event.available_seats)
				event.save()
	eventos = Event.objects.filter(artist=artist_profile)
	# Ventas y balance
	tickets = Ticket.objects.filter(event__artist=artist_profile)
	expenses = Expense.objects.filter(event__artist=artist_profile)
	total_ventas = sum(t.amount_paid for t in tickets)
	total_gastos = sum(e.amount for e in expenses)
	total_ganancia = total_ventas - total_gastos
	if request.method == 'POST':
		if 'add_expense' in request.POST:
			concept = request.POST.get('concept')
			amount = request.POST.get('amount')
			if concept and amount:
				event = eventos.first() if eventos.exists() else None
				if event:
					Expense.objects.create(event=event, concept=concept, amount=amount)
	return render(request, 'home_artista.html', {
		'artist': artist_profile,
		'eventos': eventos,
		'blog': blog,
		'edit_event': edit_event,
		'edit_blog_idx': edit_blog_idx,
		'edit_blog_value': edit_blog_value,
		'tickets': tickets,
		'expenses': expenses,
		'total_ventas': total_ventas,
		'total_ganancia': total_ganancia
	})
