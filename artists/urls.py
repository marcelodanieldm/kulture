from django.urls import path
from .views import home_artista, artist_list, api_eventos_list, api_eventos_create, api_eventos_edit, api_eventos_delete, api_gastos_list, api_gastos_create

urlpatterns = [
    path('', home_artista, name='home_artista'),
    path('list/', artist_list, name='artist_list'),
    path('api/eventos/', api_eventos_list, name='api_eventos_list'),
    path('api/eventos/create/', api_eventos_create, name='api_eventos_create'),
    path('api/eventos/<int:event_id>/edit/', api_eventos_edit, name='api_eventos_edit'),
    path('api/eventos/<int:event_id>/delete/', api_eventos_delete, name='api_eventos_delete'),
    path('api/gastos/', api_gastos_list, name='api_gastos_list'),
    path('api/gastos/create/', api_gastos_create, name='api_gastos_create'),
]
