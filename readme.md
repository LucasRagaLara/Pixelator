# Pixelador de Caras

Sistema automático de anonimización de imágenes que detecta rostros, clasifica si pertenecen a menores de edad y los pixeliza si es necesario. Está diseñado como un sistema de microservicios en Docker, totalmente escalable, eficiente y usable desde una interfaz web.

## ¿Qué hace este sistema?

1. Recibe una imagen desde una API o frontend web.
2. Detecta rostros mediante un servicio de detección de caras (bbox).
3. Clasifica cada rostro (menor o mayor de edad) con un modelo propio entrenado en TensorFlow.
4. Pixeliza los rostros de menores respetando su privacidad.
5. Devuelve la imagen procesada al usuario.
6. Todo se realiza en segundos, con feedback visual y mensajes desde el frontend.

## Arquitectura del sistema

El sistema se estructura en 5 microservicios independientes:

* `api/`: interfaz principal que recibe las imágenes.
* `engine/`: orquestador que conecta los servicios.
* `bounding_box/`: detección facial mediante Mediapipe.
* `classifier/`: red neuronal que clasifica si el rostro es de un menor.
* `pixelator/`: aplica el pixelado solo si corresponde.

Estos servicios se comunican vía HTTP y corren en contenedores Docker, permitiendo escalabilidad y aislamiento.

## Estructura del proyecto

```
Pixelator/
├── api/
│   └── static/  
│   └── templates/  
├── bounding_box/
├── caras/
├── classifier/
├── docs/
├── engine/
├── models/
├── pixelator/
├── pruebas/
│   └── rendimiento/        
│   └── testing/       
├── docker-compose.yaml
├── dockerfile
├── readme.md
├── resultado_final.bin
└── docs/README_errores.md   
```

## Tecnologías utilizadas

* Python 3.10
* TensorFlow + Keras
* OpenCV
* Flask
* Docker
* Tailwind CSS
* HTML + JavaScript
* Mediapipe / Haar cascades

## Modelo de Clasificación

* Entrenado desde cero con imágenes recortadas de caras.
* Dataset balanceado (adultos vs menores).
* Ajustado con `class_weight` y búsqueda de threshold óptimo por F1-score.

**Métricas finales:**

```
Accuracy:     0.85
F1-score:     0.83
Precision:    0.90 (menores)
Recall:       0.70 (menores)
```

## Cómo levantar el proyecto

1. Clona el repositorio:

```bash
git clone https://github.com/LucasRagaLara/Pixelator.git
cd Pixelator
```

2. Asegúrate de tener Docker instalado.

3. Ejecuta los servicios:

```bash
docker-compose -p api-pixel build
docker-compose -p api-pixel up
```

4. Abre el navegador en:

```
http://localhost:8000/api
```

## Cómo probar la API

Puedes subir una imagen desde la interfaz web para probar todo el flujo.
Alternativamente, puedes usar herramientas como Postman o `curl`:

```bash
curl -X POST -F "image=@ruta/a/imagen.jpg" http://localhost:8000/api/v1/procesar --output salida.jpg
```

## Entrenamiento del modelo

Para reentrenar el modelo de clasificación:

```bash
cd models
# Abre y ejecuta modelo_edad.ipynb con Jupyter Notebook
```

Se recomienda usar **TensorFlow con soporte para GPU**, ya que el entrenamiento puede ser costoso computacionalmente.

## Casos de uso

* Anonimización en medios de comunicación
* Tratamiento de imágenes escolares
* Herramientas de privacidad para menores en redes sociales
* Censura automática en contextos legales

## Métricas visuales

La interfaz incluye gráficas y contadores para visualizar:

* Número de imágenes procesadas
* Porcentaje de detección efectiva
* Tiempos de respuesta
* Métricas de precisión, recall, F1-score y pérdida

## Pruebas unitarias

Para ejecutar pruebas individuales sobre los servicios, consulta la carpeta:

```
pruebas/testing/
```

Allí encontrarás ejemplos que permiten validar detección, clasificación y pixelado por separado.

## Gestión de Errores por Servicio

Consulta el documento completo aquí:

[`docs/README_errores.md`](docs/README_errores.md)

Allí se detalla cómo responde cada microservicio ante situaciones como imágenes inválidas, servicios desconectados, errores de clasificación o fallos internos.

## Autoría y agradecimientos

Desarrollado como parte de un proyecto académico por:

* Carla Ruiz y Lucas Raga — Desarrollo completo, modelo IA, backend y frontend

## Licencia

MIT — Puedes usarlo, modificarlo y compartirlo. Pero da crédito.