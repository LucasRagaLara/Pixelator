from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Cargar modelo entrenado
modelo = tf.keras.models.load_model("children_vs_adults_model.keras")

# Clasificación binaria: 1 = menor, 0 = mayor
def predecir_edad(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
    img_array = tf.keras.utils.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    pred = modelo.predict(img_array)[0][0]
    return int(pred < 0.5)

@app.route("/classify", methods=["POST"])
def classify():
    face_bytes = request.files["face"].read()
    menor = predecir_edad(face_bytes)
    return jsonify({"menor": bool(menor)})

app.run(host="0.0.0.0", port=5002)