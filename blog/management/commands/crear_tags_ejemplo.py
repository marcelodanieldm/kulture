from django.core.management.base import BaseCommand
from blog.models import Tag

class Command(BaseCommand):
    help = 'Crea tags de ejemplo para el blog'

    def handle(self, *args, **kwargs):
        tags = ['Cultura', 'Música', 'Convocatoria', 'Festival', 'Arte', 'Noticias', 'Eventos', 'Recomendado', 'Entrevista', 'Tendencia']
        for name in tags:
            Tag.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('Tags de ejemplo creados.'))
