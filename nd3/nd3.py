import os
import shutil
import time
from flask import Flask, request, render_template, send_from_directory
from gradio_client import Client, handle_file
from PIL import Image

# Sukuriami katalogai
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HF_API_URL = "kamilesto/facerecognation"

def process_image(image_path, reference_path):
    # Kreipiasi į Hugging Face API ir grąžina apdorotą vaizdą.
    client = Client(HF_API_URL)
    # Kviečiamas API
    result_path = client.predict(
        input_img=handle_file(image_path),
        reference_img=handle_file(reference_path),
        api_name="/predict"
    )
    print("API grąžintas kelias:", result_path)

    # Jei API grąžino failo kelią
    if isinstance(result_path, str) and os.path.exists(result_path):
        local_path = os.path.join(RESULT_FOLDER, "processed_result.webp")
        shutil.copy(result_path, local_path)

        image = Image.open(local_path).convert("RGB")
        png_path = os.path.join(RESULT_FOLDER, "processed_result.png")
        image.save(png_path, "PNG")

        time.sleep(1)

        if os.path.exists(png_path):
            png_url = f"/static/results/processed_result.png"  # Normalizuotas kelias
            print("Flask išsaugojo PNG:", png_url)
            return png_url
        else:
            print("Klaida: PNG failas nebuvo sukurtas!")
            return None
    else:
        print("API grąžino netinkamą failą:", result_path)
        return None

@app.route('/')
def index():
    # Apdorojami vaizdai ir rodomi HTML puslapyje
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Įkelia vaizdus, kviečia API ir grąžina rezultatą
    if 'image' not in request.files or 'reference' not in request.files:
        return "Klaida: Trūksta įkeltų failų"

    image_file = request.files['image']
    reference_file = request.files['reference']

    if image_file.filename == '' or reference_file.filename == '':
        return "Klaida: Pasirinkti failai negali būti tušti"

    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    reference_path = os.path.join(UPLOAD_FOLDER, reference_file.filename)

    image_file.save(image_path)
    reference_file.save(reference_path)

    result_image = process_image(image_path, reference_path)

    return render_template("index.html", result_image=result_image)

@app.route('/static/results/<filename>')
def get_result_image(filename):
    """ Pateikia apdorotą vaizdą per Flask. """
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)