import pygame
import random
import numpy as np
import sys
import matplotlib.pyplot as plt
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode((800, 600))  # Pantalla dividida para dos simulaciones
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

resultados_simulacion_1 = {}
resultados_simulacion_2 = {}

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

def draw_text(text, pos):
    screen.blit(font.render(text, True, BLACK), pos)

def draw_button(text, pos, size):
    rect = pygame.Rect(pos, size)
    pygame.draw.rect(screen, BLUE, rect)
    draw_text(text, (pos[0] + 10, pos[1] + 10))
    return rect

def ejecutar_simulacion(tiempo_simulacion, resultados_simulacion, side):
    global clientes_en_cola, clientes_atendidos, clientes_abandonados, boxes, tiempos_espera, tiempos_atencion
    tiempo_actual = 0
    incremento_tiempo = 15

    clientes_en_cola = []
    clientes_atendidos = []
    clientes_abandonados = []
    boxes = [None] * boxes_active
    tiempos_espera = []
    tiempos_atencion = []

    while tiempo_actual < tiempo_simulacion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Ingreso de nuevos clientes
        for _ in range(incremento_tiempo):
            if tiempo_actual < segundos_apertura:
                if random.random() < probabilidad_ingreso:
                    cliente = Cliente(tiempo_actual)
                    clientes_en_cola.append(cliente)
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
        if side == 1:
            draw_text(f"Simulación 1", (20, 20))
        else:
            draw_text(f"Simulación 2", (20, 20))

        draw_text(f"Clientes ingresados: {len(clientes_en_cola) + len(clientes_atendidos) + len(clientes_abandonados)}", (20, 50))
        draw_text(f"Clientes atendidos: {len(clientes_atendidos)}", (20, 80))
        draw_text(f"Clientes abandonados: {len(clientes_abandonados)}", (20, 110))

        if tiempos_atencion:
            draw_text(f"Tiempo mínimo de atención en box: {min(tiempos_atencion):.2f} s", (20, 140))
            draw_text(f"Tiempo máximo de atención en box: {max(tiempos_atencion):.2f} s", (20, 170))

        if tiempos_espera:
            draw_text(f"Tiempo mínimo de espera en salón: {min(tiempos_espera):.2f} s", (20, 200))
            draw_text(f"Tiempo máximo de espera en salón: {max(tiempos_espera):.2f} s", (20, 230))
        
        # Costos
        costo_operacion = len(boxes) * 1000 + len(clientes_abandonados) * 10000
        draw_text(f"Costo de la operación: ${costo_operacion}", (20, 260))

        # Dibujar boxes
        for i in range(len(boxes)):
            box_x = 100 + (150 * i)
            box_y = 350
            if boxes[i] is None:
                color = GREEN
            else:
                color = RED
            pygame.draw.rect(screen, color, (box_x, box_y, 150, 40))
            draw_text(f"Box {i + 1}", (box_x + 10, box_y + 10))
        # Dibujar clientes en cola
        for i, cliente in enumerate(clientes_en_cola):
            pygame.draw.circle(screen, VIOLET, (50, 450 + i * 30), 10)
        
        # Actualizar pantalla
        pygame.display.flip()
        # Esperar 1 segundo en cada iteración para que sea visible en la pantalla
        pygame.time.wait(1)

    # Guardar los resultados de la simulación
    if side == 1:
        resultados_simulacion_1['clientes_ingresados'] = len(clientes_en_cola) + len(clientes_atendidos) + len(clientes_abandonados)
        resultados_simulacion_1['clientes_atendidos'] = len(clientes_atendidos)
        resultados_simulacion_1['clientes_abandonados'] = len(clientes_abandonados)
        resultados_simulacion_1['costo_operacion'] = costo_operacion
    else:
        resultados_simulacion_2['clientes_ingresados'] = len(clientes_en_cola) + len(clientes_atendidos) + len(clientes_abandonados)
        resultados_simulacion_2['clientes_atendidos'] = len(clientes_atendidos)
        resultados_simulacion_2['clientes_abandonados'] = len(clientes_abandonados)
        resultados_simulacion_2['costo_operacion'] = costo_operacion

    # Guardar los resultados para análisis posterior    
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    np.save(f'resultados_{side}_{"_".join(map(str, resultados_simulacion_1.values()))}_{now}.npy', resultados_simulacion_1)
    np.save(f'resultados_{side}_{"_".join(map(str, resultados_simulacion_2.values()))}_{now}.npy', resultados_simulacion_2)

# Botones para seleccionar la cantidad de boxes
botones_boxes = []
print("Selecione la cantidad de boxes que desea simular:")
for i in range(1, 11):
    botones_boxes.append(draw_button(str(i), (200 + (i - 1) * 60, 500), (50, 50)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, boton in enumerate(botones_boxes):
                if boton.collidepoint(event.pos):
                    boxes_active = i + 1
                    ejecutar_simulacion(segundos_apertura, resultados_simulacion_1, 1)
                    ejecutar_simulacion(segundos_apertura, resultados_simulacion_2, 2)  # Segunda simulación

    pygame.display.flip()

    import numpy as np

    # Suponiendo que resultados_simulacion_1 contiene los resultados de la simulación
    np.save('resultados_1.npy', resultados_simulacion_1)
    np.save('resultados_2.npy', resultados_simulacion_2)    

    # Después de cerrar el juego, cargar los resultados y generar gráficos
    results1 = np.load('resultados_1.npy').item()
    results2 = np.load('resultados_2.npy').item()

    plt.figure(figsize=(12, 6))
    plt.plot(results1.keys(), [results1[key] for key in results1.keys()], label='Simulación 1')
    plt.plot(results2.keys(), [results2[key] for key in results2.keys()], label='Simulación 2')
    plt.legend()
    plt.title('Comparación de Resultados')
    plt.xlabel('Parámetros')
    plt.ylabel('Valores')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()