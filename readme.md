# 🧠 Pixelador de Caras

Sistema automático de anonimización de imágenes que detecta rostros, clasifica si pertenecen a menores de edad y los pixeliza si es necesario. Está diseñado como un sistema de microservicios en Docker, totalmente escalable, eficiente y usable desde una interfaz web.

## 🚀 ¿Qué hace este sistema?

1. **Recibe una imagen desde una API o frontend web.**
2. **Detecta rostros** mediante un servicio de detección de caras (bbox).
3. **Clasifica cada rostro** (menor o mayor de edad) con un modelo propio entrenado en TensorFlow.
4. **Pixeliza los rostros** de menores respetando su privacidad.
5. **Devuelve la imagen procesada** al usuario.
6. **Todo se realiza en segundos**, con feedback visual y mensajes desde el frontend.

## 📦 Estructura del proyecto

```bash
Pixelator/
├── api/               # Interfaz principal HTTP
├── engine/            # Orquestador de microservicios
├── bbox/              # Detección de rostros
├── classifier/        # Clasificación por edad
├── pixelator/         # Pixelado de rostros
├── frontend/          # Interfaz web con Tailwind + JS
├── models/            # Modelos Keras (.h5 / .keras)
├── static/            # Recursos estáticos (imágenes, CSS)
└── docker-compose.yaml
```

## 🧰 Tecnologías utilizadas

* **Python 3.10**
* **TensorFlow + Keras** — para el modelo de clasificación de edad
* **OpenCV** — manipulación de imágenes
* **Flask** — microservicios REST
* **Docker** — para contenerización y despliegue
* **Tailwind CSS** — diseño moderno y responsive
* **HTML + JavaScript** — interacción de frontend
* **Mediapipe / Haar cascades** — detección facial

## 📸 Modelo de Clasificación

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

## 🛠️ Cómo levantar el proyecto

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/pixelador-caras.git
cd pixelador-caras
```

2. Asegúrate de tener Docker instalado.

3. Construye y lanza los servicios:

```bash
   docker-compose -p api-pixel build
   docker-compose -p api-pixel up
```

4. Abre el navegador en:
   `http://localhost:8000/api`

## 📊 Entrenamiento del modelo

Si deseas reentrenar el modelo:

```bash
cd models
python modelo_edad.ipynb
```

Ajusta hiperparámetros en `configs`, mejora el dataset o entrena con nuevos umbrales de decisión.

## 🎯 Casos de uso

* Anonimización en medios de comunicación
* Tratamiento de imágenes escolares
* Herramientas de privacidad para menores en redes sociales
* Censura automática en contextos legales

## 📊 Métricas visuales

La interfaz web incluye gráficas y contadores animados para visualizar:

* Nº de imágenes procesadas
* % de detección efectiva
* Tiempos de respuesta
* Logs de clasificación

## ✍️ Autoría y agradecimientos

Desarrollado como parte de un proyecto académico por:

* **Carla Ruiz y Lucas Raga** — Desarrollo completo, modelo IA, backend y frontend
* **Colaboraciones**: mejora de UX, evaluación y testeo de sistema