from django.core.management.base import BaseCommand
from users.models import CustomUser
from spaces.models import SpaceProfile
import random

class Command(BaseCommand):
    help = 'Crea espacios de ejemplo para pruebas'

    def handle(self, *args, **options):
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
                        foto=None,
                )
        self.stdout.write(self.style.SUCCESS('Espacios de ejemplo creados.'))
