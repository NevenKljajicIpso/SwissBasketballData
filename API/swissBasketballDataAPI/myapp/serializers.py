from rest_framework import serializers
from .models import Player, PlayerMatchStatistic, Match, Team

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class PlayerMatchStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerMatchStatistic
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'