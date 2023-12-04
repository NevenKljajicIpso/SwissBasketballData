import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import mysql.connector
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.db_config import db_config

db = mysql.connector.connect(**db_config)
cursor = db.cursor()

# WebDriver initialisieren
driver = webdriver.Chrome()

# Schedule Seite öffnen
driver.get("https://swiss.basketball/de/national-competitions/nlb/men/schedule")

# Kurze Wartezeit um sicherzustellen, dass alles geladen wird
time.sleep(2)

# Alle Spieltage finden
game_days = driver.find_elements(By.CSS_SELECTOR, 'div[id^="anchor-"]')

for game_day in game_days:
    # Datum des Spiels extrahieren
    date = game_day.find_element(By.CSS_SELECTOR, 'div.mt-6.text-white.p-2').text
    # Datum umwandeln
    formatted_date = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")

    # Alle Spiele an diesem Tag finden
    games = game_day.find_elements(By.CSS_SELECTOR, 'table.schedule-table > tbody > tr')

    for i in range(0, len(games), 2):  # Schritt 2, da jedes Spiel durch 2 Zeilen repräsentiert wird
        # Teams aus den beiden Zeilen extrahieren
        team1 = games[i].find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
        team2 = games[i+1].find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text

        # Überprüfen, ob ein Statistik-Link vorhanden ist
        stats_elements = games[i].find_elements(By.CSS_SELECTOR, 'td > a[href*="?gid="]')
        if not stats_elements:
            continue  # Kein Link vorhanden, überspringe dieses Spiel

        # Statistik-Link extrahieren
        stats_link = stats_elements[0].get_attribute('href')
        
        # Team-IDs basierend auf Teamnamen abrufen
        cursor.execute("SELECT TeamID FROM Teams WHERE TeamName = %s", (team1,))
        team1_id = cursor.fetchone()[0]
        cursor.execute("SELECT TeamID FROM Teams WHERE TeamName = %s", (team2,))
        team2_id = cursor.fetchone()[0]

        # Spiel in die Matches-Tabelle einfügen
        insert_query = "INSERT INTO Matches (MatchDate, Team1ID, Team2ID) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (formatted_date, team1_id, team2_id))
        db.commit()
        match_id = cursor.lastrowid

        print("Matches inserted, now to stats link")

        # Navigieren zur Statistikseite
        driver.get(stats_link)
        time.sleep(2)

        print("Now here stats")

        # Spielerstatistiken verarbeiten
        team_tables = driver.find_elements(By.CSS_SELECTOR, "table[id^='DataTables_Table_']")

        for table_index, team_id in enumerate([team1_id, team2_id]):
            print("Heerooo")
            player_rows = team_tables[table_index].find_elements(By.CSS_SELECTOR, 'tbody > tr')
            for row in player_rows:
                print("Aaand Heere?")
                data = [td.text for td in row.find_elements(By.TAG_NAME, 'td') if td.text.strip() != '']
                print(data)
                if len(data) < 24:  # Überprüfen, ob die Zeile vollständige Daten enthält
                    print("passt")
                    player_name = data[1]  # Spielername

                    try:
                        cursor.execute("SELECT PlayerID FROM Players WHERE PlayerName = %s", (player_name,))
                        result = cursor.fetchone()
                        if result:
                            player_id = result[0]
                        else:
                            cursor.execute("INSERT INTO Players (PlayerName) VALUES (%s)", (player_name,))
                            db.commit()
                            player_id = cursor.lastrowid

                        cursor.execute("INSERT INTO PlayerTeamAffiliation (PlayerID, TeamID) VALUES (%s, %s) ON DUPLICATE KEY UPDATE TeamID = %s", (player_id, team_id, team_id))
                        db.commit()

                        # Spielerstatistiken eintragen
                        insert_stats_query = "INSERT INTO PlayerMatchStatistics (MatchID, PlayerID, MinutesPlayed, TwoPointsMade, TwoPointsAttempt, TwoPointsPercentage, ThreePointsMade, ThreePointsAttempt, ThreePointsPercentage, FreeThrowMade, FreeThrowAttempt, FreeThrowPercentage, OffensiveRebound, DefensiveRebound, TotalRebound, Assists, Turnovers, Steals, Blocks, Fouls, FoulsOn, Efficency, TotalPoints) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(insert_stats_query, (match_id, player_id, data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20], data[21], data[22]))
                        db.commit()
                    except mysql.connector.Error as err:
                        print(f"Database error: {err}")

        # Teamstatistiken verarbeiten
        team_stats_tables = driver.find_elements(By.CSS_SELECTOR, "table[id^='DataTables_Table_']")
        for table_index, team_id in enumerate([team1_id, team2_id]):
            tfoot = team_stats_tables[table_index].find_element(By.TAG_NAME, 'tfoot')
            stats_row = tfoot.find_element(By.TAG_NAME, 'tr')
            stats_data = [th.text for th in stats_row.find_elements(By.TAG_NAME, 'th') if th.text.strip() != '']
            print(stats_data)
            if len(stats_data) >= 22:
                # Teamstatistiken einfügen
                insert_team_stats_query = "INSERT INTO TeamMatchStatistics (MatchID, TeamID, MinutesPlayed, TwoPointsMade, TwoPointsAttempt, TwoPointsPercentage, ThreePointsMade, ThreePointsAttempt, ThreePointsPercentage, FreeThrowMade, FreeThrowAttempt, FreeThrowPercentage, OffensiveRebound, DefensiveRebound, TotalRebound, Assists, Turnovers, Steals, Blocks, Fouls, FoulsOn, Efficency, TotalPoints) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_team_stats_query, (match_id, team_id, stats_data[1], stats_data[2], stats_data[3], stats_data[4], stats_data[5], stats_data[6], stats_data[7], stats_data[8], stats_data[9], stats_data[10], stats_data[11], stats_data[12], stats_data[13], stats_data[14], stats_data[15], stats_data[16], stats_data[17], stats_data[18], stats_data[19], stats_data[20], stats_data[21]))
                db.commit()
            else:
                print(f"Fehler: Nicht genügend Daten für Team-ID {team_id}")

        # Zurück zur Hauptseite navigieren, um das nächste Spiel zu verarbeiten
        driver.get("https://swiss.basketball/de/national-competitions/nlb/men/schedule")
        time.sleep(2)

        print(f"Date: {formatted_date}, Team1: {team1}, Team2: {team2}, Stats Link: {stats_link}")

# Browser schließen
driver.quit()
cursor.close()
db.close()
