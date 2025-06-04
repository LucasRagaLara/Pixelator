from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Cargar el modelo una vez al iniciar
try:
    modelo = tf.keras.models.load_model("modelo_final.h5")
except Exception as e:
    raise RuntimeError(f"No se pudo cargar el modelo: {str(e)}")

THRESHOLD = 0.738

def predecir_edad(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        pred = modelo.predict(img_array)[0][0]
        menor = int(pred > THRESHOLD)
        return menor, float(pred)
    except Exception as e:
        raise ValueError(f"Error al procesar la imagen: {str(e)}")

@app.route("/classify", methods=["POST"])
def classify():
    try:
        if "face" not in request.files:
            return jsonify(error="No se recibió archivo 'face'"), 400

        face_bytes = request.files["face"].read()
        if not face_bytes:
            return jsonify(error="La imagen está vacía"), 400

        menor, score = predecir_edad(face_bytes)
        return jsonify({"menor": bool(menor), "score": round(score, 4)})

    except ValueError as ve:
        return jsonify(error=str(ve)), 400
    except Exception as e:
        return jsonify(error=f"Error interno en el clasificador: {str(e)}"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)