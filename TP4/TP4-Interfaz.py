import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

class CalentadorH2O:
    def __init__(self):
        self.parametros()
        self.root = tk.Tk()
        self.root.title("Graficador de Pérdida de Calor")
        self.create_widgets()

    def parametros(self):
        self.radio = 0.05 # Define el radio del calentador en metros.
        self.altura = 0.14 # Define la altura del calentador en metros.
        self.espesor = [0.01, 0.005, 0.05] # Define los espesores de las paredes del calentador en metros.
        self.qent = 108 # Define la cantidad de energía entregada al sistema por unidad de tiempo en vatios.
        self.qesph2o = 4.186 # Define la cantidad de calor específico del agua en vatios por gramo por grado Celsius.
        self.tiempo_max = 8 # Define el tiempo máximo de simulación en segundos.
        self.ti = 10  # Temperatura inicial
        self.te = 10  # Temperatura externa
        self.k =  0.0225 # Define la conductividad térmica del material en vatios por metro por grado Celsius.

    def sin_perdidas(self):
        temperaturas = []
        tiempos = []

        for tiempo in range(self.tiempo_max):
            tf = self.ti + (self.qent / self.qesph2o)
            temperaturas.append(tf)
            tiempos.append(tiempo)
            self.ti = tf

        self.grafico_tiempo_temp_sin_perdidas(tiempos, temperaturas)
    
    def con_perdidas(self):
        area = 2 * 3.1416 * self.altura * self.radio + 2 * 3.1416 * self.radio**2
        temperaturas1, tiempos1, temperaturas2, tiempos2 = [], [], [], []

        for i in range(3):
            temperaturas, tiempos = [], []
            print("Espesor:", self.espesor[i])
            for tiempo in range(self.tiempo_max):
                perdida_calor = (self.k * area * (self.ti - self.te)) / self.espesor[i]
                temperaturas.append(self.ti)
                tiempos.append(tiempo)
                self.ti += (self.qent - perdida_calor) / self.qesph2o

            self.ti = 25
            if i == 0:
                temperaturas1, tiempos1 = temperaturas, tiempos
            elif i == 1:
                temperaturas2, tiempos2 = temperaturas, tiempos

        self.grafico_tiempo_temp(tiempos, temperaturas, tiempos2, temperaturas2, tiempos1, temperaturas1)

    def grafico_tiempo_temp(self, tiempos, temperaturas, tiempos2, temperaturas2, tiempos1, temperaturas1):
        plt.plot(tiempos1, temperaturas1, label="Espesor = 0.01")
        #plt.plot(tiempos2, temperaturas2, label="Espesor = 0.005")                 #Desocmientar para ver el gráfico con el espesor de 0.005
        #plt.plot(tiempos, temperaturas, label="Espesor = 0.05")                    #Desocmientar para ver el gráfico con el espesor de 0.05
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Gráfico de Temperatura vs. Tiempo (Con Pérdidas))')
        plt.legend()
        plt.show()

    def grafico_tiempo_temp_sin_perdidas(self, tiempos, temperaturas):
        plt.plot(tiempos, temperaturas)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Gráfico de Temperatura vs. Tiempo (Sin Pérdidas)')
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

