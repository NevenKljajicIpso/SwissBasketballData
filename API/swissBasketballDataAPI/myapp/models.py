from django.db import models

# Player Model
class Player(models.Model):
    PlayerID = models.AutoField(primary_key=True)
    playerName = models.CharField(max_length=255)

    def __str__(self):
        return self.PlayerName

    class Meta:
        managed = False
        db_table = 'players'
        