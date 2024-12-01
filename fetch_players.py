import sqlite3
import requests

# SPARQL query to fetch player data
query = """
SELECT ?playerLabel ?teamLabel ?image WHERE {
  ?player wdt:P31 wd:Q5;               # Instance of human
          wdt:P106 wd:Q937857;         # Occupation: football player
          wdt:P54 ?team;               # Member of a sports team
          wdt:P18 ?image.              # Has image
  ?team wdt:P118 wd:Q9448.             # Team is part of the Premier League
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}LIMIT 6000
"""

# URL to query Wikidata
url = "https://query.wikidata.org/sparql"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Fetch data from Wikidata
response = requests.get(url, params={"query": query, "format": "json"}, headers=headers)
response.raise_for_status()
data = response.json()

# Connect to SQLite database (create if not exists)
conn = sqlite3.connect("players.db")
cursor = conn.cursor()

# Create players table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    team TEXT,
    image_url TEXT
)
""")

# Insert player data into the database
for item in data["results"]["bindings"]:
    name = item["playerLabel"]["value"]
    team = item["teamLabel"]["value"]
    image_url = item["image"]["value"]

    cursor.execute("INSERT INTO players (name, team, image_url) VALUES (?, ?, ?)", (name, team, image_url))


# Commit and close the database connection
conn.commit()
conn.close()

print("Player data has been fetched and stored in players.db.")
