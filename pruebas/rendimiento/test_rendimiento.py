import time
import requests
import csv

img_path = "imagen.jpg"
face_path = "cara.jpg"

urls = {
    "bbox": "http://localhost:5001/detect",
    "classifier": "http://localhost:5002/classify",
    "pixelator": "http://localhost:5003/pixelate",
    "engine": "http://localhost:5000/handle",
    "api": "http://localhost:8000/api/v1/procesar"
}

N = 10
output_csv = "metricas_rendimiento.csv"

resultados = {key: [] for key in urls}

for _ in range(N):
    with open(img_path, "rb") as f:
        start = time.time()
        requests.post(urls["bbox"], files={"image": f})
        resultados["bbox"].append(time.time() - start)

    with open(face_path, "rb") as f:
        start = time.time()
        requests.post(urls["classifier"], files={"face": f})
        resultados["classifier"].append(time.time() - start)

    with open(face_path, "rb") as f:
        start = time.time()
        requests.post(urls["pixelator"], files={"face": f})
        resultados["pixelator"].append(time.time() - start)

    with open(img_path, "rb") as f:
        start = time.time()
        requests.post(urls["engine"], files={"image": f})
        resultados["engine"].append(time.time() - start)

    with open(img_path, "rb") as f:
        start = time.time()
        requests.post(urls["api"], files={"image": f})
        resultados["api"].append(time.time() - start)

with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Repeticion"] + list(urls.keys()))
    for i in range(N):
        writer.writerow([
            i + 1
        ] + [resultados[svc][i] for svc in urls])