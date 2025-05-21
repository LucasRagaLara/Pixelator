import os
import requests
from PIL import Image
from io import BytesIO

# Ruta a la imagen real que usarás como simulación de cara
ruta_actual = os.path.dirname(os.path.abspath(__file__))
imagen_path = os.path.join(ruta_actual, "imagen.jpg")
salida_path = os.path.join(ruta_actual, "test_pix.jpg")

# Enviar al pixelator
url_pixelator = "http://localhost:5003/pixelate"

with open(imagen_path, "rb") as f:
    files = {"face": f}
    data = {"is_minor": "True"}
    response = requests.post(url_pixelator, files=files, data=data)

# Verificamos si respondió correctamente
if response.status_code != 200:
    print(f"❌ Error HTTP {response.status_code}")
    print("Respuesta:", response.text)
    exit(1)

# Guardar archivo de salida
with open(salida_path, "wb") as f:
    f.write(response.content)

print(f"✅ Imagen guardada en {salida_path}")
print(f"📦 Tamaño recibido: {len(response.content)} bytes")

# Validar que sea una imagen real
try:
    img = Image.open(BytesIO(response.content))
    img.verify()
    print("✅ La imagen devuelta por pixelator ES válida.")
except Exception as e:
    print("❌ La imagen devuelta está corrupta o no es JPEG válido.")
    print("Error:", e)

    # Guardar los primeros bytes para inspección
    hex_preview = response.content[:20].hex(" ")
    print("🔍 Primeros bytes del archivo recibido:", hex_preview)
