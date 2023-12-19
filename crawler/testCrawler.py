import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import mysql.connector
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.db_config import db_config

# Funktion zum Verarbeiten der Statistiken eines Spiels
def process_game_stats(match_id, team1_id, team2_id, stats_link):
    # Öffnet die Seite mit den Spielstatistiken
    driver.get(stats_link)
    time.sleep(2)

    # Sucht nach den Tabellen mit den Spielerstatistiken für beide Teams
    team_tables = driver.find_elements(By.CSS_SELECTOR, "table[id^='DataTables_Table_']")
    for table_index, team_id in enumerate([team1_id, team2_id]):
        # Durchläuft alle Zeilen in der Tabelle für jedes Team
        player_rows = team_tables[table_index].find_elements(By.CSS_SELECTOR, 'tbody > tr')
        for row in player_rows:
            # Sammelt Daten aus jeder Zelle in der Zeile
            data = [td.text for td in row.find_elements(By.TAG_NAME, 'td') if td.text.strip() != '']
            if len(data) < 24:
                player_name = data[1]

                try:
                    # Überprüft, ob der Spieler bereits in der Datenbank vorhanden ist
                    cursor.execute("SELECT PlayerID FROM Players WHERE PlayerName = %s", (player_name,))
                    result = cursor.fetchone()
                    if result:
                        player_id = result[0]
                    else:
                        # Fügt den Spieler hinzu, wenn er noch nicht existiert
                        cursor.execute("INSERT INTO Players (PlayerName) VALUES (%s)", (player_name,))
                        db.commit()
                        player_id = cursor.lastrowid

                        # Überprüfe, ob die Kombination Spieler-Team bereits existiert
                        cursor.execute("SELECT * FROM PlayerTeamAffiliation WHERE PlayerID = %s AND TeamID = %s", (player_id, team_id))
                        if not cursor.fetchone():
                            # Füge den neuen Spieler-Team-Eintrag nur hinzu, wenn er noch nicht existiert
                            cursor.execute("INSERT INTO PlayerTeamAffiliation (PlayerID, TeamID) VALUES (%s, %s)", (player_id, team_id))
                            db.commit()

                    # Fügt die gesammelten Spielerstatistiken in die Datenbank ein
                    insert_stats_query = "INSERT INTO PlayerMatchStatistics (MatchID, PlayerID, MinutesPlayed, TwoPointsMade, TwoPointsAttempt, TwoPointsPercentage, ThreePointsMade, ThreePointsAttempt, ThreePointsPercentage, FreeThrowMade, FreeThrowAttempt, FreeThrowPercentage, OffensiveRebound, DefensiveRebound, TotalRebound, Assists, Turnovers, Steals, Blocks, Fouls, FoulsOn, Efficency, TotalPoints) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(insert_stats_query, (match_id, player_id, data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20], data[21], data[22]))
                    db.commit()
                except mysql.connector.Error as err:
                    print(f"Database error: {err}")

    # Verarbeitet Teamstatistiken in ähnlicher Weise wie Spielerstatistiken
    team_stats_tables = driver.find_elements(By.CSS_SELECTOR, "table[id^='DataTables_Table_']")
    for table_index, team_id in enumerate([team1_id, team2_id]):
        tfoot = team_stats_tables[table_index].find_element(By.TAG_NAME, 'tfoot')
        stats_row = tfoot.find_element(By.TAG_NAME, 'tr')
        stats_data = [th.text for th in stats_row.find_elements(By.TAG_NAME, 'th') if th.text.strip() != '']
        if len(stats_data) >= 22:
            insert_team_stats_query = "INSERT INTO TeamMatchStatistics (MatchID, TeamID, MinutesPlayed, TwoPointsMade, TwoPointsAttempt, TwoPointsPercentage, ThreePointsMade, ThreePointsAttempt, ThreePointsPercentage, FreeThrowMade, FreeThrowAttempt, FreeThrowPercentage, OffensiveRebound, DefensiveRebound, TotalRebound, Assists, Turnovers, Steals, Blocks, Fouls, FoulsOn, Efficency, TotalPoints) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_team_stats_query, (match_id, team_id, stats_data[1], stats_data[2], stats_data[3], stats_data[4], stats_data[5], stats_data[6], stats_data[7], stats_data[8], stats_data[9], stats_data[10], stats_data[11], stats_data[12], stats_data[13], stats_data[14], stats_data[15], stats_data[16], stats_data[17], stats_data[18], stats_data[19], stats_data[20], stats_data[21]))
            db.commit()

# Hauptteil des Crawlers
db = mysql.connector.connect(**db_config)
cursor = db.cursor()
driver = webdriver.Chrome()
driver.get("https://swiss.basketball/de/national-competitions/nlb/men/schedule")
time.sleep(1)

# Sammelt Daten von allen Spieltagen auf der Seite
game_days = driver.find_elements(By.CSS_SELECTOR, 'div[id^="anchor-"]')
games_data = []
new_games_processed = False  # Flag zur Überprüfung neuer Spiele

# URLs und Datum für jedes Spiel sammeln
for game_day in game_days:
    date = game_day.find_element(By.CSS_SELECTOR, 'div.mt-6.text-white.p-2').text
    formatted_date = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")

     # Überprüfe, ob der Spieltag bereits verarbeitet wurde
    cursor.execute("SELECT * FROM processedgamedays WHERE GameDay = %s", (formatted_date,))
    if cursor.fetchone():
        continue  # Dieser Spieltag wurde bereits verarbeitet

    games = game_day.find_elements(By.CSS_SELECTOR, 'table.schedule-table > tbody > tr')

    # Sammelt Daten für jedes Spiel des Spieltags
    for i in range(0, len(games), 2):
        team1 = games[i].find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
        team2 = games[i+1].find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
        stats_elements = games[i].find_elements(By.CSS_SELECTOR, 'td > a[href*="?gid="]')

        if stats_elements:
            stats_link = stats_elements[0].get_attribute('href')
            games_data.append((formatted_date, team1, team2, stats_link))

# Jedes Spiel verarbeiten
for game in games_data:
    formatted_date, team1, team2, stats_link = game
    cursor.execute("SELECT TeamID FROM Teams WHERE TeamName = %s", (team1,))
    team1_id = cursor.fetchone()[0]
    cursor.execute("SELECT TeamID FROM Teams WHERE TeamName = %s", (team2,))
    team2_id = cursor.fetchone()[0]
    insert_query = "INSERT INTO Matches (MatchDate, Team1ID, Team2ID) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (formatted_date, team1_id, team2_id))
    db.commit()
    match_id = cursor.lastrowid
    process_game_stats(match_id, team1_id, team2_id, stats_link)
    new_games_processed = True  # Setze das Flag, wenn ein neues Spiel verarbeitet wird

    # Markiere den Spieltag als verarbeitet in der processedgamedays Tabelle
    cursor.execute("INSERT IGNORE INTO processedgamedays (GameDay) VALUES (%s)", (formatted_date,))
    db.commit()

# Überprüfen, ob neue Spiele verarbeitet wurden
if not new_games_processed:
    print("Keine neuen Spiele zurzeit")

driver.quit()
cursor.close()
db.close()