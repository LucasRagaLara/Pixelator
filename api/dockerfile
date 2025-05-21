# === api/Dockerfile ===
FROM python:3.10-slim

WORKDIR /app

# Copiamos solo primero el requirements.txt para aprovechar cache de Docker
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Comando para arrancar Flask
CMD ["python", "app.py"]