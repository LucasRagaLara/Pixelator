import requests

with open("cara_bebe.jpg", "rb") as face:
    response = requests.post("http://localhost:5002/classify", files={"face": face})
    if response.ok:
        print("Clasificación:", response.json())
    else:
        print(f"Error Classifier: {response.status_code} - {response.text}")