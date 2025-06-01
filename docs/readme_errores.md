## Gestión de Errores en los Servicios de Pixelator

Este documento describe la gestión de errores implementada en cada uno de los servicios de la arquitectura Pixelator. Se actualiza progresivamente por cada servicio.

---

### Servicio `api`

El servicio `api` actúa como punto de entrada principal, encargado de recibir peticiones del usuario y redirigirlas al servicio `engine`. Gestiona distintos tipos de errores para ofrecer respuestas claras y robustas.

#### Errores gestionados directamente

| Código  | Situación                                      | Manejo                                                        |
| ------- | ---------------------------------------------- | ------------------------------------------------------------- |
| **400** | El campo `image` falta en la petición POST     | Retorna texto plano: "Falta el campo 'image'"                 |
| **415** | Formato de imagen no soportado (no JPEG o PNG) | Retorna texto plano: "Formato de imagen no soportado..."      |
| **500** | Error de conexión con el servicio `engine`     | Capturado con `try/except` y devuelve el mensaje de excepción |
| **404** | Ruta no encontrada                             | Manejada con `@app.errorhandler(404)`                         |

#### Detalles de implementación

* **Validación previa**:

  * Se verifica la existencia del campo `image` en `request.files`
  * Se comprueba que el tipo MIME sea `image/jpeg` o `image/png`

* **Errores al contactar `engine`**:

  * Se maneja con `try/except`
  * En caso de fallo, se responde con código `500` y el mensaje de error

* **Errores en la respuesta del `engine`**:

  * Si el contenido de la respuesta no es imagen, se muestra con `print(...)`
  * Se devuelve el contenido tal cual y su código de estado original

* **Errores 404 personalizados**:

  * Si la ruta empieza con `/api/`, se responde en formato JSON:

    ```json
    { "error": "Ruta no encontrada" }
    ```
  * Para rutas web normales, se renderiza la plantilla `404.html`

#### Ejemplos de respuesta

* **Error por imagen ausente o errónea**:

  ```http
  POST /api/v1/procesar
  HTTP/1.1 400 Bad Request
  "Falta el campo 'image'"
  ```

* **Ruta inexistente (modo API)**:

  ```http
  GET /api/v1/desconocido
  HTTP/1.1 404 Not Found
  { "error": "Ruta no encontrada" }
  ```

---

### Servicio `bounding_box`

Este servicio se encarga de detectar rostros dentro de una imagen y devolver sus coordenadas junto con la imagen recortada codificada en base64.

#### Errores gestionados directamente

| Código  | Situación                                     | Manejo                                                       |
| ------- | --------------------------------------------- | ------------------------------------------------------------ |
| **400** | Falta el campo 'image' o la imagen está vacía | Devuelve JSON con el campo `error` explicando el problema    |
| **204** | No se detectaron caras                        | Devuelve JSON con mensaje y código 204                       |
| **500** | Error general en la detección                 | Envuelto en `try/except` y devuelve mensaje JSON explicativo |

#### Detalles de implementación

* **Validación de entrada**:

  * Se verifica que exista el archivo con clave `image`
  * Se comprueba que no esté vacío

* **Errores al abrir o procesar imagen**:

  * `ValueError` si la imagen no puede abrirse: se responde con 400
  * `RuntimeError` si falla MediaPipe: se responde con 500

* **Respuesta sin detecciones**:

  * Si no se detectan caras, se responde con código `204` y mensaje JSON

#### Ejemplos de respuesta

* **Imagen faltante**:

  ```json
  HTTP/1.1 400 Bad Request
  { "error": "No se recibió archivo 'image'" }
  ```

* **Imagen vacía**:

  ```json
  HTTP/1.1 400 Bad Request
  { "error": "La imagen está vacía" }
  ```

* **Ninguna cara detectada**:

  ```json
  HTTP/1.1 204 No Content
  { "error": "No se detectaron caras" }
  ```

* **Error de procesamiento**:

  ```json
  HTTP/1.1 500 Internal Server Error
  { "error": "Error interno en el detector: <mensaje>" }
  ```

---

### Servicio `classifier`

Este servicio clasifica si una cara pertenece a una persona menor de 18 años según una red neuronal previamente entrenada.

#### Errores gestionados directamente

| Código  | Situación                                      | Manejo                               |
| ------- | ---------------------------------------------- | ------------------------------------ |
| **400** | El campo `face` falta o la imagen está vacía   | Devuelve JSON con el error descripto |
| **500** | Error durante el procesamiento o clasificación | Devuelve mensaje JSON con el fallo   |

#### Detalles de implementación

* **Validación de entrada**:

  * Se verifica la existencia del campo `face` en la petición
  * Se comprueba que no esté vacía

* **Errores al cargar o procesar imagen**:

  * `ValueError` para errores durante la lectura o predicción de la imagen
  * `Exception` genérica para otros errores imprevistos

