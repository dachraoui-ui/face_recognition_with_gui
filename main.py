import pickle
import face_recognition
from PIL import Image, ImageDraw, ImageTk, ImageFont
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox


try:
    with open("known_faces.pkl", "rb") as file:
        known_face_encodings, known_face_names = pickle.load(file)
    print("Données de visages encodées chargées avec succès.")
except FileNotFoundError:
    messagebox.showerror("Erreur", "Fichier de données encodées introuvable. Veuillez exécuter pre_encode.py d'abord.")
    exit()


def process_image():
    file_path = filedialog.askopenfilename(title="Sélectionnez une image", filetypes=[("Fichiers image", "*.jpg;*.png;*.jpeg")])
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
            name = "Inconnu"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]


            draw.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0), width=3)


            text_width, text_height = draw.textbbox((0, 0), name)[2:]
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(255, 0, 0))


            font = ImageFont.truetype("arial.ttf", 20)
            draw.text((left + 6, bottom - text_height - 10), name, fill=(255, 255, 255), font=font)

        del draw


        pil_image.thumbnail((500, 500))
        img = ImageTk.PhotoImage(pil_image)
        image_label.config(image=img)
        image_label.image = img

    except FileNotFoundError:
        messagebox.showerror("Erreur", f"Image {file_path} introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


root = tk.Tk()
root.title("Application de reconnaissance faciale")
root.geometry("600x700")
root.config(bg="#f0f0f0")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

title_label = tk.Label(frame, text="Application de reconnaissance faciale", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

upload_button = tk.Button(frame, text="Télécharger et traiter une image", command=process_image, font=("Helvetica", 14), bg="#0078d7", fg="white", padx=10, pady=5)
upload_button.pack(pady=20)

image_label = tk.Label(root, text="L'image traitée apparaîtra ici.", font=("Helvetica", 12), bg="#f0f0f0", fg="#888")
image_label.pack(pady=20)


root.mainloop()
