"""
URL configuration for videogameserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gameserver import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('remove-from-collection/<int:usergame_id>/', views.remove_from_collection, name='remove_from_collection'),
    path('add-to-collection/', views.add_to_collection, name='add_to_collection'),
    path('games/', views.game_list, name='game_list'),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('my-collection/', views.my_collection, name='my_collection'),
    path('edit-status/<int:usergame_id>/', views.edit_status, name='edit_status'),
    path('add-review/<int:usergame_id>/', views.add_review, name='add_review'),
    path('add-game/', views.add_game, name='add_game'),
    path('remove-game/<int:game_id>/', views.remove_game, name='remove_game'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)