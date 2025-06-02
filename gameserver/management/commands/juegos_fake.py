from faker import Faker
import random
from gameserver.models import Game
from django.core.management.base import BaseCommand


class JuegosFake:
    def __init__(self):
        self.fake = Faker('es_ES')
        self.platforms = ['PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch', 'Mobile']

    def crear_juegos(self, cantidad=50):
        juegos_creados = []
        for _ in range(cantidad):
            titulo = self.fake.unique.sentence(nb_words=3).rstrip('.')
            plataforma = random.choice(self.platforms)
            fecha_lanzamiento = self.fake.date_between(start_date='-10y', end_date='today')
            desarrollador = self.fake.company()
            juego = Game.objects.create(
                title=titulo,
                platform=plataforma,
                release_date=fecha_lanzamiento,
                developer=desarrollador
            )
            juegos_creados.append(juego)
        return juegos_creados


class Command(BaseCommand):
    help = 'Genera juegos fake en el catálogo'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        platforms = ['PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch', 'Mobile']
        juegos_creados = 0

        for _ in range(50):
            titulo = fake.unique.sentence(nb_words=3).rstrip('.')
            plataforma = random.choice(platforms)
            fecha_lanzamiento = fake.date_between(start_date='-10y', end_date='today')
            desarrollador = fake.company()
            if not Game.objects.filter(title=titulo, platform=plataforma).exists():
                Game.objects.create(
                    title=titulo,
                    platform=plataforma,
                    release_date=fecha_lanzamiento,
                    developer=desarrollador
                )
                juegos_creados += 1

        self.stdout.write(self.style.SUCCESS(f'{juegos_creados} juegos fake añadidos al catálogo.'))
