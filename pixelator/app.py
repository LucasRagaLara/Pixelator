# === pixelator/app.py ===
from flask import Flask, request, send_file
from io import BytesIO
from PIL import Image
import sys

app = Flask(__name__)

@app.route("/pixelate", methods=["POST"])
def pixelate():
    face_file = request.files.get("face")
    if not face_file:
        print("❌ No se recibió archivo 'face'", file=sys.stderr)
        return "No image provided", 400

    face_bytes = face_file.read()
    print(f"✅ Recibidos {len(face_bytes)} bytes", file=sys.stderr)

    if not face_bytes:
        return "Empty image", 400

    try:
        image = Image.open(BytesIO(face_bytes)).convert("RGB")
    except Exception as e:
        print(f"❌ Error al abrir imagen: {e}", file=sys.stderr)
        return f"Error al abrir imagen: {e}", 400

    # ✅ Pixelado real sin interpolación de color
    pixel_size = 10  # Ajusta según el nivel de pixelado deseado
    small = image.resize(
        (image.width // pixel_size, image.height // pixel_size),
        resample=Image.NEAREST
    )
    image = small.resize(image.size, Image.NEAREST)

    output = BytesIO()
    try:
        image.save(output, format="JPEG", quality=95)
        output.seek(0)
        print("✅ Imagen pixelada correctamente", file=sys.stderr)
    except Exception as e:
        print(f"❌ Error al guardar imagen: {e}", file=sys.stderr)
        return f"Error al guardar imagen: {e}", 500

    return send_file(output, mimetype="image/jpeg")

app.run(host="0.0.0.0", port=5003)
