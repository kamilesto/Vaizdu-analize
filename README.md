## Veidų Atpažinimo Sistemos – ND1, ND2, ND3

Prieš failų paleidimus įdiegite reikalingas bibliotekas Python terminale su šia komanda:

   pip install -r requirements.txt
   
Jei kyla problemų, bandykite rankiniu būdu:

   pip install tensorflow keras opencv-python numpy pillow deepface retinaface torch transformers tk flask gradio-client huggingface_hub


### 1 ND – Veidų Atpažinimo ir blur efekto taikymo Sistema

Sistemos Paleidimo Instrukcijos:
1. Paleiskite programą terminale:
   python nd1.py
2. Naudojimosi žingsniai:
   - Pasirinkite nuotrauką su keliais žmonėmis.
   - Pasirinkite norimą atpažinti veidą.
   - Programa pažymės identifikuotą veidą ir kitiems veidams pritaikys blur efektą.
   - Galutinis rezultatas bus rodomas ekrane ir išsaugotas kaip failas.

Naudoti metodai:
- Veidų aptikimas: RetinaFace.
- Veidų atpažinimas: DeepFace su ArcFace.
- Neryškumo efektas: Gaussian Blur.
- Failų pasirinkimas: Tkinter.

Iškilusios problemos ir sprendimai:
1. Netikslus aptikimas su Haar Cascade, pakeista į RetinaFace.
2. Netikslus DeepFace atpažinimas, pridėtas klaidų valdymas ir slenkstinė reikšmė.
3. Programa nulūžta be veidų, pridėta išankstinė patikra.
---

### 2 ND – Veidų Atpažinimo Vaizdo Įraše Sistema

Bibliotekos:
- OpenCV, PyTorch, Transformers, Tkinter.

Metodai:
- Veidų aptikimas: Haar Cascade.
- Embedding generavimas: DINO-ViT (Transformer modelis).
- Panašumo skaičiavimas: Kosinuso panašumas.
- Vaizdo apdorojimas: Visi kadrai analizuojami ir pažymimi atpažinti veidai.

Sistemos veikimo aprašymas:
1. Pasirinkite referencinį veidą ir vaizdo įrašą.
2. Kiekviename kadre aptinkami veidai, kuriami embedding ir palyginami su referenciniu veidu.
3. Jei panašumas > 0.85, veidas pažymimas žaliu rėmeliu.
4. Sugeneruojamas naujas vaizdo įrašas su pažymėtais veidais.

Iškilusios problemos ir sprendimai:
1. Lėtas Transformer modelis, optimizacija naudojant GPU ("torch.cuda").
2. Tkinter GUI problemos, naudojamas "root.update()".

Sistemos Paleidimo Instrukcijos:
1. Paleiskite programą:
   python nd2.py
---

### 3 ND – Veidų Atpažinimo Web Sistema

Sistemos Paleidimo Instrukcijos:
1. Atidarykite katalogą terminale:
   cd nd3
2. Paleiskite programą:
   python nd3.py
3. Web sąsajos naudojimas:
   - Terminale pasirodys nuoroda, kuri turėtų būti: http://127.0.0.1:5000, ir ją atidarykite naršyklėje.
   - Įkelkite pagrindinę nuotrauką ir referencinį veidą.
   - Tada matysite apdorotą rezultatą su pažymėtais veidais.

Bibliotekos:
- Flask, OpenCV, PIL, DeepFace, RetinaFace, Gradio, Hugging Face API.

Naudoti metodai:
- Veidų aptikimas: RetinaFace.
- Veidų atpažinimas: DeepFace su ArcFace.
- Neryškumo efektas: Gaussian Blur.
- API komunikacija: Flask siunčia užklausas į Hugging Face serverį.

Iškilusios problemos ir sprendimai:
1. TensorFlow, Keras priklausomybių konfliktai, spręsta per rankinį diegimą.
2. Netinkamas failų kelias Flask API, išsaugoma "static/" kataloge.

*Papildomi komentarai:*
- Modelis įkeltas į Hugging Face: https://huggingface.co/spaces/kamilesto/faceRecognation
