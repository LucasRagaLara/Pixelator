from flask import Flask, request, Response, render_template
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

    try:
        response = requests.post("http://engine:5000/handle", files={"image": file})
    except Exception as e:
        return f"Error al conectar con engine: {e}", 500

    return Response(response.content, content_type="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)