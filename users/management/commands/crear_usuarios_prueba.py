from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Crea usuarios de prueba para Kulture'

    def handle(self, *args, **kwargs):
        usuarios = [
            {
                'username': 'evento',
                'email': 'evento@kulture.com',
                'password': 'evento123',
                'user_type': 'evento',
                'city': 'Ciudad Evento',
                'country': 'EventoLand',
            },
            {
                'username': 'espacio',
                'email': 'espacio@kulture.com',
                'password': 'espacio123',
                'user_type': 'space',
                'city': 'Ciudad Espacio',
                'country': 'EspacioLand',
            },
            {
                'username': 'admin',
                'email': 'admin@kulture.com',
                'password': 'admin123',
                'is_superuser': True,
                'is_staff': True,
                'user_type': 'admin',
                'city': 'Ciudad Admin',
                'country': 'AdminLand',
            },
            {
                'username': 'artista',
                'email': 'artista@kulture.com',
                'password': 'artista123',
                'user_type': 'artist',
                'city': 'Ciudad Artista',
                'country': 'ArtistaLand',
            },
            {
                'username': 'colaborador',
                'email': 'colaborador@kulture.com',
                'password': 'colaborador123',
                'user_type': 'colaborador',
                'city': 'Ciudad Colaborador',
                'country': 'ColaboradorLand',
            },
        ]
        for u in usuarios:
            if CustomUser.objects.filter(username=u['username']).exists():
                self.stdout.write(self.style.WARNING(f"El usuario {u['username']} ya existe."))
                continue
            if u.get('is_superuser'):
                user = CustomUser.objects.create_superuser(
                    username=u['username'],
                    email=u['email'],
                    password=u['password'],
                    city=u['city'],
                    country=u['country'],
                    user_type=u['user_type'],
                )
            else:
                user = CustomUser.objects.create_user(
                    username=u['username'],
                    email=u['email'],
                    password=u['password'],
                    city=u['city'],
                    country=u['country'],
                    user_type=u['user_type'],
                )
            if u.get('is_staff'):
                user.is_staff = True
                user.save()
            self.stdout.write(self.style.SUCCESS(f"Usuario {u['username']} creado."))
