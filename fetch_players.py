import sqlite3
import requests


query = """
SELECT ?playerLabel ?teamLabel ?image ?birthDate ?height WHERE {
  ?player wdt:P31 wd:Q5;               # Instance of human
          wdt:P106 wd:Q937857;         # Occupation: football player
          wdt:P54 ?team;               # Member of a sports team
          wdt:P18 ?image;              # Has image
          wdt:P569 ?birthDate;         # Date of birth
          wdt:P2048 ?height.           # Height
  ?team wdt:P118 wd:Q9448.             # Team is part of the Premier League
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}LIMIT 20
"""
#another query
#query = "select from that table where the player is a football player and the team is in the premier league""


url = "https://query.wikidata.org/sparql"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


response = requests.get(url, params={"query": query, "format": "json"}, headers=headers)
response.raise_for_status()
data = response.json()


conn = sqlite3.connect("players.db")
cursor = conn.cursor()


cursor.execute("DROP TABLE IF EXISTS players")


cursor.execute("""
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    team TEXT,
    image_url TEXT,
    age INTEGER,
    height REAL
)
""")


for item in data["results"]["bindings"]:
    name = item["playerLabel"]["value"]
    team = item["teamLabel"]["value"]
    image_url = item["image"]["value"]
    birth_date = item.get("birthDate", {}).get("value", None)
    height = item.get("height", {}).get("value", None)


    if birth_date:
        from datetime import datetime
        birth_year = int(birth_date.split("-")[0])
        current_year = datetime.now().year
        age = current_year - birth_year
    else:
        age = None

    cursor.execute("""
        INSERT INTO players (name, team, image_url, age, height)
        VALUES (?, ?, ?, ?, ?)
    """, (name, team, image_url, age, height))

conn.commit()
conn.close()

print("Player data has been fetched and stored in players.db.")
