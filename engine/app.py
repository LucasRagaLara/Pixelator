# === engine/app.py ===
from flask import Flask, request, send_file
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/handle", methods=["POST"])
def handle():
    image_bytes = request.files["image"].read()

    # Paso 1: Enviar imagen completa a BBOX
    r_bbox = requests.post("http://bbox:5001/detect", files={"image": BytesIO(image_bytes)})
    faces = r_bbox.json()["faces"]
    print("Caras detectadas por bbox:", len(faces))

    # CODIGO COMENTADO TEMPORALMENTE PARA PRUEBAS
    # resultado_faces = []
    # for face_bytes in faces:
    #     face_io = BytesIO(bytes(face_bytes))
    #
    #     # Paso 2: Clasificar
    #     r_clf = requests.post("http://classifier:5002/classify", files={"face": face_io})
    #     is_minor = r_clf.json()["menor"]
    #     print("Clasificada como menor:", is_minor)
    #
    #     # Paso 3: Pixelar si es menor
    #     face_io.seek(0)
    #     if is_minor:
    #         r_pix = requests.post("http://pixelator:5003/pixelate", files={"face": face_io})
    #         resultado_faces.append(r_pix.content)
    #     else:
    #         face_io.seek(0)
    #         resultado_faces.append(face_io.read())
    #
    # print("Caras procesadas:", len(resultado_faces))
    #
    # if resultado_faces:
    #     print("Tamaño de la primera cara (bytes):", len(resultado_faces[0]))
    #     return send_file(BytesIO(resultado_faces[0]), mimetype="image/jpeg")
    # else:
    #     print("❌ No se detectaron caras. No se devuelve imagen.")
    #     return "No se detectaron caras", 204

    # CODIGO HABILITADO TEMPORALMENTE PARA PRUEBAS
    resultado_faces = []

    for i, face_bytes in enumerate(faces):
        face_io = BytesIO(bytes(face_bytes))

        # Paso 2: Clasificar
        r_clf = requests.post("http://classifier:5002/classify", files={"face": face_io})
        is_minor = r_clf.json()["menor"]
        print(f"Rostro {i+1} clasificado como:", "MENOR" if is_minor else "MAYOR")

        # Paso 3: Pixelar si es menor
        face_io.seek(0)
        if is_minor:
            r_pix = requests.post("http://pixelator:5003/pixelate", files={"face": face_io})
            resultado_faces.append(r_pix.content)
        else:
            face_io.seek(0)
            resultado_faces.append(face_io.read())

    if resultado_faces:
        print("Devolviendo imagen procesada (primer rostro)")
        return send_file(BytesIO(resultado_faces[0]), mimetype="image/jpeg")
    else:
        print("No se detectaron caras. No se devuelve imagen.")
        return "No se detectaron caras", 204

app.run(host="0.0.0.0", port=5000)