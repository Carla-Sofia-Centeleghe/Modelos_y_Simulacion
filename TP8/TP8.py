import pygame
import random
import numpy as np
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simulación de Boxes de Atención")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
VIOLET = (238, 130, 238)
BLUE = (0, 0, 255)

font = pygame.font.SysFont(None, 24)

probabilidad_ingreso = 1 / 144
horas_apertura = 4
segundos_apertura = horas_apertura * 3600

clientes_en_cola = []
clientes_atendidos = []
clientes_abandonados = []
boxes = [None] * 5
boxes_active = 5

tiempos_espera = []
tiempos_atencion = []

resultados_simulacion = {}

class Cliente:
    def __init__(self, tiempo_llegada):
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_atendido = None

def atender_clientes(tiempo_actual):
    for i in range(len(boxes)):
        if boxes[i] is None and clientes_en_cola:
            cliente = clientes_en_cola.pop(0)
            tiempo_atencion = max(1, np.random.normal(600, 300))
            cliente.tiempo_atendido = tiempo_atencion
            clientes_atendidos.append(cliente)
            tiempos_atencion.append(tiempo_atencion)
            boxes[i] = (cliente, tiempo_actual + tiempo_atencion)

def generar_clientes(tiempo_actual):
    if tiempo_actual < segundos_apertura:
        tiempo_llegada = tiempo_actual + max(1, int(np.random.normal(36000, 7200)))
        cliente = Cliente(tiempo_llegada)
        clientes_en_cola.append(cliente)

def draw_text(text, pos):
    screen.blit(font.render(text, True, BLACK), pos)

def draw_button(text, pos, size):
    rect = pygame.Rect(pos, size)
    pygame.draw.rect(screen, BLUE, rect)
    draw_text(text, (pos[0] + 10, pos[1] + 10))
    return rect

def ejecutar_simulacion():
    global clientes_en_cola, clientes_atendidos, clientes_abandonados, boxes, tiempos_espera, tiempos_atencion
    tiempo_actual = 0
    incremento_tiempo = 15

    clientes_en_cola = []
    clientes_atendidos = []
    clientes_abandonados = []
    boxes = [None] * boxes_active
    tiempos_espera = []
    tiempos_atencion = []
    tiempo_min_espera_sala = float('inf')
    tiempo_max_espera_sala = 0


    while tiempo_actual < segundos_apertura + 1800:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        generar_clientes(tiempo_actual)

        atender_clientes(tiempo_actual)
        for i, cliente in enumerate(clientes_en_cola):
            tiempo_espera = tiempo_actual - cliente.tiempo_llegada
            tiempo_min_espera_sala = min(tiempo_min_espera_sala, tiempo_espera)
            tiempo_max_espera_sala = max(tiempo_max_espera_sala, tiempo_espera)

        for i in range(len(boxes)):
            if boxes[i] is not None:
                cliente, tiempo_fin_atencion = boxes[i]
                if tiempo_actual >= tiempo_fin_atencion:
                    boxes[i] = None

        clientes_en_cola = [cliente for cliente in clientes_en_cola if tiempo_actual - cliente.tiempo_llegada < 1800]
        clientes_abandonados = [cliente for cliente in clientes_en_cola if tiempo_actual - cliente.tiempo_llegada >= 1800]

        tiempo_actual += incremento_tiempo

        pygame.time.wait(50)

        screen.fill(WHITE)

        draw_text(f"Clientes ingresados: {len(clientes_en_cola) + len(clientes_atendidos) + len(clientes_abandonados)}", (20, 20))
        draw_text(f"Clientes atendidos: {len(clientes_atendidos)}", (20, 50))
        #draw_text(f"Clientes abandonados: {len(clientes_abandonados)}", (20, 80))

        if tiempos_atencion:
            draw_text(f"Tiempo mínimo de atención en box: {min(tiempos_atencion):.2f} s", (20, 110))
            draw_text(f"Tiempo máximo de atención en box: {max(tiempos_atencion):.2f} s", (20, 140))

        if tiempos_espera:
            draw_text(f"Tiempo mínimo de espera en salón: {min(tiempos_espera):.2f} s", (20, 170))
            draw_text(f"Tiempo máximo de espera en salón: {max(tiempos_espera):.2f} s", (20, 200))

        costo_operacion = len(boxes) * 1000 + len(clientes_abandonados) * 10000
        draw_text(f"Costo de la operación: ${costo_operacion}", (20, 230))

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

        for i, cliente in enumerate(clientes_en_cola):
            pygame.draw.circle(screen, VIOLET, (50, 400 + i * 30), 10)

        pygame.display.flip()

        pygame.time.wait(1)

    resultados_simulacion['clientes_ingresados'] = len(clientes_en_cola) + len(clientes_atendidos) + len(clientes_abandonados)
    resultados_simulacion['clientes_atendidos'] = len(clientes_atendidos)
    resultados_simulacion['clientes_abandonados'] = len(clientes_abandonados)
    resultados_simulacion['tiempo_min_atencion'] = min(tiempos_atencion)
    resultados_simulacion['tiempo_max_atencion'] = max(tiempos_atencion) 
    resultados_simulacion['costo_operacion'] = costo_operacion

botones_boxes = [] 
print("Seleccione la cantidad de boxes:")
for i in range(1, 11):
    botones_boxes.append(draw_button(str(i), (200 + (i-1) * 60, 500), (50, 50)))

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

    pygame.display.flip()
