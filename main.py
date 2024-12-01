import tkinter as tk
from tkinter import filedialog
import pickle
import face_recognition
from PIL import Image, ImageDraw, ImageTk
import numpy as np

# Load pre-encoded face data
try:
    with open("known_faces.pkl", "rb") as file:
        known_face_encodings, known_face_names = pickle.load(file)
    print("Pre-encoded face data loaded successfully.")
except FileNotFoundError:
    print("Error: Pre-encoded face data file not found. Please run pre_encode.py first.")
    exit()

def upload_and_process():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        return

    try:
        unknown_image = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        pil_image = Image.fromarray(unknown_image)
        draw = ImageDraw.Draw(pil_image)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
            text_width, text_height = draw.textbbox((0, 0), name)[2:]
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

        del draw

        # Display the processed image
        processed_image = ImageTk.PhotoImage(pil_image)
        panel.configure(image=processed_image)
        panel.image = processed_image

    except Exception as e:
        print(f"Error processing image: {e}")

# Create GUI
root = tk.Tk()
root.title("Face Recognition App")

btn = tk.Button(root, text="Upload and Process Image", command=upload_and_process)
btn.pack()

panel = tk.Label(root)
panel.pack()

root.mainloop()
