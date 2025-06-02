from faker import Faker
import random
from datetime import datetime
from .models import Game, Review, UserGame
from django.contrib.auth.models import User

fake = Faker('es_ES')

# Crear juegos
platforms = ['PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch', 'Mobile']
for _ in range(20):
    Game.objects.create(
        title=fake.unique.sentence(nb_words=3).rstrip('.'),
        platform=random.choice(platforms),
        release_date=fake.date_between(start_date='-10y', end_date='today'),
        developer=fake.company()
    )

# Crear usuarios
for _ in range(5):
    User.objects.create_user(
        username=fake.unique.user_name(),
        email=fake.email(),
        password='password123'
    )

# Crear colecciones y reseñas
games = list(Game.objects.all())
users = list(User.objects.all())
status_choices = ['pending', 'playing', 'completed', 'abandoned']

for user in users:
    user_games = random.sample(games, random.randint(5, 15))
    for game in user_games:
        usergame = UserGame.objects.create(
            user=user,
            game=game,
            status=random.choice(status_choices),
            added_at=fake.date_time_this_year()
        )
        # Aproximadamente la mitad con reseña
        if random.random() > 0.5:
            Review.objects.create(
                user_game=usergame,
                rating=random.randint(1, 5),
                text=fake.paragraph(nb_sentences=3),
                created_at=fake.date_time_this_year()
            )
