from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('players/', views.player_list, name='player-list'),
    path('players/search/', views.search_player, name='search-player'),

    path('teams/', views.teams_list, name='teams-list'),
    path('teams/search/', views.search_teams, name='search-teams'),
]