import pygame
import random
import math

# Configuración inicial de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulación de Sistema de Atención al Público')
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
VIOLET = (238, 130, 238)
BLUE = (0, 0, 255)

# Parámetros del sistema
NUM_BOXES = 5  # Puede ser de 1 a 10
BOX_COST = 1000
CUSTOMER_LOSS_COST = 10000
OPEN_HOURS = 4  # De 8 a 12 horas
SECONDS_PER_HOUR = 3600
TOTAL_SECONDS = OPEN_HOURS * SECONDS_PER_HOUR
ARRIVAL_PROBABILITY = 1 / 144
SERVICE_TIME_MEAN = 10 * 60  # 10 minutos en segundos
SERVICE_TIME_STD_DEV = 5 * 60  # 5 minutos en segundos
CLOSE_TIME = 12 * SECONDS_PER_HOUR

# Variables de simulación
customers = []
boxes = [None] * NUM_BOXES
waiting_queue = []
served_customers = 0
unserved_customers = 0
total_customers = 0
abandoned_customers = 0  # Conteo de clientes abandonados
current_time = 0
service_times = []
waiting_times = []

# Función para generar tiempo de atención
def generate_service_time():
    return max(1, int(random.gauss(SERVICE_TIME_MEAN, SERVICE_TIME_STD_DEV)))

class Customer:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.service_end_time = None

    def start_service(self, start_time):
        self.service_start_time = start_time
        self.service_end_time = start_time + generate_service_time()
        service_times.append(self.service_end_time - self.service_start_time)

    def is_being_served(self, current_time):
        return self.service_start_time is not None and self.service_start_time <= current_time < self.service_end_time

    def is_served(self, current_time):
        return self.service_end_time is not None and current_time >= self.service_end_time

    def has_abandoned(self, current_time):
        return self.arrival_time + 30 * 60 <= current_time and self.service_end_time is None

# Función para dibujar texto en pantalla
def draw_text(text, x, y, font_size=24, color=BLACK):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Main loop
running = True
while running and current_time <= TOTAL_SECONDS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generar nuevos clientes
    if random.random() < ARRIVAL_PROBABILITY:
        customers.append(Customer(current_time))
        total_customers += 1

    # Asignar clientes
    for i in range(NUM_BOXES):
        if boxes[i] is None and waiting_queue:
            customer = waiting_queue.pop(0)
            customer.start_service(current_time)
            boxes[i] = customer
            waiting_times.append(current_time - customer.arrival_time)

    # Procesar clientes en boxes
    for i in range(NUM_BOXES):
        if boxes[i] is not None:
            if boxes[i].is_served(current_time):
                boxes[i] = None
                served_customers += 1
            elif boxes[i].has_abandoned(current_time):
                abandoned_customers += 1
                unserved_customers += 1  # Incrementa unserved_customers cuando un cliente abandona
                boxes[i] = None

    # Verificar si algún cliente debe abandonar el local
    for customer in customers:
        if not customer.is_being_served(current_time) and customer.has_abandoned(current_time):
            abandoned_customers += 1
            customers.remove(customer)
        elif not customer.is_being_served(current_time) and customer.service_start_time is None:
            waiting_queue.append(customer)

    # Mover clientes a la cola
    for customer in customers:
        if not customer.is_being_served(current_time) and customer.service_start_time is None:
            waiting_queue.append(customer)

    # Dibuje
    screen.fill(WHITE)

    # Dibujar boxes
    for i in range(NUM_BOXES):
        color = GREEN if boxes[i] is None else RED
        pygame.draw.rect(screen, color, (50 + i * 70, 50, 60, 60))

    # Dibujar clientes en la cola
    for i, customer in enumerate(waiting_queue):
        pygame.draw.circle(screen, VIOLET, (100, 150 + i * 30), 10)

    pygame.display.flip()
    clock.tick(60)
    current_time += 1

pygame.quit()

# Contar clientes no atendidos como abandonados
for customer in customers:
    if customer.service_start_time is None:
        abandoned_customers += 1
        unserved_customers += 1

# Imprimir resultados al final de la simulación
print("Resultados:")
print(f"1) Total de clientes ingresaron al local: {total_customers}")
print(f"2) Clientes atendidos: {served_customers}")
print(f"3) Clientes no atendidos (abandonaron el local por demoras): {unserved_customers}")
print(f"4) Clientes abandonados: {abandoned_customers}")
print(f"5) Tiempo mínimo de atención en box: {min(service_times) / 60:.2f} minutos" if service_times else "No hay datos")
print(f"6) Tiempo máximo de atención en box: {max(service_times) / 60:.2f} minutos" if service_times else "No hay")
