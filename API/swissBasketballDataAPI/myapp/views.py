from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PlayerSerializer, TeamSerializer, PlayerMatchStatisticSerializer
from .models import Player, PlayerMatchStatistic, Team, TeamMatchStatistic, PlayerTeamAffiliation
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
def teams_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 20  # Anzahl der Objekte pro Seite
    teams = Team.objects.all()
    result_page = paginator.paginate_queryset(teams, request)
    serializer = TeamSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def search_player(request):
    query = request.query_params.get('name')
    if query:
        players = Player.objects.filter(PlayerName__icontains=query)
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
            team_affiliations = PlayerTeamAffiliation.objects.filter(PlayerID=player.PlayerID)
            team_names = [affiliation.TeamID.TeamName for affiliation in team_affiliations]
            player_data = {
                "player_id": player.PlayerID,
                "player_Name": player.PlayerName,
                "teams": team_names,
                "average_statistics": avg_stats
            }
            player_stats.append(player_data)

        return Response(player_stats)
    return Response({"message": "Kein Name angegeben"})

@api_view(['GET'])
def search_teams(request):
    query = request.query_params.get('name')
    if query:
        teams = Team.objects.filter(TeamName__icontains=query)
        team_stats = []

        for team in teams:
            avg_stats = TeamMatchStatistic.objects.filter(TeamID=team.TeamID).aggregate(
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
            team_data = {
                "team_id": team.TeamID,
                "team_name": team.TeamName,
                "average_statistics": avg_stats
            }
            team_stats.append(team_data)

        return Response(team_stats)
    return Response({"message": "Kein Teamname angegeben"})