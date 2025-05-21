import requests
from PIL import Image
import io
import os

# Ruta al archivo actual
ruta_actual = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(ruta_actual, "imagen4.jpg")

url = "http://localhost:8000/api/v1/procesar"

with open(img_path, "rb") as f:
    response = requests.post(url, files={"image": f})

print("Status:", response.status_code)
print("Tamaño respuesta:", len(response.content), "bytes")

if response.status_code == 200 and len(response.content) > 10:
    try:
        img = Image.open(io.BytesIO(response.content))
        img.show()
        img.save(os.path.join(ruta_actual, "resultado.jpg"))
        print("✅ Imagen guardada como resultado.jpg")
    except Exception as e:
        print("❌ No se pudo abrir como imagen:", e)
        with open(os.path.join(ruta_actual, "resultado_raw.bin"), "wb") as f:
            f.write(response.content)
        print("🧪 Respuesta binaria guardada como resultado_raw.bin para inspección")
else:
    print("❌ Error:", response.status_code, response.text)