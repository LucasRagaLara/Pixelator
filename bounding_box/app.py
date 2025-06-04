from flask import Flask, request, jsonify
from PIL import Image
import torch
from facenet_pytorch import MTCNN
import numpy as np
import io
import base64
import cv2

app = Flask(__name__)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
detector = MTCNN(keep_all=True, device=device)

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if "image" not in request.files:
            return jsonify(error="No se recibió archivo 'image'"), 400

        image_bytes = request.files["image"].read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        boxes, _ = detector.detect(image)

        if boxes is None or len(boxes) == 0:
            return jsonify(error="No se detectaron caras"), 204

        image_np = np.array(image)
        h_img, w_img = image_np.shape[:2]
        resultados = []

        for box in boxes:
            x1, y1, x2, y2 = [int(coord) for coord in box]
            w, h = x2 - x1, y2 - y1

            # FILTRO 1: tamaño mínimo
            if w < 60 or h < 60:
                continue

            # FILTRO 2: proporción razonable
            aspect_ratio = w / h
            if aspect_ratio < 0.6 or aspect_ratio > 1.6:
                continue

            # Ajustar dentro de los límites
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w_img, x2)
            y2 = min(h_img, y2)

            rostro = image_np[y1:y2, x1:x2]
            _, buffer = cv2.imencode(".jpg", cv2.cvtColor(rostro, cv2.COLOR_RGB2BGR))
            encoded = base64.b64encode(buffer).decode("utf-8")

            resultados.append({
                "image": encoded,
                "bbox": [x1, y1, x2, y2]
            })

        return jsonify({"faces": resultados})

    except Exception as e:
        return jsonify(error=f"Error interno: {str(e)}"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)