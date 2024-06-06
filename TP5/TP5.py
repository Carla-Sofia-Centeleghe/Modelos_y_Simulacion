import numpy as np
import matplotlib.pyplot as plt

class CalentadorH2O:
    def __init__(self):
        self.parametros()

    def parametros(self):
        self.radio = 0.05  # Define el radio del calentador en metros.
        self.altura = 0.14  # Define la altura del calentador en metros.
        self.espesor = [0.01, 0.005, 0.05]  # Define los espesores de las paredes del calentador en metros.
        self.qent = 108  # Define la cantidad de energía entregada al sistema por unidad de tiempo en vatios.
        self.qesph2o = 4.186  # Define la cantidad de calor específico del agua en vatios por gramo por grado Celsius.
        self.tiempo_max = 8  # Define el tiempo máximo de simulación en segundos.
        self.ti = 10  # Temperatura inicial.
        self.te = 10  # Temperatura externa.
        self.k = 0.02  # Define la conductividad térmica del material en vatios por metro por grado Celsius.

    def resistencia_uniforme(self):
        return np.random.uniform(1, 10, 5)

    def temperatura_normal(self):
        return np.random.normal(10, 5, 5)

    def temperatura_ambiente_uniforme(self):
        return np.random.uniform(-20, 50, 8)

    def tension_alimentacion_normal(self, option=1):
        if option == 1:
            return np.random.normal(12, 4, 5)
        elif option == 2:
            return np.random.normal(220, 40, 5)

    def curva_familia(self, x, parametros):
        a, b, c = parametros
        return a * np.exp(b * x) + c  

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

    def grafico_tiempo_temp(self, tiempos1, temperaturas1):
        plt.plot(tiempos1, temperaturas1, label="Espesor = 0.01")
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Gráfico de Temperatura vs. Tiempo (Con Pérdidas)')
        plt.legend()
        plt.show()

    def grafico_tiempo_temp_sin_perdidas(self, tiempos, temperaturas):
        plt.plot(tiempos, temperaturas)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Gráfico de Temperatura vs. Tiempo (Sin Pérdidas)')
        plt.show()

    def generar_y_graficar_curvas(self):
        resistencias = self.resistencia_uniforme()
        temperaturas_agua = self.temperatura_normal()
        temperaturas_ambiente = self.temperatura_ambiente_uniforme()
        tensiones_alimentacion_1 = self.tension_alimentacion_normal(option=1)
        tensiones_alimentacion_2 = self.tension_alimentacion_normal(option=2)

        x = np.linspace(0, 10, 100)

        plt.figure(figsize=(10, 8))

        # Curvas de resistencia
        plt.subplot(321)
        for resistencia in resistencias:
            parametros = [resistencia, 0.1, 0.5]
            plt.plot(x, self.curva_familia(x, parametros))
        plt.title('Curvas de Familia - Resistencias')

        # Curvas de temperatura del agua
        plt.subplot(322)
        for temperatura in temperaturas_agua:
            parametros = [1, 0.1, temperatura]
            plt.plot(x, self.curva_familia(x, parametros))
        plt.title('Curvas de Familia - Temperatura del Agua')

        # Curvas de temperatura del ambiente
        plt.subplot(323)
        for temperatura in temperaturas_ambiente:
            parametros = [1, 0.1, temperatura]
            plt.plot(x, self.curva_familia(x, parametros))
        plt.title('Curvas de Familia - Temperatura del Ambiente')

        # Curvas de tensión de alimentación (Media 12)
        plt.subplot(324)
        for tension in tensiones_alimentacion_1:
            parametros = [tension, 0.1, 0.5]
            plt.plot(x, self.curva_familia(x, parametros))
        plt.title('Curvas de Familia - Tensión de Alimentación (Media 12)')

        # Curvas de tensión de alimentación (Media 220)
        plt.subplot(325)
        for tension in tensiones_alimentacion_2:
            parametros = [tension, 0.1, 0.5]
            plt.plot(x, self.curva_familia(x, parametros))
        plt.title('Curvas de Familia - Tensión de Alimentación (Media 220)')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    g = CalentadorH2O()
    stop = False
    while not stop:
        election = int(input("Ingresar 1 para cálculo sin pérdidas \nIngresar 2 para cálculo con pérdidas\nIngresar 3 para generar y graficar curvas de familia\n"))
        if election == 1:
            g.sin_perdidas()
            stop = True
        elif election == 2:
            g.con_perdidas()
            stop = True
        elif election == 3:
            g.generar_y_graficar_curvas()
            stop = True

