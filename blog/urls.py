from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('colaborador/', views.home_colaborador, name='home_colaborador'),
    path('colaborador/nuevo/', views.post_create, name='post_create'),
    path('colaborador/editar/<int:post_id>/', views.post_update, name='post_update'),
    path('colaborador/eliminar/<int:post_id>/', views.post_delete, name='post_delete'),
]
