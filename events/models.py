from django.db import models

# Create your models here.
# events/models.py

from django.db import models
from users.models import CustomUser
from spaces.models import SpaceProfile
from artists.models import ArtistProfile

class Event(models.Model):
    horario = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=200)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    space = models.ForeignKey(SpaceProfile, on_delete=models.CASCADE, null=True, blank=True)
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    description = models.TextField()
    sectors = models.JSONField(default=list)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fotos = models.ImageField(upload_to='eventos/', blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True)
    categoria_arte = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, blank=True)
    codigo_promocion = models.CharField(max_length=50, blank=True)
    porcentaje_descuento = models.PositiveIntegerField(default=0)
    comentario_novedades = models.TextField(blank=True)

    @property
    def is_full(self):
        return self.available_seats <= 0

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name