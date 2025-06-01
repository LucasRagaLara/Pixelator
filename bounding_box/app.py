from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import cv2
import io
import mediapipe as mp
import base64

app = Flask(__name__)

# Inicializar detector de MediaPipe una vez
mp_face_detection = mp.solutions.face_detection
detector = mp_face_detection.FaceDetection(
    model_selection=1,
    min_detection_confidence=0.5
)

def detectar_caras(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise ValueError(f"No se pudo abrir la imagen: {str(e)}")

    image_np = np.array(image)
    h, w, _ = image_np.shape

    try:
        results = detector.process(cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
    except Exception as e:
        raise RuntimeError(f"Error al procesar la imagen con MediaPipe: {str(e)}")

    resultados = []
    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            x1 = int(bbox.xmin * w)
            y1 = int(bbox.ymin * h)
            x2 = int((bbox.xmin + bbox.width) * w)
            y2 = int((bbox.ymin + bbox.height) * h)

            x1, y1 = max(x1, 0), max(y1, 0)
            x2, y2 = min(x2, w), min(y2, h)

            rostro_rgb = image_np[y1:y2, x1:x2]
            rostro_bgr = cv2.cvtColor(rostro_rgb, cv2.COLOR_RGB2BGR)

            success, buffer = cv2.imencode(".jpg", rostro_bgr)
            if success:
                encoded = base64.b64encode(buffer).decode("utf-8")
                resultados.append({
                    "image": encoded,
                    "bbox": [x1, y1, x2, y2]
                })

    return resultados

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if "image" not in request.files:
            return jsonify(error="No se recibió archivo 'image'"), 400

        image_bytes = request.files["image"].read()
        if not image_bytes:
            return jsonify(error="La imagen está vacía"), 400

        caras = detectar_caras(image_bytes)

        if not caras:
            return jsonify(error="No se detectaron caras"), 204

        return jsonify({"faces": caras})

    except ValueError as ve:
        return jsonify(error=str(ve)), 400
    except Exception as e:
        return jsonify(error=f"Error interno en el detector: {str(e)}"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)