import requests

with open("test.jpg", "rb") as img:
    response = requests.post("http://localhost:8000/api/v1/procesar", files={"image": img})
    if response.ok and response.headers.get("Content-Type", "").startswith("image/"):
        with open("resultado_api.jpg", "wb") as out:
            out.write(response.content)
        print("Imagen procesada desde API guardada como resultado_api.jpg")
    else:
        print(f"Error API: {response.status_code} - {response.text}")