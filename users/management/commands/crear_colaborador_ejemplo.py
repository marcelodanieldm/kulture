from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Crea un usuario colaborador de ejemplo'

    def handle(self, *args, **kwargs):
        if CustomUser.objects.filter(username='colaborador_demo').exists():
            self.stdout.write(self.style.WARNING('El usuario colaborador_demo ya existe.'))
            return
        user = CustomUser.objects.create_user(
            username='colaborador_demo',
            email='colaborador@demo.com',
            password='demo1234',
            user_type='colaborador',
            city='Ciudad Demo',
            country='DemoLand'
        )
        self.stdout.write(self.style.SUCCESS('Usuario colaborador_demo creado.'))
