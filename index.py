import pygame

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Batall Aerea")

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)

# Deadzone para evitar movimientos erráticos
DEADZONE = 0.2

# Inicializar los mandos
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()
    print(f"Mando detectado: {joystick.get_name()}")

# Clase para las naves
class Nave(pygame.sprite.Sprite):
    def __init__(self, color, pos_x, pos_y, direccion_bala):
        super().__init__()
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, color, [(0, 0), (50, 20), (0, 40)])
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.velocidad = 5
        self.direccion_bala = direccion_bala
        self.balas = pygame.sprite.Group()

    def mover(self, eje_x, eje_y):
        # Deadzone: ignorar valores pequeños para evitar drift
        if abs(eje_x) < DEADZONE:
            eje_x = 0
        if abs(eje_y) < DEADZONE:
            eje_y = 0

        # Movimiento basado en los ejes del joystick
        self.rect.x += int(eje_x * self.velocidad)
        self.rect.y += int(eje_y * self.velocidad)

        # Limitar movimiento dentro de la pantalla
        self.rect.x = max(0, min(ANCHO - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(ALTO - self.rect.height, self.rect.y))

    def disparar(self):
        # Crear una bala en la dirección asignada
        velocidad_x, velocidad_y = self.direccion_bala
        bala = Bala(self.rect.centerx, self.rect.centery, velocidad_x, velocidad_y)
        self.balas.add(bala)

    def actualizar_balas(self):
        # Actualizar balas y eliminarlas si salen de la pantalla
        self.balas.update()
        for bala in self.balas:
            if bala.rect.bottom < 0 or bala.rect.top > ALTO or bala.rect.right < 0 or bala.rect.left > ANCHO:
                self.balas.remove(bala)

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad_x, velocidad_y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

# Crear naves
nave1 = Nave(AZUL, 200, ALTO // 2, (10, 0))  # Dispara hacia la derecha
nave2 = Nave(ROJO, 600, ALTO // 2, (-10, 0))  # Dispara hacia la izquierda
grupo_naves = pygame.sprite.Group(nave1, nave2)

# Configuración de FPS
reloj = pygame.time.Clock()
FPS = 60

# Bucle principal
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        # Detectar disparos con RT (Axis 5 > 0.9 indica que el gatillo fue presionado)
        if len(joysticks) >= 2:
            if evento.type == pygame.JOYAXISMOTION:
                if evento.joy == 0 and evento.axis == 5 and evento.value > 0.9:
                    nave1.disparar()
                elif evento.joy == 1 and evento.axis == 5 and evento.value > 0.9:
                    nave2.disparar()

    # Leer los ejes de los mandos
    if len(joysticks) >= 2:
        # Movimiento de la nave 1
        eje_x1 = joysticks[0].get_axis(0)  # Eje horizontal del joystick izquierdo
        eje_y1 = joysticks[0].get_axis(1)  # Eje vertical del joystick izquierdo
        nave1.mover(eje_x1, eje_y1)

        # Movimiento de la nave 2
        eje_x2 = joysticks[1].get_axis(0)
        eje_y2 = joysticks[1].get_axis(1)
        nave2.mover(eje_x2, eje_y2)

    # Actualizar balas
    nave1.actualizar_balas()
    nave2.actualizar_balas()

    # Dibujar todo
    pantalla.fill(NEGRO)
    grupo_naves.draw(pantalla)
    nave1.balas.draw(pantalla)
    nave2.balas.draw(pantalla)
    pygame.display.flip()

    # Configurar FPS
    reloj.tick(FPS)

pygame.quit()
