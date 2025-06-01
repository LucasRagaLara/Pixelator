from flask import Flask, request, send_file, jsonify
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route("/pixelate", methods=["POST"])
def pixelate():
    face_file = request.files.get("face")
    if not face_file:
        return jsonify(error="No se recibió archivo 'face'"), 400

    face_bytes = face_file.read()
    if not face_bytes:
        return jsonify(error="La imagen recibida está vacía"), 400

    try:
        image = Image.open(BytesIO(face_bytes)).convert("RGB")
    except Exception as e:
        return jsonify(error=f"No se pudo abrir la imagen: {str(e)}"), 400

    try:
        # Nivel de pixelado adaptativo según el tamaño del rostro
        w, h = image.size
        pixel_size = max(4, min(w, h) // 10)  # al menos 4px, hasta el 10% del lado menor

        small = image.resize(
            (max(1, w // pixel_size), max(1, h // pixel_size)),
            resample=Image.NEAREST
        )
        image = small.resize((w, h), Image.NEAREST)
    except Exception as e:
        return jsonify(error=f"Error durante el proceso de pixelado: {str(e)}"), 500

    try:
        output = BytesIO()
        image.save(output, format="JPEG", quality=95)
        output.seek(0)
        return send_file(output, mimetype="image/jpeg")
    except Exception as e:
        return jsonify(error=f"No se pudo guardar la imagen procesada: {str(e)}"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
