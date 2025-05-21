import os
import requests

# Simulamos una cara (puedes usar el mismo archivo imagen.jpg)
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_face = os.path.join(ruta_actual, "imagen.jpg")

# URL del clasificador
url_classifier = "http://localhost:5002/classify"

# Enviar la imagen
with open(ruta_face, "rb") as face_file:
    files = {"face": face_file}
    response = requests.post(url_classifier, files=files)

# Mostrar resultado
print("Status Code:", response.status_code)
try:
    data = response.json()
    print("Respuesta JSON:", data)
except Exception as e:
    print("❌ Error interpretando JSON:", e)
    print("Texto recibido:", response.text)
