"""
URL configuration for kulture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users.views import login_view, signup_view, home, crear_usuarios_prueba, home_superusuario, logout_view, signup_artist, signup_evento, signup_space
from spaces.views import home_espacio_cultural, espacio_list, exportar_balance_pdf
from artists.views import home_artista, artist_list
from events.views import comprar_ticket, ticket_exito
from events.views import comprar_ticket, ticket_exito, lista_eventos
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('espacio/exportar-balance/', exportar_balance_pdf, name='exportar_balance_pdf'),
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('crear-usuarios-prueba/', crear_usuarios_prueba, name='crear_usuarios_prueba'),
    path('superusuario/', home_superusuario, name='home_superusuario'),
    path('logout/', logout_view, name='logout'),
    path('espacio/', home_espacio_cultural, name='home_espacio_cultural'),
    path('espacios/', espacio_list, name='espacio_list'),
    path('artista/', home_artista, name='home_artista'),
    path('artistas/', artist_list, name='artist_list'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('signup/artist/', signup_artist, name='signup_artist'),
    path('signup/evento/', signup_evento, name='signup_evento'),
    path('signup/space/', signup_space, name='signup_space'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('comprar-ticket/<int:event_id>/', comprar_ticket, name='comprar_ticket'),
    path('ticket-exito/<int:event_id>/', ticket_exito, name='ticket_exito'),
    path('eventos/', lista_eventos, name='lista_eventos'),
    path('blog/', include('blog.urls')),
]
