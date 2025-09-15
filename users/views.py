from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('admin:index')
		else:
			return render(request, 'login.html', {'error': 'Credenciales inválidas'})
	return render(request, 'login.html')


from django.contrib.auth.models import User
from django.contrib import messages

def signup_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		if User.objects.filter(username=username).exists():
			return render(request, 'signup.html', {'error': 'El usuario ya existe'})
		user = User.objects.create_user(username=username, email=email, password=password)
		user.save()
		messages.success(request, 'Usuario creado exitosamente. Inicia sesión.')
		return redirect('login')
	return render(request, 'signup.html')


def home(request):
	return render(request, 'home.html')
