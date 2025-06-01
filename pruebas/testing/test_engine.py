import requests

with open("test.jpg", "rb") as img:
    response = requests.post("http://localhost:5000/handle", files={"image": img})
    if response.ok and response.headers.get("Content-Type", "").startswith("image/"):
        with open("resultado_engine.jpg", "wb") as out:
            out.write(response.content)
        print("Imagen procesada por Engine guardada como resultado_engine.jpg")
    else:
        print(f"Error Engine: {response.status_code} - {response.text}")