from django.core.management.base import BaseCommand
from django.conf import settings
import random
# Comando para crear datos de ejemplo
class Command(BaseCommand):
    help = 'Crea espacios de ejemplo para pruebas'

    def handle(self, *args, **options):
        from users.models import CustomUser
        from spaces.models import SpaceProfile
        ciudades = ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'La Plata']
        paises = ['Argentina', 'Uruguay', 'Chile', 'Brasil', 'Paraguay']
        actividades_lista = [
            'Teatro, Música, Danza',
            'Exposiciones, Charlas',
            'Cine, Talleres',
            'Conciertos, Ferias',
            'Arte, Literatura',
        ]
        for i in range(1, 16):
            username = f'espacio{i}'
            if not CustomUser.objects.filter(username=username).exists():
                user = CustomUser.objects.create_user(
                    username=username,
                    password='test1234',
                    user_type='space',
                    city=random.choice(ciudades),
                    country=random.choice(paises),
                )
                SpaceProfile.objects.create(
                    user=user,
                    description=f'Este es el espacio cultural {username} dedicado a {random.choice(actividades_lista)}.',
                    members='Juan, Ana, Pedro',
                    sectors=["Sala Principal", "Auditorio"],
                    total_seats=random.randint(50, 300),
                    available_seats=random.randint(10, 200),
                )
        self.stdout.write(self.style.SUCCESS('Espacios de ejemplo creados.'))
from django.db import models

# Create your models here.
# spaces/models.py

from django.db import models
from users.models import CustomUser

class SpaceProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    members = models.TextField()  # Puede ser JSONField si se quiere estructura
    sectors = models.JSONField(default=list)
    total_seats = models.PositiveIntegerField(default=0)
    available_seats = models.PositiveIntegerField(default=0)
    foto = models.ImageField(upload_to='espacios/', blank=True, null=True)

    @property
    def is_full(self):
        return self.available_seats <= 0

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo en creación
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
