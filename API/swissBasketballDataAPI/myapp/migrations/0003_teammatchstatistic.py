# Generated by Django 5.0 on 2023-12-25 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMatchStatistic',
            fields=[
                ('StatID', models.AutoField(primary_key=True, serialize=False)),
                ('MinutesPlayed', models.IntegerField()),
                ('TwoPointsMade', models.IntegerField()),
                ('TwoPointsAttempt', models.IntegerField()),
                ('TwoPointsPercentage', models.FloatField()),
                ('ThreePointsMade', models.IntegerField()),
                ('ThreePointsAttempt', models.IntegerField()),
                ('ThreePointsPercentage', models.FloatField()),
                ('FreeThrowMade', models.IntegerField()),
                ('FreeThrowAttempt', models.IntegerField()),
                ('FreeThrowPercentage', models.FloatField()),
                ('OffensiveRebound', models.IntegerField()),
                ('DefensiveRebound', models.IntegerField()),
                ('TotalRebound', models.IntegerField()),
                ('Assists', models.IntegerField()),
                ('Turnovers', models.IntegerField()),
                ('Steals', models.IntegerField()),
                ('Blocks', models.IntegerField()),
                ('Fouls', models.IntegerField()),
                ('FoulsOn', models.IntegerField()),
                ('Efficency', models.IntegerField()),
                ('TotalPoints', models.IntegerField()),
            ],
            options={
                'db_table': 'TeamMatchStatistic',
                'managed': False,
            },
        ),
    ]