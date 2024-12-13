import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import face_recognition
import pickle
import numpy as np



try:
    with open("known_faces.pkl", "rb") as file:
        known_face_encodings, known_face_names, known_face_ages, known_face_heights = pickle.load(file)
    print("Pre-encoded face data loaded successfully.")
except FileNotFoundError:
    print("Error: Pre-encoded face data file not found. Please run pre_encode.py first.")
    exit()


def upload_and_process_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        return


    unknown_image = face_recognition.load_image_file(file_path)
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)


    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        age = "Unknown"
        height = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            age = known_face_ages[best_match_index]
            height = known_face_heights[best_match_index]

        # Draw rectangle around face
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255), width=3)


        text = f"{name} - {age} years - {height} cm"
        text_width, text_height = draw.textbbox((0, 0), text)[2:]
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), text, fill=(255, 255, 255))

    del draw
    pil_image.show()


window = tk.Tk()
window.title("Face Recognition App")
window.geometry("600x600")

label = tk.Label(window, text="Face Recognition App", font=("Arial", 24), pady=20)
label.pack()

upload_button = tk.Button(window, text="Upload and Process Image", font=("Arial", 16), command=upload_and_process_image)
upload_button.pack(pady=20)


window.mainloop()
