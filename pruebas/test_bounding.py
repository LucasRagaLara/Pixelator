import os
import requests

# Ruta a la imagen de prueba
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_imagen = os.path.join(ruta_actual, "imagen.jpg")  # ← usa tu imagen de prueba

# URL del microservicio bbox
url_bbox = "http://localhost:5001/detect"

# Enviar la imagen
with open(ruta_imagen, "rb") as img:
    files = {"image": img}
    response = requests.post(url_bbox, files=files)

# Mostrar resultado
print("Status Code:", response.status_code)
try:
    data = response.json()
    print("Respuesta JSON:", data)
except Exception as e:
    print("❌ Error interpretando JSON:", e)
    print("Texto recibido:", response.text)