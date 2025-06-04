from flask import Flask, request, send_file, jsonify
import requests
from io import BytesIO
from PIL import Image
import base64
import numpy as np
import os
import cv2

app = Flask(__name__)

@app.route("/handle", methods=["POST"])
def handle():
    try:
        image_bytes = request.files["image"].read()
    except Exception:
        return jsonify({"error": "No se pudo leer la imagen"}), 400

    # Paso 1: Detección de caras (BBOX)
    try:
        r_bbox = requests.post("http://bbox:5001/detect", files={"image": BytesIO(image_bytes)}, timeout=5)
        r_bbox.raise_for_status()
        bbox_result = r_bbox.json()
    except Exception:
        return jsonify({"error": "No se pudo conectar con el servicio de detección facial"}), 500

    if not bbox_result.get("faces"):
        return jsonify({"error": "No se detectaron caras en la imagen."}), 200

    try:
        original_img = Image.open(BytesIO(image_bytes)).convert("RGB")
        original_np = np.array(original_img)

        for face_data in bbox_result["faces"]:
            try:
                face_bytes = base64.b64decode(face_data["image"])
                x1, y1, x2, y2 = face_data["bbox"]
                face_io = BytesIO(face_bytes)

                # Paso 2: Clasificación de edad
                r_clf = requests.post("http://classifier:5002/classify", files={"face": face_io}, timeout=5)
                r_clf.raise_for_status()
                clf_data = r_clf.json()
                is_minor = clf_data.get("menor", False)
                score = clf_data.get("score", 0.0)
                face_io.seek(0)

                # Paso 3: Pixelado si es menor
                if is_minor:
                    r_pix = requests.post("http://pixelator:5003/pixelate", files={"face": face_io}, timeout=5)
                    r_pix.raise_for_status()
                    cara_modificada = Image.open(BytesIO(r_pix.content)).convert("RGB")
                else:
                    cara_modificada = Image.open(face_io).convert("RGB")

                # Redimensionar y reemplazar en la imagen original
                cara_redimensionada = cara_modificada.resize((x2 - x1, y2 - y1))
                cara_array = np.array(cara_redimensionada)

                if cara_array.shape[:2] == (y2 - y1, x2 - x1):
                    original_np[y1:y2, x1:x2] = cara_array

                    # Colores: rojo (menor), verde (mayor)
                    color = (0, 255, 0) if not is_minor else (0, 0, 255)

                    # Dibujar recuadro
                    cv2.rectangle(original_np, (x1, y1), (x2, y2), color, thickness=3)

                    # Dibujar texto con score
                    label = f"{'Menor' if is_minor else 'Mayor'} ({score:.2f})"
                    font_scale = 0.6
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    thickness = 2
                    (text_width, text_height), _ = cv2.getTextSize(label, font, font_scale, thickness)

                    # Coordenadas para el texto encima del recuadro
                    text_x = x1
                    text_y = y1 - 10 if y1 - 10 > text_height else y1 + text_height + 10

                    cv2.putText(original_np, label, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

            except Exception:
                # Si falla un rostro, lo saltamos sin interrumpir todo el proceso
                continue

        # Imagen final
        imagen_final = Image.fromarray(original_np)
        output = BytesIO()
        imagen_final.save(output, format="JPEG", quality=95)
        output.seek(0)

        return send_file(output, mimetype="image/jpeg")

    except Exception:
        return jsonify({"error": "Error durante el procesamiento de la imagen"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)