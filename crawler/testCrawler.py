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

# Initialize the web driver
driver = webdriver.Chrome()

# Open the schedule page
driver.get("https://swiss.basketball/de/national-competitions/nlb/men/schedule")

# Wait for the page to load
time.sleep(5)

# Find all game day divs
game_days = driver.find_elements(By.CSS_SELECTOR, 'div[id^="anchor-"]')

# Iterate over each game day
for game_day in game_days:
    # Extract the date of the game
    date = game_day.find_element(By.CSS_SELECTOR, 'div.mt-6.text-white.p-2').text
    # Datum umwandeln
    formatted_date = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")

    # Find all games on this day
    games = game_day.find_elements(By.CSS_SELECTOR, 'table.schedule-table > tbody > tr')

    # Iterate over each pair of rows representing a game
    for i in range(0, len(games), 2):  # Step by 2 as each game is represented by 2 rows
        # Extract teams from the two rows
        team1 = games[i].find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
        team2 = games[i+1].find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text

        # Überprüfen, ob ein Statistik-Link vorhanden ist
        stats_elements = games[i].find_elements(By.CSS_SELECTOR, 'td > a[href*="?gid="]')
        if not stats_elements:
            # Wenn kein Link vorhanden ist, überspringe dieses Spiel
            continue

        # Statistik-Link extrahieren
        stats_link = stats_elements[0].get_attribute('href')
        
        # Abrufen der Team-IDs basierend auf Teamnamen
        cursor.execute("SELECT TeamID FROM Teams WHERE TeamName = %s", (team1,))
        team1_id = cursor.fetchone()[0]
        cursor.execute("SELECT TeamID FROM Teams WHERE TeamName = %s", (team2,))
        team2_id = cursor.fetchone()[0]

        # Einfügen des Spiels in die Matches-Tabelle
        insert_query = "INSERT INTO Matches (MatchDate, Team1ID, Team2ID) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (formatted_date, team1_id, team2_id))
        db.commit()

        # Print or process the data
        print(f"Date: {formatted_date}, Team1: {team1}, Team2: {team2}, Stats Link: {stats_link}")

# Close the browser
driver.quit()
cursor.close()
db.close()