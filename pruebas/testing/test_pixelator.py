import requests

with open("cara_bebe.jpg", "rb") as face:
    response = requests.post("http://localhost:5003/pixelate", files={"face": face})
    if response.ok and response.headers.get("Content-Type", "").startswith("image/"):
        with open("pixelated_test_face.jpg", "wb") as out:
            out.write(response.content)
        print("Imagen pixelada guardada como pixelated_test_face.jpg")
    else:
        print(f"Error Pixelator: {response.status_code} - {response.text}")