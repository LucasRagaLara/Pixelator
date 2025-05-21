import os
import requests
from PIL import Image
from io import BytesIO

# Ruta a la imagen de entrada
ruta_actual = os.path.dirname(os.path.abspath(__file__))
imagen_entrada = os.path.join(ruta_actual, "imagen.jpg")  # Asegúrate de tener esta imagen en el directorio

# Ruta para guardar el resultado
imagen_salida = os.path.join(ruta_actual, "resultado.jpg")

# URL de la API pública
url_api = "http://localhost:8000/procesar"

# Enviar imagen como multipart/form-data
with open(imagen_entrada, "rb") as f:
    files = {"image": f}
    try:
        response = requests.post(url_api, files=files)
    except Exception as e:
        print(f"❌ Error al conectar con la API: {e}")
        exit(1)

# Guardar respuesta si es válida
if response.status_code == 200:
    with open(imagen_salida, "wb") as f:
        f.write(response.content)
    print(f"✅ Imagen procesada guardada en: {imagen_salida}")

    # Verificar que es una imagen válida
    try:
        imagen_resultado = Image.open(BytesIO(response.content))
        imagen_resultado.verify()
        print("✅ La imagen recibida es válida y se puede abrir con PIL.")
    except Exception as e:
        print("❌ La imagen recibida está corrupta.")
        print("Error:", e)

else:
    print(f"❌ Error en la respuesta: HTTP {response.status_code}")
    print(response.text)
