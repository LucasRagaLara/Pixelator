import os
import pandas as pd
import matplotlib.pyplot as plt

# Leer CSV
df = pd.read_csv("metricas_rendimiento.csv")
plt.style.use("ggplot")

# Colores asignados por servicio
colores = {
    "bbox": "#1f77b4",
    "classifier": "#ff7f0e",
    "pixelator": "#2ca02c",
    "engine": "#d62728",
    "api": "#9467bd"
}

# Posición para mostrar los promedios a la derecha del gráfico
x_pos = df["Repeticion"].max() + 0.6

# Desplazamiento vertical para evitar que se solapen
offset = {
    "bbox": 0.004,
    "classifier": -0.003,
    "pixelator": 0.01,
    "engine": 0.005,
    "api": -0.008
}

plt.figure(figsize=(11, 6))

# Dibujar cada serie
for columna in df.columns:
    if columna != "Repeticion":
        plt.plot(
            df["Repeticion"],
            df[columna],
            label=columna,
            marker="o",
            linewidth=2,
            markersize=6,
            color=colores.get(columna)
        )
        avg = df[columna].mean()
        plt.text(
            x_pos,
            df[columna].iloc[-1] + offset.get(columna, 0),
            f"{avg:.3f}s",
            fontsize=9,
            color=colores.get(columna),
            ha="left"
        )

# Configuración del gráfico
plt.title("Evolución del tiempo de respuesta por microservicio", fontsize=14, fontweight="bold")
plt.xlabel("Repetición", fontsize=12)
plt.ylabel("Tiempo (segundos)", fontsize=12)
plt.xticks(range(1, df["Repeticion"].max() + 1))  # Mostrar 1 al 10
plt.xlim(left=0.5, right=df["Repeticion"].max() + 1.5)
plt.ylim(bottom=0)
plt.legend(title="Servicio")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# Guardar el gráfico
plt.savefig("grafico_rendimiento.png", dpi=300)
plt.savefig("grafico_rendimiento.svg")
plt.savefig("grafico_rendimiento.pdf")
plt.show()
