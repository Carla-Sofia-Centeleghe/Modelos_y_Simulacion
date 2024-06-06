import pygame
import random
import numpy as np
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación de Cajas de Atención")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VIOLETA = (238, 130, 238)

# Fuente
fuente = pygame.font.SysFont(None, 24)

# Parámetros de simulación
probabilidad_ingreso = 1 / 144
horas_apertura = 4  # De 8 a 12 horas, son 4 horas
segundos_apertura = horas_apertura * 3600
incremento_tiempo = 15  # Cada iteración representa 15 segundos

# Variables para almacenar datos de simulación
clientes_en_cola = []
clientes_atendidos = []
clientes_abandonados = []
cajas = []
boxes_active = 5  # Cantidad inicial de cajas activas

# Estadísticas
tiempos_espera = []
tiempos_atencion = []

# Resultados de simulaciones
resultados_simulacion = {}

# Clase Cliente
class Cliente:
    def __init__(self, tiempo_llegada):
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_atendido = None

# Función para manejar la lógica de atención
def atender_clientes(tiempo_actual):
    global cajas
    for i in range(len(cajas)):
        if cajas[i] is None and clientes_en_cola:
            cliente = clientes_en_cola.pop(0)
            tiempo_atencion = max(1, int(np.random.normal(600, 300)))  # Normal(10min=600s, std=5min=300s)
            cliente.tiempo_atendido = tiempo_atencion
            clientes_atendidos.append(cliente)
            tiempos_atencion.append(tiempo_atencion)
            cajas[i] = (cliente, tiempo_actual + tiempo_atencion)

# Función para dibujar texto en pantalla
def dibujar_texto(texto, pos):
    pantalla.blit(fuente.render(texto, True, NEGRO), pos)

# Función para dibujar botones
def dibujar_boton(texto, pos, tam):
    rect = pygame.Rect(pos, tam)
    pygame.draw.rect(pantalla, AZUL, rect)
    dibujar_texto(texto, (pos[0] + 10, pos[1] + 10))
    return rect

# Función para ejecutar la simulación
def ejecutar_simulacion():
    global clientes_en_cola, clientes_atendidos, clientes_abandonados, cajas, tiempos_espera, tiempos_atencion
    tiempo_actual = 0

    # Inicializar listas y variables
    clientes_en_cola = []
    clientes_atendidos = []
    clientes_abandonados = []
    cajas = [None] * boxes_active
    tiempos_espera = []
    tiempos_atencion = []

    while tiempo_actual < segundos_apertura + 1800:  # 30 minutos adicionales para los clientes en cola
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Ingreso de nuevos clientes
        if tiempo_actual < segundos_apertura:
            if random.random() < probabilidad_ingreso:
                cliente = Cliente(tiempo_actual)
                clientes_en_cola.append(cliente)

        # Atención de clientes en cajas
        atender_clientes(tiempo_actual)

        # Actualización de estado de las cajas
        for i in range(len(cajas)):
            if cajas[i] is not None:
                cliente, tiempo_fin_atencion = cajas[i]
                if tiempo_actual >= tiempo_fin_atencion:
                    cajas[i] = None

        # Abandono de clientes después de 30 minutos
        clientes_abandonados.extend([cliente for cliente in clientes_en_cola if tiempo_actual - cliente.tiempo_llegada >= 1800])
        clientes_en_cola = [cliente for cliente in clientes_en_cola if tiempo_actual - cliente.tiempo_llegada < 1800]

        # Actualizar tiempo
        tiempo_actual += incremento_tiempo

        # Dibujar fondo
        pantalla.fill(BLANCO)

        # Mostrar estadísticas
        dibujar_texto(f"Clientes ingresados: {len(clientes_en_cola) + len(clientes_atendidos) + len(clientes_abandonados)}", (20, 20))
        dibujar_texto(f"Clientes atendidos: {len(clientes_atendidos)}", (20, 50))
        dibujar_texto(f"Clientes abandonados: {len(clientes_abandonados)}", (20, 80))

        if tiempos_atencion:
            dibujar_texto(f"Tiempo mínimo de atención en box: {min(tiempos_atencion):.2f} s", (20, 110))
            dibujar_texto(f"Tiempo máximo de atención en box: {max(tiempos_atencion):.2f} s", (20, 140))

        if tiempos_espera:
            dibujar_texto(f"Tiempo mínimo de espera en salón: {min(tiempos_espera):.2f} s", (20, 170))
            dibujar_texto(f"Tiempo máximo de espera en salón: {max(tiempos_espera):.2f} s", (20, 200))

        # Costo de operación
        costo_operacion = len(cajas) * 1000 + len(clientes_abandonados) * 10000
        dibujar_texto(f"Costo de la operación: ${costo_operacion}", (20, 230))

        # Dibujar cajas
        ancho_cuadro = 60
        altura_cuadro = 40
        margen_cuadro = 20
        for i in range(len(cajas)):
            cuadro_x = margen_cuadro + (ancho_cuadro + margen_cuadro) * i
            cuadro_y = 300
            color = VERDE if cajas[i] is None else ROJO
            pygame.draw.rect(pantalla, color, (cuadro_x, cuadro_y, ancho_cuadro, altura_cuadro))
            dibujar_texto(f"Box {i + 1}", (cuadro_x + 10, cuadro_y + 10))

        # Dibujar clientes en cola
        for i, cliente in enumerate(clientes_en_cola):
            pygame.draw.circle(pantalla, VIOLETA, (50, 400 + i * 30), 10)

        # Actualizar pantalla
        pygame.display.flip()

        # Esperar un poco para visualizar en la pantalla
        pygame.time.wait(50)

    # Guardar resultados de la simulación
    resultados_simulacion['clientes_ingresados'] = len(clientes_en_cola) + len(clientes_atendidos) + len(clientes_abandonados)
    resultados_simulacion['clientes_atendidos'] = len(clientes_atendidos)
    resultados_simulacion['clientes_abandonados'] = len(clientes_abandonados)
    resultados_simulacion['costo_operacion'] = costo_operacion

# Botones para seleccionar la cantidad de cajas
botones_boxes = []
print("Seleccione la cantidad de cajas:")
for i in range(1, 11):  # Rango de 1 a 10 cajas
    botones_boxes.append(dibujar_boton(str(i), (200 + (i - 1) * 60, 500), (50, 50)))

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for i, boton in enumerate(botones_boxes):
                if boton.collidepoint(evento.pos):
                    boxes_active = i + 1
                    ejecutar_simulacion()

    # Actualizar pantalla
    pygame.display.flip()
