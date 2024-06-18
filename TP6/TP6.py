import matplotlib.pyplot as plt
import numpy as np

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
        self.ti = 10  # Temperatura interna inicial
        self.te = 25  # Temperatura externa inicial
        self.k = 1  # Conductividad térmica de la ceramica en W/m°C 
        self.qent = (self.voltaje_V ** 2) / self.resistencia_Ohm  # Potencia entregada al sistema por unidad de tiempo

    def sin_perdidas(self):
        temperaturas = []
        tiempos = []

        for tiempo in range(self.tiempo_max):
            # Simulación del fenómeno estocástico
            if np.random.random() < 1/300:  # Probabilidad de 1/300 de ocurrencia del fenómeno
                descenso_grados = np.random.uniform(0, 50)  # Grados de descenso aleatorio (hasta 50 grados)
                duracion_descenso = np.random.randint(1, 11)  # Duración del descenso en ticks de tiempo (hasta 10 ticks)
                for _ in range(duracion_descenso):
                    self.ti -= descenso_grados / duracion_descenso  # Aplicar el descenso de temperatura
                    if tiempo < self.tiempo_max:
                        temperaturas.append(self.ti)
                        tiempos.append(tiempo)
                        tiempo += 1

            # Actualización de la temperatura sin pérdidas
            tf = self.ti + (self.qent / self.qesph2o)
            temperaturas.append(tf)
            tiempos.append(tiempo)
            self.ti = tf

        self.grafico_tiempo_temp_sin_perdidas(tiempos, temperaturas)

    def con_perdidas(self):
        area = 2 * 3.1416 * self.altura * self.radio + 2 * 3.1416 * self.radio ** 2
        todas_temperaturas = []
        todas_tiempos = []

        for i in range(3):
            temperaturas, tiempos = [], []
            print("Espesor:", self.espesor[i])
            for tiempo in range(self.tiempo_max):
                # Simulación del fenómeno estocástico
                if np.random.random() < 1/300:  # Probabilidad de 1/300 de ocurrencia del fenómeno
                    descenso_grados = np.random.uniform(0, 50)  # Grados de descenso aleatorio (hasta 50 grados)
                    duracion_descenso = np.random.randint(1, 11)  # Duración del descenso en ticks de tiempo (hasta 10 ticks)
                    for _ in range(duracion_descenso):
                        self.ti -= descenso_grados / duracion_descenso  # Aplicar el descenso de temperatura
                        if tiempo < self.tiempo_max:
                            temperaturas.append(self.ti)
                            tiempos.append(tiempo)
                            tiempo += 1

                # Cálculo de la pérdida de calor
                perdida_calor = (self.k * area * (self.ti - self.te)) / self.espesor[i]
                temperaturas.append(self.ti)
                tiempos.append(tiempo)
                self.ti += (self.qent - perdida_calor) / self.qesph2o

            todas_temperaturas.append(temperaturas)
            todas_tiempos.append(tiempos)
            self.ti = 10  # Reiniciar la temperatura inicial para el siguiente espesor

        self.grafico_tiempo_temp(todas_tiempos, todas_temperaturas)

    def grafico_tiempo_temp(self, todas_tiempos, todas_temperaturas):
        for i, (tiempos, temperaturas) in enumerate(zip(todas_tiempos, todas_temperaturas)):
            plt.plot(tiempos, temperaturas, label=f"Espesor = {self.espesor[i]}")
        
        plt.xlabel('Tiempo (ticks)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Gráfico de Temperatura vs. Tiempo (Con Pérdidas)')
        plt.legend()
        plt.show()

    def grafico_tiempo_temp_sin_perdidas(self, tiempos, temperaturas):
        plt.plot(tiempos, temperaturas)
        plt.xlabel('Tiempo (ticks)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Gráfico de Temperatura vs. Tiempo (Sin Pérdidas)')
        plt.show()

if __name__ == "__main__":
    g = CalentadorH2O()
    stop = False
    while not stop:
        election = int(input("Ingresar 1 para cálculo sin pérdidas \nIngresar 2 para cálculo con pérdidas\n"))
        if election == 1:
            g.sin_perdidas()
            stop = True
        elif election == 2:
            g.con_perdidas()
            stop = True
