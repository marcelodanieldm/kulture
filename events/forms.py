from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'description', 'fotos', 'tags', 'categoria_arte', 'ciudad', 'pais',
            'date', 'horario', 'total_seats', 'price', 'codigo_promocion', 'porcentaje_descuento', 'comentario_novedades',
            'fecha_publicacion_inicio', 'fecha_publicacion_fin'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'horario': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_publicacion_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_publicacion_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'comentario_novedades': forms.Textarea(attrs={'rows': 2}),
        }
