from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Dashboard para usuarios tipo colaborador
@login_required
def home_colaborador(request):
	return render(request, 'home_colaborador.html', {})
def signup_artist(request):
	from artists.models import ArtistProfile
	if request.method == 'POST':
		nombre = request.POST.get('nombre', '').strip()
		ciudad = request.POST.get('ciudad', '').strip()
		pais = request.POST.get('pais', '').strip()
		redes = request.POST.get('redes', '').strip()
		sectores = request.POST.getlist('sector')
		foto = request.FILES.get('foto')
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '').strip()
		errors = {}
		# Validaciones avanzadas
		if not nombre or len(nombre) < 3:
			errors['nombre'] = 'El nombre debe tener al menos 3 caracteres.'
		if not ciudad:
			errors['ciudad'] = 'La ciudad es obligatoria.'
		if not pais:
			errors['pais'] = 'El país es obligatorio.'
		if not email or '@' not in email or CustomUser.objects.filter(email=email).exists():
			errors['email'] = 'Email inválido o ya registrado.'
		if not password:
			errors['password'] = 'La contraseña es obligatoria.'
		if not sectores:
			errors['sectores'] = 'Debes seleccionar al menos un tipo de arte.'
		username = nombre.lower().replace(' ', '_')
		if CustomUser.objects.filter(username=username).exists():
			errors['username'] = 'El usuario ya existe.'
		if errors:
			return render(request, 'signup_artist.html', {'errors': errors, 'nombre': nombre, 'ciudad': ciudad, 'pais': pais, 'redes': redes, 'sectores': sectores, 'email': email})
		user = CustomUser.objects.create_user(
			username=username,
			user_type='artist',
			city=ciudad,
			country=pais,
			email=email,
			password=password,
		)
		profile = ArtistProfile.objects.create(
			user=user,
			nombre=nombre,
			apellido_grupo='',
			ciudad=ciudad,
			pais=pais,
			sectores=sectores,
			descripcion=redes,
			foto=foto
		)
		return redirect('login')
	return render(request, 'signup_artist.html')

def signup_evento(request):
	from events.models import Event
	if request.method == 'POST':
		nombre = request.POST.get('nombre', '').strip()
		ciudad = request.POST.get('ciudad', '').strip()
		pais = request.POST.get('pais', '').strip()
		sectores = request.POST.getlist('sector')
		descripcion = request.POST.get('descripcion', '').strip()
		capacidad = request.POST.get('capacidad', '').strip()
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '').strip()
		errors = {}
		if not nombre or len(nombre) < 3:
			errors['nombre'] = 'El nombre debe tener al menos 3 caracteres.'
		if not ciudad:
			errors['ciudad'] = 'La ciudad es obligatoria.'
		if not pais:
			errors['pais'] = 'El país es obligatorio.'
		if not email or '@' not in email or CustomUser.objects.filter(email=email).exists():
			errors['email'] = 'Email inválido o ya registrado.'
		if not password:
			errors['password'] = 'La contraseña es obligatoria.'
		if not sectores:
			errors['sectores'] = 'Debes seleccionar al menos un tipo de arte.'
		if not descripcion or len(descripcion) < 10:
			errors['descripcion'] = 'La descripción debe tener al menos 10 caracteres.'
		if not capacidad or not capacidad.isdigit() or int(capacidad) < 1:
			errors['capacidad'] = 'La capacidad debe ser un número mayor a 0.'
		username = nombre.lower().replace(' ', '_')
		if CustomUser.objects.filter(username=username).exists():
			errors['username'] = 'El usuario ya existe.'
		if errors:
			return render(request, 'signup_evento.html', {'errors': errors, 'nombre': nombre, 'ciudad': ciudad, 'pais': pais, 'sectores': sectores, 'descripcion': descripcion, 'capacidad': capacidad, 'email': email})
		user = CustomUser.objects.create_user(
			username=username,
			user_type='evento',
			city=ciudad,
			country=pais,
			email=email,
			password=password,
		)
		event = Event.objects.create(
			name=nombre,
			organizer=user,
			description=descripcion,
			sectors=sectores,
			total_seats=int(capacidad),
			available_seats=int(capacidad),
		)
		return redirect('login')
	return render(request, 'signup_evento.html')

