from flask import Flask, request, Response, render_template, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Permite peticiones CORS (útil si se sirve desde otro dominio)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/v1/procesar", methods=["POST"])
def procesar():
    if "image" not in request.files:
        return "Falta el campo 'image'", 400

    file = request.files["image"]

    # Validación de tipo MIME
    if file.mimetype not in ["image/jpeg", "image/png"]:
        return "Formato de imagen no soportado. Solo se permite JPEG o PNG.", 415

    try:
        response = requests.post("http://engine:5000/handle", files={"image": file}, timeout=10)
    except Exception as e:
        return f"Error al conectar con engine: {e}", 500

    content_type = response.headers.get("Content-Type", "")
    if content_type.startswith("image/"):
        return Response(response.content, content_type=content_type)
    else:
        print("El engine devolvió algo que no es imagen:", response.text)
        return response.text, response.status_code

@app.errorhandler(404)
def page_not_found(e):
    # Si la petición es a la API, devolver JSON
    if request.path.startswith("/api/"):
        return jsonify(error="Ruta no encontrada"), 404

    # Si es una ruta web normal, devolver página 404
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)