import numpy as np
import matplotlib.pyplot as plt

class CalentadorH2O:
    def __init__(self):
        self.parametros()

    def parametros(self):
        self.radio = 0.05  # Radio del calentador en metros.
        self.altura = 0.14  # Altura del calentador en metros.
        self.espesor = [0.01, 0.005, 0.05]  # Define los espesores de las paredes del calentador en metros.
        self.voltaje_V = 110  # Voltaje suministrado en V
        self.resistencia_Ohm = 108  # Resistencia eléctrica en Ohm
        self.qesph2o = 4186  # Capacidad térmica del agua en J/kg°C
        self.tiempo_max = 2500  # Tiempo máximo de simulación en segundos
        self.ti = 10  # Temperatura inicial.
        self.te = 25  # Temperatura externa.
        self.k = 1  # Conductividad térmica de la ceramica en W/m°C 

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
        election = int(input("Ingresar 1 para cálculo sin pérdidas \nIngresar 2 para generar y graficar curvas de familia\n"))
        if election == 1:
            g.sin_perdidas()
            stop = True
        elif election == 2:
            g.generar_y_graficar_curvas()
            stop = True

