from django.contrib import admin
from .models import Player, PlayerMatchStatistic, Match, Team, TeamMatchStatistic

# Register your models here.
admin.site.register(Player)
admin.site.register(PlayerMatchStatistic)
admin.site.register(Match)
admin.site.register(Team)
admin.site.register(TeamMatchStatistic)