#### Ejemplos de respuesta

* **Imagen ausente**:

  ```json
  HTTP/1.1 400 Bad Request
  { "error": "No se recibió archivo 'face'" }
  ```

* **Imagen vacía**:

  ```json
  HTTP/1.1 400 Bad Request
  { "error": "La imagen está vacía" }
  ```

* **Error en predicción**:

  ```json
  HTTP/1.1 400 Bad Request
  { "error": "Error al procesar la imagen: <mensaje>" }
  ```

* **Error interno del clasificador**:

  ```json
  HTTP/1.1 500 Internal Server Error
  { "error": "Error interno en el clasificador: <mensaje>" }
  ```

---

### Servicio `engine`

Este servicio orquesta toda la lógica de detección, clasificación y pixelado. Recibe una imagen completa, detecta caras, clasifica edad y aplica pixelado si corresponde.

#### Errores gestionados directamente

| Código  | Situación                                                | Manejo                                                   |
| ------- | -------------------------------------------------------- | -------------------------------------------------------- |
| **400** | La imagen no se pudo leer desde `request.files`          | Devuelve JSON con mensaje: `"No se pudo leer la imagen"` |
| **500** | Fallo de conexión con `bbox`, `classifier` o `pixelator` | Devuelve JSON con mensaje de error genérico              |
| **200** | No se detectaron caras en la imagen                      | Devuelve JSON con `"error": "No se detectaron caras..."` |

#### Detalles de implementación

* **Validación de la imagen recibida**:

  * Se intenta leer desde `request.files['image']`
  * Si falla, se responde con `400`

* **Errores en llamadas a servicios internos (`bbox`, `classifier`, `pixelator`)**:

  * Manejados con `try/except`
  * Se usa `requests.post(...).raise_for_status()`
  * Si alguna llamada falla, se responde con `500`

* **Resultado sin caras detectadas**:

  * Se comprueba si `faces` está vacío
  * Si no hay detecciones, se devuelve mensaje con código `200`

* **Errores individuales por cara**:

  * Si una cara falla durante clasificación o pixelado, se ignora con `continue`
  * Esto permite procesar las demás caras

* **Error general**:

  * Cualquier otro error durante el procesamiento completo se captura con `except` y retorna `500`

#### Ejemplos de respuesta

* **Imagen mal subida**:

  ```json
  HTTP/1.1 400 Bad Request
  { "error": "No se pudo leer la imagen" }
  ```

* **Error en conexión con servicios**:

  ```json
  HTTP/1.1 500 Internal Server Error
  { "error": "No se pudo conectar con el servicio de detección facial" }
  ```

* **Sin caras detectadas**:

  ```json
  HTTP/1.1 200 OK
  { "error": "No se detectaron caras en la imagen." }
  ```

* **Error general de procesamiento**:

  ```json
  HTTP/1.1 500 Internal Server Error
  { "error": "Error durante el procesamiento de la imagen" }
  ```

---

### Servicio `pixelator`

Este servicio se encarga de aplicar un efecto de pixelado a las caras clasificadas como menores de edad.

#### Errores gestionados directamente

| Código  | Situación                            | Manejo                                                        |
| ------- | ------------------------------------ | ------------------------------------------------------------- |
| **400** | Falta el campo `face` o imagen vacía | Devuelve JSON explicativo del error                           |
| **400** | Error al abrir la imagen             | Capturado con `try/except`, mensaje detallado                 |
| **500** | Error durante el proceso de pixelado | Devuelve JSON con mensaje detallado del fallo                 |
| **500** | Error al guardar la imagen procesada | Devuelve JSON explicando que no se pudo guardar correctamente |

#### Detalles de implementación

* **Validación del archivo recibido**:

  * Verifica existencia y contenido de `request.files['face']`

* **Errores al abrir la imagen**:

  * Captura errores con `try/except`, respuesta con `400`

* **Errores durante el pixelado o guardado**:

  * Si ocurre algún fallo en el procesamiento, se devuelve `500` con mensaje explicativo

#### Ejemplos de respuesta

* **Imagen vacía**:

  ```json
  HTTP/1.1 400 Bad Request
  { "error": "La imagen recibida está vacía" }
  ```

* **Fallo en apertura de imagen**:

  ```json
  HTTP/1.1 400 Bad Request
  { "error": "No se pudo abrir la imagen: <mensaje>" }
  ```

* **Fallo durante el pixelado**:

  ```json
  HTTP/1.1 500 Internal Server Error
  { "error": "Error durante el proceso de pixelado: <mensaje>" }
  ```

* **Fallo al guardar la imagen**:

  ```json
  HTTP/1.1 500 Internal Server Error
  { "error": "No se pudo guardar la imagen procesada: <mensaje>" }
  ```