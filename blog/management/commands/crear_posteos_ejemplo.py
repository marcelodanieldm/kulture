from django.core.management.base import BaseCommand
from blog.models import Post, BlogCategory
from users.models import CustomUser
from django.utils import timezone

class Command(BaseCommand):
    help = 'Crea posteos de ejemplo para el blog'

    def handle(self, *args, **kwargs):
        # Crear categorías si no existen
        cat_noticias, _ = BlogCategory.objects.get_or_create(name='Noticias')
        cat_eventos, _ = BlogCategory.objects.get_or_create(name='Eventos')
        cat_cultura, _ = BlogCategory.objects.get_or_create(name='Cultura')

        # Buscar un colaborador
        colaborador = CustomUser.objects.filter(user_type='colaborador').first()
        if not colaborador:
            self.stdout.write(self.style.ERROR('No hay usuario colaborador.'))
            return

        # Crear posteos
        posts = [
            {
                'title': 'Bienvenidos al Blog Kulture',
                'content': 'Este es el primer post de nuestro blog, donde compartiremos novedades y noticias culturales.',
                'category': cat_noticias,
            },
            {
                'title': 'Nuevo evento: Festival de Música',
                'content': 'El Festival de Música se realizará el próximo mes. ¡No te lo pierdas! Más info en la sección eventos.',
                'category': cat_eventos,
            },
            {
                'title': 'Convocatoria abierta para artistas',
                'content': 'Si eres artista y quieres participar en nuestros eventos, revisa la convocatoria y postúlate.',
                'category': cat_cultura,
            },
        ]

        for p in posts:
            Post.objects.create(
                title=p['title'],
                content=p['content'],
                author=colaborador,
                category=p['category'],
                created_at=timezone.now(),
                published=True
            )
        self.stdout.write(self.style.SUCCESS('Posteos de ejemplo creados.'))
