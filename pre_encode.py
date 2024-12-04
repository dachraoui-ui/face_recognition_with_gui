import sqlite3
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import face_recognition
import numpy as np
import pickle


conn = sqlite3.connect("players.db")
cursor = conn.cursor()


cursor.execute("SELECT name, image_url, age, height FROM players")
players = cursor.fetchall()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


known_face_encodings = []
known_face_names = []
known_face_ages = []
known_face_heights = []


for name, image_url, age, height in players:
    try:
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image = image.convert("RGB")
        image_array = np.array(image)


        face_encodings = face_recognition.face_encodings(image_array)
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(name)
            known_face_ages.append(age)
            known_face_heights.append(height)
        else:
            print(f"No face found for {name}, skipping.")
    except (UnidentifiedImageError, IndexError):
        print(f"Error processing {name}: invalid image or no face found.")
    except requests.RequestException as e:
        print(f"Error fetching image for {name}: {e}")


with open("known_faces.pkl", "wb") as file:
    pickle.dump((known_face_encodings, known_face_names, known_face_ages, known_face_heights), file)

print("Face data saved to known_faces.pkl.")


conn.close()