def signup_space(request):
	from spaces.models import SpaceProfile
	if request.method == 'POST':
		nombre = request.POST.get('nombre', '').strip()
		ciudad = request.POST.get('ciudad', '').strip()
		pais = request.POST.get('pais', '').strip()
		descripcion = request.POST.get('descripcion', '').strip()
		sectores = request.POST.getlist('sector')
		redes = request.POST.get('redes', '').strip()
		capacidad = request.POST.get('capacidad', '').strip()
		foto = request.FILES.get('foto')
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '').strip()
		errors = {}
		if not nombre or len(nombre) < 3:
			errors['nombre'] = 'El nombre debe tener al menos 3 caracteres.'
		if not ciudad:
			errors['ciudad'] = 'La ciudad es obligatoria.'
		if not pais:
			errors['pais'] = 'El país es obligatorio.'
		if not email or '@' not in email or CustomUser.objects.filter(email=email).exists():
			errors['email'] = 'Email inválido o ya registrado.'
		if not password:
			errors['password'] = 'La contraseña es obligatoria.'
		if not sectores:
			errors['sectores'] = 'Debes seleccionar al menos un tipo de arte.'
		if not descripcion or len(descripcion) < 10:
			errors['descripcion'] = 'La descripción debe tener al menos 10 caracteres.'
		if not capacidad or not capacidad.isdigit() or int(capacidad) < 1:
			errors['capacidad'] = 'La capacidad debe ser un número mayor a 0.'
		username = nombre.lower().replace(' ', '_')
		if CustomUser.objects.filter(username=username).exists():
			errors['username'] = 'El usuario ya existe.'
		if errors:
			return render(request, 'signup_space.html', {'errors': errors, 'nombre': nombre, 'ciudad': ciudad, 'pais': pais, 'sectores': sectores, 'descripcion': descripcion, 'redes': redes, 'capacidad': capacidad, 'email': email})
		user = CustomUser.objects.create_user(
			username=username,
			user_type='space',
			city=ciudad,
			country=pais,
			email=email,
			password=password,
		)
		profile = SpaceProfile.objects.create(
			user=user,
			description=descripcion + '\nRedes: ' + redes,
			members='',
			sectors=sectores,
			total_seats=int(capacidad),
			available_seats=int(capacidad),
			foto=foto
		)
		return redirect('login')
	return render(request, 'signup_space.html')
from django.contrib.auth import logout
def logout_view(request):
	logout(request)
	return redirect('home')
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
@login_required
@user_passes_test(lambda u: u.is_superuser)
def home_superusuario(request):
	return render(request, 'home_superusuario.html')
from django.http import HttpResponse
from .models import CustomUser

def crear_usuarios_prueba(request):
	usuarios = [
		{'username': 'evento', 'email': 'evento@kulture.com', 'password': 'evento123', 'user_type': 'super'},
		{'username': 'espacio', 'email': 'espacio@kulture.com', 'password': 'espacio123', 'user_type': 'space'},
		{'username': 'admin', 'email': 'admin@kulture.com', 'password': 'admin123', 'user_type': 'super', 'is_staff': True, 'is_superuser': True},
		{'username': 'artista', 'email': 'artista@kulture.com', 'password': 'artista123', 'user_type': 'artist'},
		{'username': 'colaborador', 'email': 'colaborador@kulture.com', 'password': 'colaborador123', 'user_type': 'collaborator'},
	]
	for u in usuarios:
		if not CustomUser.objects.filter(username=u['username']).exists():
			CustomUser.objects.create_user(**u)
	return HttpResponse('Usuarios de prueba creados exitosamente.')
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

@csrf_protect
def login_view(request):
	if request.method == 'POST':
		identifier = request.POST.get('identifier')
		password = request.POST.get('password')
		# Buscar usuario por email o username
		from django.contrib.auth import get_user_model
		UserModel = get_user_model()
		user_obj = None
		if '@' in identifier:
			try:
				user_obj = UserModel.objects.get(email=identifier)
				username = user_obj.username
			except UserModel.DoesNotExist:
				username = None
		else:
			username = identifier
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if user.is_superuser:
				return redirect('home_superusuario')
			elif hasattr(user, 'user_type'):
				if user.user_type == 'artist':
					return redirect('home_artista')
				elif user.user_type == 'space':
					return redirect('home_espacio_cultural')
				elif user.user_type == 'collaborator':
					return redirect('home_colaborador')
				elif user.user_type == 'evento':
					return redirect('home_evento')
			return redirect('admin:index')
		else:
			return render(request, 'login.html', {'error': 'Credenciales inválidas'})
	return render(request, 'login.html')


from django.contrib.auth.models import User
from django.contrib import messages

def signup_view(request):
	if request.method == 'POST':
		user_type = request.POST.get('user_type')
		if user_type == 'artist':
			return redirect('signup_artist')
		elif user_type == 'evento':
			return redirect('signup_evento')
		elif user_type == 'space':
			return redirect('signup_space')
		else:
			return render(request, 'signup.html', {'error': 'Debes seleccionar una categoría.'})
	return render(request, 'signup.html')


def home(request):
	return render(request, 'home.html')
