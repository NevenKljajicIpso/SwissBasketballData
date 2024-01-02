from django.db import models

# Player Model
class Player(models.Model):
    PlayerID = models.AutoField(primary_key=True)
    PlayerName = models.CharField(max_length=255)

    def __str__(self):
        return self.PlayerName

    class Meta:
        managed = False
        db_table = 'players'

class Match(models.Model):
    MatchID = models.AutoField(primary_key=True)
    MatchDate = models.DateField()
    Team1ID = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='home_matches')
    Team2ID = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='away_matches')

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.match_date}"
    
    class Meta:
        managed = False
        db_table = 'matches'

class PlayerMatchStatistic(models.Model):
    StatID = models.AutoField(primary_key=True)
    MatchID = models.ForeignKey('Match', on_delete=models.CASCADE, db_column='MatchID')
    PlayerID = models.ForeignKey('Player', on_delete=models.CASCADE, db_column='PlayerID')
    MinutesPlayed = models.IntegerField()
    TwoPointsMade = models.IntegerField()
    TwoPointsAttempt = models.IntegerField()
    TwoPointsPercentage = models.FloatField()
    ThreePointsMade = models.IntegerField()
    ThreePointsAttempt = models.IntegerField()
    ThreePointsPercentage = models.FloatField()
    FreeThrowMade = models.IntegerField()
    FreeThrowAttempt = models.IntegerField()
    FreeThrowPercentage = models.FloatField()
    OffensiveRebound = models.IntegerField()
    DefensiveRebound = models.IntegerField()
    TotalRebound = models.IntegerField()
    Assists = models.IntegerField()
    Turnovers = models.IntegerField()
    Steals = models.IntegerField()
    Blocks = models.IntegerField()
    Fouls = models.IntegerField()
    FoulsOn = models.IntegerField()
    Efficency = models.IntegerField()
    TotalPoints = models.IntegerField()

    class Meta:
        db_table = 'PlayerMatchStatistics'
        managed = False

class Team(models.Model):
    TeamID = models.AutoField(primary_key=True)
    TeamName = models.CharField(max_length=255)

    def __str__(self):
        return self.team_name
    
    class Meta:
        managed = False
        db_table = 'teams'

class TeamMatchStatistic(models.Model):
    StatID = models.AutoField(primary_key=True)
    MatchID = models.ForeignKey('Match', on_delete=models.CASCADE, db_column='MatchID')
    TeamID = models.ForeignKey('Team', on_delete=models.CASCADE, db_column='TeamID')
    MinutesPlayed = models.IntegerField()
    TwoPointsMade = models.IntegerField()
    TwoPointsAttempt = models.IntegerField()
    TwoPointsPercentage = models.FloatField()
    ThreePointsMade = models.IntegerField()
    ThreePointsAttempt = models.IntegerField()
    ThreePointsPercentage = models.FloatField()
    FreeThrowMade = models.IntegerField()
    FreeThrowAttempt = models.IntegerField()
    FreeThrowPercentage = models.FloatField()
    OffensiveRebound = models.IntegerField()
    DefensiveRebound = models.IntegerField()
    TotalRebound = models.IntegerField()
    Assists = models.IntegerField()
    Turnovers = models.IntegerField()
    Steals = models.IntegerField()
    Blocks = models.IntegerField()
    Fouls = models.IntegerField()
    FoulsOn = models.IntegerField()
    Efficency = models.IntegerField()
    TotalPoints = models.IntegerField()

    class Meta:
        db_table = 'TeamMatchStatistics'
        managed = False

class PlayerTeamAffiliation(models.Model):
    AffiliationID = models.AutoField(primary_key=True)
    PlayerID = models.ForeignKey('Player', on_delete=models.CASCADE, db_column='PlayerID')
    TeamID = models.ForeignKey('Team', on_delete=models.CASCADE, db_column='TeamID')

    class Meta:
        managed = False
        db_table = 'PlayerTeamAffiliation'