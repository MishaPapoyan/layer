from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.games_home, name='home'),
    path('type/<int:pk>/', views.game_type_detail, name='game_type_detail'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('game/<int:pk>/start/', views.start_game, name='start_game'),
    path('play/<int:session_id>/', views.play_game, name='play_game'),
    path('result/<int:session_id>/', views.game_result, name='game_result'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    # Multiplayer
    path('multiplayer/', views.multiplayer_home, name='multiplayer_home'),
    path('multiplayer/create/', views.create_multiplayer_room, name='create_multiplayer_room'),
    path('multiplayer/room/<str:room_code>/', views.multiplayer_room, name='multiplayer_room'),
    path('multiplayer/join/', views.join_multiplayer_room, name='join_multiplayer_room'),
]

