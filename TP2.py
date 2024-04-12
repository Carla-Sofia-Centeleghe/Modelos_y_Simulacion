import numpy as np
import matplotlib.pyplot as plt

# Datos del calentador de agua
masa_agua_kg = 1  # Masa de agua en kg
capacidad_termica_agua_J_kgC = 4186  # Capacidad térmica del agua en J/kg°C
potencia_resistencia_W = 1950  # Potencia de la resistencia eléctrica en W
tiempo_simulacion_s = 150  # Tiempo de simulación en segundos
temperatura_inicial_C = 10  # Temperatura inicial del agua en °C
temperatura_objetivo_C = 75  # Temperatura objetivo del agua en °C
delta_t = 1  # Paso del tiempo en segundos

# Inicializo listas para guardar datos de la simulación
tiempo = [0]  # Lista para el tiempo
temperatura = [temperatura_inicial_C]  # Lista para la temperatura

# Realizo la simulación
for t in range(1, tiempo_simulacion_s + 1):
    # Calculo cambio de temperatura usando la potencia de la resistencia
    delta_temperatura = (potencia_resistencia_W * delta_t) / (masa_agua_kg * capacidad_termica_agua_J_kgC)
    nueva_temperatura = temperatura[-1] + delta_temperatura

    # Actualizo listas del tiempo y de la temperatura
    tiempo.append(t)
    temperatura.append(nueva_temperatura)

    # Se detiene la simulación si alcanzo la temperatura objetivo
    if nueva_temperatura >= temperatura_objetivo_C:
        break

# Grafico los resultados
plt.figure(figsize=(10, 6))
plt.plot(tiempo, temperatura, label='Temperatura del agua')
plt.axhline(y=temperatura_objetivo_C, color='r', linestyle='--', label='Temperatura objetivo')
plt.xlabel('Tiempo (segundos)')
plt.ylabel('Temperatura (°C)')
plt.title('Simulación de calentador de agua')
plt.legend()
plt.grid(True)
plt.show()
