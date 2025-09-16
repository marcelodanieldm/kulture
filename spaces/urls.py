from django.urls import path
from . import views

urlpatterns = [
    # ...otros endpoints...
    path('exportar_balance_pdf/', views.exportar_balance_pdf, name='exportar_balance_pdf'),
]
