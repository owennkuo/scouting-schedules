# DEFINITIONS
event_key = "2026cacac"
team_key = "frc5507"
api_key = "1pASptoMl6xXHptBnpRfEG3KFU6ghqdU9pzDNs3WWaD9hXsL6LDW22imF99SZlFA"

import sqlite3
import requests
import csv

conn = sqlite3.connect("data.db")
cursor = conn.cursor()
query = "INSERT INTO event_matches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
cursor.execute("DELETE FROM event_matches")
cursor.execute("DELETE FROM scouting")

matches_data = requests.get(f"https://www.thebluealliance.com/api/v3/event/{event_key}/matches", headers={'X-TBA-AUTH-KEY':api_key}).json()
#print(matches_data)

for match in matches_data:
    match_id = match.get("key")
    red_teams = match["alliances"]["red"]["team_keys"]
    blue_teams = match["alliances"]["blue"]["team_keys"]
    cursor.execute(query, (match_id, match["comp_level"], match["match_number"], red_teams[0], red_teams[1], red_teams[2], blue_teams[0], blue_teams[1], blue_teams[2]))

cursor.execute("""SELECT * FROM event_matches
                  WHERE comp_level = 'qm'
                  AND 'frc5507' IN (R1, R2, R3, B1, B2, B3)
                  ORDER BY match_number""")
matches = cursor.fetchall()
index = 1
# For each match with the target team key, find the last match for each opponent.
for row in matches:
    for i in range(6):
        if row[i+3] == team_key:
            continue
        cursor.execute(f"SELECT * FROM event_matches WHERE comp_level = 'qm' AND match_number < {row[2]} AND '{row[i+3]}' IN (R1, R2, R3, B1, B2, B3) ORDER BY match_number DESC LIMIT 1")
        match = cursor.fetchone()
        print(row[i+3] + " for match " + row[0] + ": " + str(match))
        if match != None:
            # Log the match into a separate table.
            cursor.execute(
                """
                INSERT
                OR IGNORE INTO scouting
                VALUES (?, ?, ?, ?)
                """,
                (match[0], match[2], row[i+3], row[0]),
            )
    index += 1

cursor.execute(f"SELECT * FROM scouting")
headers = [description[0] for description in cursor.description]
rows = cursor.fetchall()

output_file = event_key + "_schedule.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    writer.writerows(rows)


conn.commit()
conn.close()