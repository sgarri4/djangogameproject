from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg

from .models import Game, UserGame, Review
from .forms import UserGameForm, ReviewForm
from .forms import GameForm

def index(request):
    """Página de inicio."""
    return render(request, 'index.html')

def game_list(request):
    """
    Lista todos los juegos disponibles.
    Permite búsqueda por título y filtrado por plataforma.
    """
    games = Game.objects.all()
    query = request.GET.get('q')
    platform = request.GET.get('platform')

    if query != "None" and query:
        games = games.filter(title__icontains=query)
    if platform:
        games = games.filter(platform__iexact=platform)

    platforms = Game.objects.values_list('platform', flat=True).distinct()
    return render(request, 'game_list.html', {
        'games': games,
        'platforms': platforms,
        'selected_platform': platform,
        'query': query,
    })

def game_detail(request, game_id):
    """
    Muestra el detalle de un juego, sus reseñas y la media de puntuaciones.
    """
    game = get_object_or_404(Game, id=game_id)
    reviews = Review.objects.filter(user_game__game=game)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    stars = int(round(avg_rating)) if avg_rating else 0
    user_game = UserGame.objects.filter(game=game).first()
    user_review = None
    if user_game:
        user_review = Review.objects.filter(user_game=user_game).first()

    return render(request, 'game_detail.html', {
        'game': game,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'stars': stars,
        'user_game': user_game,
        'user_review': user_review,
    })

def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Juego añadido al catálogo.')
            return redirect('game_list')
    else:
        form = GameForm()
    return render(request, 'add_game.html', {'form': form})

def remove_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        game.delete()
        messages.success(request, 'Juego eliminado del catálogo.')
        return redirect('game_list')
    return render(request, 'remove_game.html', {'game': game})

def add_to_collection(request):
    games = Game.objects.all()
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        status = request.POST.get('status')
        game = Game.objects.get(id=game_id)
        # Comprobar si ya existe
        if UserGame.objects.filter(game=game).exists():
            # Opcional: muestra un mensaje de error o redirige
            messages.error(request, f'El juego "{game.title}" ya está en la colección.')
            return redirect('my_collection')
        UserGame.objects.create(game=game, status=status)
        messages.success(request, f'Juego "{game.title}" añadido a la colección.')
        return redirect('my_collection')
    return render(request, 'add_to_collection.html', {'games': games})

    

def my_collection(request):
    """
    Muestra la colección global, con filtros por estado y búsqueda.
    """
    user_games = UserGame.objects.select_related('game').all()
    status = request.GET.get('status')
    query = request.GET.get('q')

    if status:
        user_games = user_games.filter(status=status)
    if query != "None" and query:
        user_games = user_games.filter(game__title__icontains=query)

    statuses = UserGame.STATUS_CHOICES
    return render(request, 'my_collection.html', {
        'user_games': user_games,
        'statuses': statuses,
        'selected_status': status,
        'query': query,
    })

def edit_status(request, usergame_id):
    """
    Permite editar el estado de un juego en la colección.
    """
    user_game = get_object_or_404(UserGame, id=usergame_id)
    if request.method == 'POST':
        form = UserGameForm(request.POST, instance=user_game)
        if form.is_valid():
            form.save()
            messages.success(request, f'Estado de "{user_game.game.title}" actualizado.')
            return redirect('my_collection')
    else:
        form = UserGameForm(instance=user_game)
    return render(request, 'edit_status.html', {
        'form': form,
        'user_game': user_game,
    })

def remove_from_collection(request, usergame_id):
    """
    Elimina un juego de la colección.
    """
    user_game = get_object_or_404(UserGame, id=usergame_id)
    if request.method == 'POST':
        user_game.delete()
        messages.success(request, f'"{user_game.game.title}" eliminado de la colección.')
        return redirect('my_collection')
    return render(request, 'remove_from_collection.html', {
        'user_game': user_game,
    })  

def add_review(request, usergame_id):
    """
    Permite añadir o editar una reseña para un juego de la colección.
    """
    user_game = get_object_or_404(UserGame, id=usergame_id)
    review, created = Review.objects.get_or_create(user_game=user_game)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reseña guardada correctamente.')
            return redirect('my_collection')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'add_review.html', {
        'form': form,
        'user_game': user_game,
        'created': created,
    })

def delete_review(request, usergame_id):
    """
    Permite eliminar la reseña de un juego de la colección.
    """
    user_game = get_object_or_404(UserGame, id=usergame_id)
    review = get_object_or_404(Review, user_game=user_game)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Reseña eliminada correctamente.')
        return redirect('my_collection')
    return render(request, 'delete_review.html', {
        'user_game': user_game,
        'review': review,
    })
