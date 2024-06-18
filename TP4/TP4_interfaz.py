import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox


class CalentadorH2O:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Graficador de Pérdida de Calor")
        self.create_widgets()

        self.radio = 0.05  # Radio del calentador en metros
        self.altura = 0.14  # Altura del calentador en metros
        self.espesores = [0.01, 0.005, 0.05]  # Definición de los espesores de las paredes del calentador en metros
        self.temperatura_inicial_C = 10  # Temperatura inicial del agua en °C
        self.temperatura_objetivo_C = 75  # Temperatura objetivo del agua en °C
        self.temperatura_externa_C = 25  # Temperatura externa en °C
        self.delta_t = 1  # Paso del tiempo en segundos
        self.tiempo_max = 2500  # Tiempo máximo de simulación en segundos
        self.voltaje_V = 110  # Voltaje suministrado en V
        self.resistencia_Ohm = 108  # Resistencia eléctrica en Ohm
        self.qesph2o = 4186  # Capacidad térmica del agua en J/kg°C
        self.k = 1  # Conductividad térmica de la ceramica en W/m.K
        self.area = 2 * np.pi * self.radio * self.altura + 2 * np.pi * self.radio**2  # Área total del cilindro
        self.qent = self.calcular_potencia()  # Cálculo de la potencia utilizando la Ley de Ohm

    def calcular_potencia(self):
        # Cálculo de la potencia entregada al sistema por unidad de tiempo
        q_total = (self.voltaje_V**2) / self.resistencia_Ohm
        return q_total

    def sin_perdidas(self):
        temperaturas = []
        tiempos = []

        temperatura_inicial = self.temperatura_inicial_C  # Restablecer la temperatura inicial

        for tiempo in range(self.tiempo_max):
            tf = temperatura_inicial + (self.calcular_potencia() / self.qesph2o)
            temperaturas.append(tf)
            tiempos.append(tiempo)
            temperatura_inicial = tf

        self.grafico_tiempo_temp_sin_perdidas(tiempos, temperaturas)

    def con_perdidas(self):
        temperaturas_por_espesor = []
        tiempos_por_espesor = []

        for espesor in self.espesores:
            temperaturas, tiempos = [], []
            temperatura_inicial = self.temperatura_inicial_C  # Restablecer la temperatura inicial

            for tiempo in range(self.tiempo_max):
                q_total = self.calcular_potencia()
                perdida_calor_paredes = (self.k * self.area * (temperatura_inicial - self.temperatura_externa_C)) / espesor
                q_net = q_total - perdida_calor_paredes
                temperatura_inicial += q_net / self.qesph2o
                temperaturas.append(temperatura_inicial)
                tiempos.append(tiempo)

            temperaturas_por_espesor.append(temperaturas)
            tiempos_por_espesor.append(tiempos)

        self.grafico_tiempo_temp(tiempos_por_espesor, temperaturas_por_espesor)

    def grafico_tiempo_temp(self, tiempos_por_espesor, temperaturas_por_espesor):
        plt.figure(figsize=(10, 6))
        
        for tiempos, temperaturas, espesor in zip(tiempos_por_espesor, temperaturas_por_espesor, self.espesores):
            label = f"Espesor = {espesor} m"
            plt.plot(tiempos, temperaturas, label=label)
        
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Gráfico de Temperatura vs. Tiempo con Pérdidas')
        plt.legend()
        plt.grid(True)
        plt.show()

    def grafico_tiempo_temp_sin_perdidas(self, tiempos, temperaturas):
        plt.figure(figsize=(10, 6))
        plt.plot(tiempos, temperaturas, label='Temperatura del agua')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Gráfico de Temperatura vs. Tiempo (Sin Pérdidas)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def create_widgets(self):
            self.sin_perdidas_button = tk.Button(self.root, text="Sin Pérdida de Calor",bg="blue", fg="white", command=self.sin_perdidas)
            self.sin_perdidas_button.pack(side="top")

            self.con_perdidas_button = tk.Button(self.root, text="Con Pérdida de Calor",bg="green", fg="white", command=self.con_perdidas)
            self.con_perdidas_button.pack(side="top")

            self.salir_button = tk.Button(self.root, text="Salir",bg="red", fg="white", command=self.root.quit)
            self.salir_button.pack(side="top")

if __name__ == "__main__":
    app = CalentadorH2O()
    app.root.mainloop()