from django.core.management.base import BaseCommand
import random

# Comando para crear artistas de ejemplo
class Command(BaseCommand):
    help = 'Crea artistas de ejemplo para pruebas'

    def handle(self, *args, **options):
        from users.models import CustomUser
        from artists.models import ArtistProfile
        ciudades = ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'La Plata']
        paises = ['Argentina', 'Uruguay', 'Chile', 'Brasil', 'Paraguay']
        tipos_arte = [
            ['Musica'], ['Teatro'], ['Danza'], ['Literatura'], ['Artes Visuales'],
            ['Musica', 'Teatro'], ['Danza', 'Artes Visuales']
        ]
        for i in range(1, 16):
            username = f'artista{i}'
            if not CustomUser.objects.filter(username=username).exists():
                user = CustomUser.objects.create_user(
                    username=username,
                    password='test1234',
                    user_type='artist',
                    city=random.choice(ciudades),
                    country=random.choice(paises),
                )
                ArtistProfile.objects.create(
                    user=user,
                    description=f'Artista {username} especializado en {", ".join(random.choice(tipos_arte))}.',
                    sectors=random.choice(tipos_arte),
                    website='',
                    ranking=round(random.uniform(2.5, 5.0), 2),
                )
        self.stdout.write(self.style.SUCCESS('Artistas de ejemplo creados.'))
from django.db import models

# Create your models here.
# artists/models.py

from django.db import models
from users.models import CustomUser

class ArtistProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, default="")
    apellido_grupo = models.CharField(max_length=100, default="")
    ciudad = models.CharField(max_length=100, default="")
    pais = models.CharField(max_length=100, default="")
    SECTORES_CHOICES = [
        ('Pintura', 'Pintura'),
        ('Escultura', 'Escultura'),
        ('Arquitectura', 'Arquitectura'),
        ('Musica', 'Música'),
        ('Danza', 'Danza'),
        ('Literatura', 'Literatura'),
        ('Cine', 'Cine'),
        ('Teatro', 'Teatro'),
        ('Otros', 'Otros'),
    ]
    sectores = models.JSONField(default=list)  # Ej: ["Musica", "Teatro"]
    descripcion = models.TextField(blank=True)
    foto = models.ImageField(upload_to='artistas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_grupo}" if self.nombre else self.user.username
