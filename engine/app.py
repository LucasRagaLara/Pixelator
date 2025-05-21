from flask import Flask, request, send_file, jsonify
import requests
from io import BytesIO
from PIL import Image
import base64
import numpy as np
import sys
sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)

@app.route("/handle", methods=["POST"])
def handle():
    image_bytes = request.files["image"].read()

    # Paso 1: Enviar imagen a BBOX y obtener caras + coordenadas
    r_bbox = requests.post("http://bbox:5001/detect", files={"image": BytesIO(image_bytes)})
    if r_bbox.status_code != 200:
        print("❌ No se detectaron caras.")
        return jsonify({"error": "No se detectaron caras en la imagen."}), 200

    bbox_result = r_bbox.json()
    print("Caras detectadas por bbox:", len(bbox_result["faces"]))

    # Abrir imagen original
    original_img = Image.open(BytesIO(image_bytes)).convert("RGB")
    original_np = np.array(original_img)

    for i, face_data in enumerate(bbox_result["faces"]):
        face_bytes = base64.b64decode(face_data["image"])
        x1, y1, x2, y2 = face_data["bbox"]
        face_io = BytesIO(face_bytes)

        # Paso 2: Clasificar
        r_clf = requests.post("http://classifier:5002/classify", files={"face": face_io})
        is_minor = r_clf.json()["menor"]
        print(f"Rostro {i+1} clasificado como:", "MENOR" if is_minor else "MAYOR")

        face_io.seek(0)
        if is_minor:
            # Paso 3: Pixelar
            r_pix = requests.post("http://pixelator:5003/pixelate", files={"face": face_io})
            with open(f"cara_pixelada_{i}.jpg", "wb") as f:
                f.write(r_pix.content)
            print(f"🧪 Imagen cara_pixelada_{i}.jpg guardada en contenedor")
            cara_modificada = Image.open(BytesIO(r_pix.content)).convert("RGB") 
            cara_modificada.save(f"debug_face_pixelada_{i}.jpg")
        else:
            cara_modificada = Image.open(face_io).convert("RGB")

        # Redimensionar para que encaje en el bbox original
        cara_redimensionada = cara_modificada.resize((x2 - x1, y2 - y1))
        cara_array = np.array(cara_redimensionada)

        if cara_array.shape[0] == (y2 - y1) and cara_array.shape[1] == (x2 - x1):
            original_np[y1:y2, x1:x2] = cara_array
        else:
            print(f"⚠️ Mismatch: cara={cara_array.shape}, esperado=({y2 - y1}, {x2 - x1})")

    # Convertir de nuevo a imagen
    imagen_final = Image.fromarray(original_np)
    output = BytesIO()
    imagen_final.save(output, format="JPEG", quality=95)
    output.seek(0)

    print("Imagen recompuesta enviada al cliente")
    return send_file(output, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)