from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PlayerSerializer, PlayerMatchStatisticSerializer
from .models import Player, PlayerMatchStatistic
from django.db.models import Avg

@api_view(['GET'])
def player_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 20  # Anzahl der Objekte pro Seite
    players = Player.objects.all()
    result_page = paginator.paginate_queryset(players, request)
    serializer = PlayerSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def search_player(request):
    query = request.query_params.get('name')
    if query:
        players = Player.objects.filter(playerName__icontains=query)
        player_stats = []

        for player in players:
            avg_stats = PlayerMatchStatistic.objects.filter(PlayerID=player.PlayerID).aggregate(
                avg_minutes_played=Avg('MinutesPlayed'),
                avg_two_points_made=Avg('TwoPointsMade'),
                avg_two_points_attempt=Avg('TwoPointsAttempt'),
                avg_two_points_percentage=Avg('TwoPointsPercentage'),
                avg_three_points_made=Avg('ThreePointsMade'),
                avg_three_points_attempt=Avg('ThreePointsAttempt'),
                avg_three_points_percentage=Avg('ThreePointsPercentage'),
                avg_free_throw_made=Avg('FreeThrowMade'),
                avg_free_throw_attempt=Avg('FreeThrowAttempt'),
                avg_free_throw_percentage=Avg('FreeThrowPercentage'),
                avg_offensive_rebound=Avg('OffensiveRebound'),
                avg_defensive_rebound=Avg('DefensiveRebound'),
                avg_total_rebound=Avg('TotalRebound'),
                avg_assists=Avg('Assists'),
                avg_turnovers=Avg('Turnovers'),
                avg_steals=Avg('Steals'),
                avg_blocks=Avg('Blocks'),
                avg_fouls=Avg('Fouls'),
                avg_fouls_on=Avg('FoulsOn'),
                avg_efficiency=Avg('Efficency'),
                avg_total_points=Avg('TotalPoints')
            )
            player_data = {
                "player_id": player.PlayerID,
                "player_name": player.playerName,
                "average_statistics": avg_stats
            }
            player_stats.append(player_data)

        return Response(player_stats)
    return Response({"message": "Kein Name angegeben"})