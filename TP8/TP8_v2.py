import pygame
import random
import numpy as np
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simulación de Boxes de Atención")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
VIOLET = (238, 130, 238)
BLUE = (0, 0, 255)

# Fuente
font = pygame.font.SysFont(None, 24)

# Parámetros de simulación
media = 10  # Media de la distribución normal (10 AM)
desviacion_estandar = 2  # Desviación estándar de la distribución normal (2 horas)
clientes_por_manana = 100  # Expectativa matemática de clientes durante la mañana
horas_apertura = 4  # De 8 a 12 horas, son 4 horas
segundos_apertura = horas_apertura * 3600

# Listas para almacenar clientes
clientes_en_cola = []
clientes_atendidos = []
clientes_abandonados = []
boxes = [None] * 5  # Inicialmente 5 boxes activos
boxes_active = 5  # Cantidad de boxes activos

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

# Función para generar tiempos de llegada con distribución normal
def generar_tiempos_llegada(clientes_totales):
    tiempos_llegada = []
    for _ in range(clientes_totales):
        while True:
            tiempo = np.random.normal(loc=media, scale=desviacion_estandar)
            if 8 <= tiempo <= 12:
                # Convertir el tiempo a segundos desde las 8 AM
                tiempo_llegada = (tiempo - 8) * 3600
                tiempos_llegada.append(tiempo_llegada)
                break
    return sorted(tiempos_llegada)

# Función para manejar la lógica de atención
def atender_clientes(tiempo_actual):
    for i in range(len(boxes)):
        if boxes[i] is None and clientes_en_cola:
            cliente = clientes_en_cola.pop(0)
            tiempo_atencion = max(1, np.random.normal(600, 7200))  # Normal(10min=600s, std=2h=7200s)
            cliente.tiempo_atendido = tiempo_atencion
            clientes_atendidos.append(cliente)
            tiempos_atencion.append(tiempo_atencion)
            boxes[i] = (cliente, tiempo_actual + tiempo_atencion)

# Función para dibujar texto en pantalla
def draw_text(text, pos):
    screen.blit(font.render(text, True, BLACK), pos)

# Función para dibujar botones
def draw_button(text, pos, size):
    rect = pygame.Rect(pos, size)
    pygame.draw.rect(screen, BLUE, rect)
    draw_text(text, (pos[0] + 10, pos[1] + 10))
    return rect

# Función para ejecutar la simulación
def ejecutar_simulacion():
    global clientes_en_cola, clientes_atendidos, clientes_abandonados, boxes, tiempos_espera, tiempos_atencion
    tiempo_actual = 0
    incremento_tiempo = 15  # Cambiar a 15 para que cada iteración represente 15 segundos

    clientes_en_cola = []
    clientes_atendidos = []
    clientes_abandonados = []
    boxes = [None] * boxes_active
    tiempos_espera = []
    tiempos_atencion = []

    # Generar tiempos de llegada de los clientes
    tiempos_llegada = generar_tiempos_llegada(clientes_por_manana)

    while tiempo_actual < segundos_apertura + 1800:  # 30 minutos adicionales para los clientes en cola
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Ingreso de nuevos clientes
        while tiempos_llegada and tiempo_actual >= tiempos_llegada[0]:
            cliente = Cliente(tiempo_actual)
            clientes_en_cola.append(cliente)
            tiempos_llegada.pop(0)

        # Atención de clientes en boxes
        atender_clientes(tiempo_actual)

        # Actualización de estado de los boxes
        for i in range(len(boxes)):
            if boxes[i] is not None:
                cliente, tiempo_fin_atencion = boxes[i]
                if tiempo_actual >= tiempo_fin_atencion:
                    boxes[i] = None

        # Abandono de clientes después de 30 minutos
        clientes_en_cola = [cliente for cliente in clientes_en_cola if tiempo_actual - cliente.tiempo_llegada < 1800]
        clientes_abandonados = [cliente for cliente in clientes_en_cola if tiempo_actual - cliente.tiempo_llegada >= 1800]

        # Actualizar tiempo
        tiempo_actual += incremento_tiempo

        # Esperar un poco para visualizar en la pantalla
        pygame.time.wait(50)

        # Dibujar fondo
        screen.fill(WHITE)

        # Mostrar estadísticas
        draw_text(f"Clientes ingresados: {len(clientes_en_cola) + len(clientes_atendidos) + len(clientes_abandonados)}", (20, 20))
        draw_text(f"Clientes atendidos: {len(clientes_atendidos)}", (20, 50))
        draw_text(f"Clientes abandonados: {len(clientes_abandonados)}", (20, 80))

        if tiempos_atencion:
            draw_text(f"Tiempo mínimo de atención en box: {min(tiempos_atencion):.2f} s", (20, 110))
            draw_text(f"Tiempo máximo de atención en box: {max(tiempos_atencion):.2f} s", (20, 140))

        if tiempos_espera:
            draw_text(f"Tiempo mínimo de espera en salón: {min(tiempos_espera):.2f} s", (20, 170))
            draw_text(f"Tiempo máximo de espera en salón: {max(tiempos_espera):.2f} s", (20, 200))

        # Costos
        costo_operacion = len(boxes) * 1000 + len(clientes_abandonados) * 10000
        draw_text(f"Costo de la operación: ${costo_operacion}", (20, 230))

        # Dibujar boxes
        box_width = 60
        box_height = 40
        box_margin = 20
        for i in range(len(boxes)):
            box_x = box_margin + (box_width + box_margin) * i
            box_y = 300
            if boxes[i] is None:
                color = GREEN
            else:
                color = RED
            pygame.draw.rect(screen, color, (box_x, box_y, box_width, box_height))
            draw_text(f"Box {i + 1}", (box_x + 10, box_y + 10))

        # Dibujar clientes en cola
        for i, cliente in enumerate(clientes_en_cola):
            pygame.draw.circle(screen, VIOLET, (50, 400 + i * 30), 10)

        # Actualizar pantalla
        pygame.display.flip()

        # Esperar 1 segundo en cada iteración para que sea visible en la pantalla
        pygame.time.wait(1)

    # Guardar resultados de la simulación
    resultados_simulacion['clientes_ingresados'] = len(clientes_en_cola) + len(clientes_atendidos) + len(clientes_abandonados)
    resultados_simulacion['clientes_atendidos'] = len(clientes_atendidos)
    resultados_simulacion['clientes_abandonados'] = len(clientes_abandonados)
    resultados_simulacion['costo_operacion'] = costo_operacion

# Botones para seleccionar la cantidad de boxes
botones_boxes = []
print("Seleccione la cantidad de boxes:")
for i in range(1, 11):  # Rango de 1 a 10 boxes
    botones_boxes.append(draw_button(str(i), (200 + (i-1) * 60, 500), (50, 50)))

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, boton in enumerate(botones_boxes):
                if boton.collidepoint(event.pos):
                    boxes_active = i + 1
                    ejecutar_simulacion()

    # Actualizar pantalla
    pygame.display.flip()
