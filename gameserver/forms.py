from django import forms
from .models import UserGame, Review
from .models import Game

class UserGameForm(forms.ModelForm):
    class Meta:
        model = UserGame
        fields = ['status']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'platform', 'release_date', 'developer', 'cover']