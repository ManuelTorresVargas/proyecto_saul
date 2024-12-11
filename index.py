import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Guerra de mundoss")

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)

# Configuración de FPS
reloj = pygame.time.Clock()
FPS = 60

# Clase de la Nave
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Crear la imagen de la nave como un rectángulo azul
        self.image = pygame.Surface((50, 40))  # Dimensiones de la nave
        self.image.fill(AZUL)  # Color azul para la nave
        self.rect = self.image.get_rect()  # Definir el área de la nave
        self.rect.center = (ANCHO // 2, ALTO // 2)  # Posición inicial en el centro
        self.velocidad = 5  # Velocidad de movimiento de la nave

    # Función para mover la nave con las teclas
    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:  # Mover a la izquierda
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:  # Mover a la derecha
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] and self.rect.top > 0:  # Mover hacia arriba
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:  # Mover hacia abajo
            self.rect.y += self.velocidad


# Crear la nave
nave = Nave()
grupo_nave = pygame.sprite.Group()
grupo_nave.add(nave)  # Agregar la nave al grupo de sprites

# Bucle principal
corriendo = True
while corriendo:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False  # Salir del bucle si se cierra la ventana

    # Capturar las teclas presionadas
    teclas = pygame.key.get_pressed()
    nave.mover(teclas)  # Llamar a la función para mover la nave

    # Dibujar todo
    pantalla.fill(NEGRO)  # Limpiar la pantalla con color negro
    grupo_nave.draw(pantalla)  # Dibujar la nave en su posición actual

    # Actualizar la pantalla
    pygame.display.flip()

    # Configurar FPS
    reloj.tick(FPS)

pygame.quit()
