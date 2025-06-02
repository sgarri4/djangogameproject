from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    developer = models.CharField(max_length=100, blank=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.platform})"

class UserGame(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('playing', 'Jugando'),
        ('completed', 'Completado'),
        ('abandoned', 'Abandonado'),
    ]
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ahora solo se asegura que no se repita el mismo juego en la colección global
        unique_together = ('game',)

    def __str__(self):
        return f"{self.game.title} - {self.get_status_display()}"

class Review(models.Model):
    user_game = models.OneToOneField(UserGame, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=0)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña para {self.user_game.game}"
