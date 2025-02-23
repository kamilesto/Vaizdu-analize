import cv2
import torch
from transformers import AutoModel, AutoProcessor
import tkinter as tk
from tkinter import filedialog

# Failo pasirinkimo funkcija naudojant tkinter
def upload_file(prompt="Pasirinkite failą"):
    root = tk.Tk()
    root.withdraw()
    root.update()  # Užtikrina, kad GUI pilnai inicializuota
    file_path = filedialog.askopenfilename(title=prompt)
    return file_path

# Įkeliamas Transformer pagrindu veidų atpažinimo modelį be pooling sluoksnio
model_name = "facebook/dino-vits16"
model = AutoModel.from_pretrained(model_name, add_pooling_layer=False)
processor = AutoProcessor.from_pretrained(model_name)

# Pasirenkama referencinė veido nuotrauka
print("Pasirinkite referencinę veido nuotrauką:")
reference_face_path = upload_file("Pasirinkite referencinę veido nuotrauką")
if not reference_face_path:
    print("Failo pasirinkimas atšauktas.")
    exit()

reference_img = cv2.imread(reference_face_path)
if reference_img is None:
    raise FileNotFoundError(f"Klaida: nepavyko įkelti nuotraukos iš {reference_face_path}. Patikrinkite failo kelią.")

# Pasirenkamas video failas
print("Pasirinkite video failą:")
video_path = upload_file("Pasirinkite video failą")
if not video_path:
    print("Failo pasirinkimas atšauktas.")
    exit()

# Inicijuojamas veidų aptikimo Haar kaskadas
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Įkeliamas video
cap = cv2.VideoCapture(video_path)

# Nuskaitomos video savybės
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Nustatomi codec ir sukuriame VideoWriter
output_video = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

# Apdorojama referencinė nuotrauka
inputs_ref = processor(images=reference_img, return_tensors="pt")
embeddings_ref = model(**inputs_ref).last_hidden_state.mean(dim=1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Konvertuojamas kadras į pilką vaizdą veidų aptikimui
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aptinkami veidai
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]
        try:
            # Apdorojamas veido regionas
            inputs_face = processor(images=face_roi, return_tensors="pt")
            embeddings_face = model(**inputs_face).last_hidden_state.mean(dim=1)

            # Skaičiuojamas kosinuso panašumas
            similarity = torch.nn.functional.cosine_similarity(embeddings_ref, embeddings_face)

            if similarity > 0.85:
                # Nubrėžiamas stačiakampis ir įrašomas panašumo rezultatas
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Match: {similarity.item():.2f}", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        except Exception as e:
            print(f"Error processing face: {e}")
            continue

    output_video.write(frame)  # Įrašomas kadras į rezultatų video

# Atlaisvinami resursai
cap.release()
output_video.release()
cv2.destroyAllWindows()
print("Face tracking completed. Output saved as 'output_video.mp4'")