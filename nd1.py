import cv2
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from deepface import DeepFace
from retinaface import RetinaFace

# Funkcija nuotraukų parinkimams naudojant failų dialogą
def upload_image(prompt="Pasirinkite failą"):
    root = tk.Tk()
    root.withdraw() # Paslepia pagrindinį langą
    file_path = filedialog.askopenfilename(title=prompt)
    return file_path

# Veidams aptikti naudojant RetinaFace
def detect_faces_retina(image):
    faces = RetinaFace.detect_faces(image)
    detected_faces = []
    for key in faces.keys():
        face = faces[key]["facial_area"]
        x, y, x1, y1 = face
        detected_faces.append((x, y, x1-x, y1-y))
    return detected_faces

# Veidų atpažinimui ir kitiems veidams blur efekto taikymui
def identify_and_blur_faces(img_path, reference_face_path):
    # Nuotraukų nuskaitymas
    img_cv2 = cv2.imread(img_path)
    reference_cv2 = cv2.imread(reference_face_path)
    
    # Aptinka veidus naudodamas RetinaFace
    faces = detect_faces_retina(img_cv2)
    best_match_index = None
    lowest_distance = float("inf")
    
    # Specifinio veido paieška naudojant DeepFace
    for i, (x, y, w, h) in enumerate(faces):
        face_roi = img_cv2[y:y+h, x:x+w]
        try:
            result = DeepFace.verify(face_roi, reference_cv2, model_name='ArcFace', enforce_detection=False)
            distance = result.get('distance', 1.0)
            if distance < lowest_distance:
                lowest_distance = distance
                best_match_index = i
        except Exception as e:
            print(f"Klaida atpažįstant veidą: {e}")
            continue
    
    # Blur efektas visiems neidentifikuotiems veidams
    for i, (x, y, w, h) in enumerate(faces):
        if i != best_match_index:
            face_region = img_cv2[y:y+h, x:x+w]
            blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
            img_cv2[y:y+h, x:x+w] = blurred_face
    
    # Pažymimas atpažintas veidas žalios spalvos rėmeliu
    if best_match_index is not None:
        x, y, w, h = faces[best_match_index]
        cv2.rectangle(img_cv2, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Konvertuoja paveikslėlį į RGB formatą ir rodo rezultatą
    img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
    result_image = Image.fromarray(img_rgb)
    
    # Išsaugomas rezultatas
    result_filename = "result.png"
    result_image.save(result_filename)
    result_image.show(title="Galutinis rezultatas")
    print(f"Rezultatas išsaugotas kaip {result_filename}")

if __name__ == "__main__":
    # Funkcijos iškvietimas nuotraukų įkėlimams
    print("Pasirinkite nuotrauką su žmonėmis:")
    img_path = upload_image("Pasirinkite nuotrauką su žmonėmis")
    if not img_path:
        print("Failo pasirinkimas atšauktas.")
        exit()

    print("Pasirinkite specifinio žmogaus veido nuotrauką:")
    reference_face_path = upload_image("Pasirinkite specifinio žmogaus veido nuotrauką")
    if not reference_face_path:
        print("Failo pasirinkimas atšauktas.")
        exit()

    # Vykdoma veidų atpažinimo ir neryškumo taikymo funkcija
    identify_and_blur_faces(img_path, reference_face_path)
