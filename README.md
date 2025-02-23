## Veidų Atpažinimo Sistemos – ND1, ND2, ND3

Prieš failų paleidimus įdiegite reikalingas bibliotekas Python terminale su šia komanda:<br>
   pip install -r requirements.txt<br>
Jei kyla problemų, bandykite rankiniu būdu:<br>
   pip install tensorflow keras opencv-python numpy pillow deepface retinaface torch transformers tk flask gradio-client huggingface_hub

Mano naudoti pavyzdžiai:
- Referencinė nuotrauka: person.jpg
- Žmonių nuotrauka: people.jpg
- Žmonių vaizdo įrašas: people1_video.mp4<br>
rezultatai:
- result.png ir processed_result.png (nd3/static/results)
- output_video.mp4

### 1 ND – Veidų Atpažinimo ir blur efekto taikymo Sistema

Sistemos Paleidimo Instrukcijos:
1. Paleiskite programą terminale:<br>
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


*Papildomi komentarai:*
- Pasibandymui naudojau people.jpg ir person.jpg, kurio rezultatas matomas result.png.
---

### 2 ND – Veidų Atpažinimo Vaizdo Įraše Sistema

Sistemos Paleidimo Instrukcijos:
1. Paleiskite programą:<br>
   python nd2.py

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

*Papildomi komentarai:*
- Pasibandymui naudojau person.jpg ir people1_video.mp4, kurio rezultatas matomas output_video.mp4.
---

### 3 ND – Veidų Atpažinimo Web Sistema

Sistemos Paleidimo Instrukcijos:
1. Atidarykite katalogą terminale:<br>
   cd nd3
2. Paleiskite programą:<br>
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
- Python failai buvo kuriami Visual Studio Code aplinkoje, 3ND svetainės stilius sukurtas templates/index.html faile.
