import os
import pandas as pd
import matplotlib.pyplot as plt

# Cargar métricas
df = pd.read_csv("./metricas_rendimiento.csv")

colores = {
    "bbox": "#1f77b4",       # azul
    "classifier": "#ff7f0e", # naranja
    "pixelator": "#2ca02c",  # verde
    "engine": "#d62728",     # rojo
    "api": "#9467bd",        # violeta
}

plt.figure(figsize=(10, 6))
for columna in df.columns:
    if columna != "Repeticion":
        plt.plot(df["Repeticion"], df[columna], marker="o", label=columna)

plt.title("Tiempos de respuesta por servicio")
plt.xlabel("Repetición")
plt.ylabel("Tiempo (s)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()


plt.savefig("grafico_rendimiento.png")

print("Gráfico guardado")