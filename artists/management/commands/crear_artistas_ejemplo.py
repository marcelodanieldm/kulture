from django.core.management.base import BaseCommand
from users.models import CustomUser
from artists.models import ArtistProfile
import random

class Command(BaseCommand):
    help = 'Crea artistas de ejemplo para pruebas'

    def handle(self, *args, **options):
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
