import pygame
import math
import sys

# Inicializar Pygame
pygame.init()

# Configurar las dimensiones de la pantalla
ANCHO = 1500
ALTO = 700
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Batalla de Naves con Sistema de Vida y Disparos")

# Colores
BLANCO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (255, 255, 255)

# Cargar imágenes de las naves
imagen_nave1 = pygame.image.load("assets/Nave1.png")
imagen_nave2 = pygame.image.load("assets/Nave2.png")

# Redimensionar imágenes para hacerlas más grandes
imagen_nave1 = pygame.transform.scale(imagen_nave1, (80, 80))
imagen_nave2 = pygame.transform.scale(imagen_nave2, (80, 80))

# Personajes
personaje1 = {
    "x": ANCHO // 3, "y": ALTO // 2, "ancho": 80, "alto": 80,
    "color": ROJO, "velocidad": 4, "vida": 100, "angulo": 0
}
personaje2 = {
    "x": 2 * ANCHO // 3, "y": ALTO // 6, "ancho": 80, "alto": 80,
    "color": AZUL, "velocidad": 4, "vida": 100, "angulo": 0
}

# Inicializar los mandos
pygame.joystick.init()
mandos = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for mando in mandos:
    mando.init()
    print(f"Mando detectado: {mando.get_name()}")

if len(mandos) < 2:
    print("Se necesitan al menos 2 mandos para controlar a ambos personajes.")
    pygame.quit()
    sys.exit()

# Lista para almacenar los disparos
disparos1 = []
disparos2 = []
vel_disparo = 10

# Función para actualizar los disparos
def actualizar_disparos(disparos):
    for disparo in disparos:
        disparo["x"] += math.cos(math.radians(disparo["angulo"])) * vel_disparo
        disparo["y"] -= math.sin(math.radians(disparo["angulo"])) * vel_disparo
    return [d for d in disparos if 0 < d["x"] < ANCHO and 0 < d["y"] < ALTO]

# Función para manejar colisiones
def chequear_colisiones(disparos, enemigo):
    for disparo in disparos:
        if (enemigo["x"] < disparo["x"] < enemigo["x"] + enemigo["ancho"] and
            enemigo["y"] < disparo["y"] < enemigo["y"] + enemigo["alto"]):
            # Disparo impacta
            enemigo["vida"] -= 5
            if enemigo["vida"] < 0:
                enemigo["vida"] = 0
            disparos.remove(disparo)

# Función para dibujar barras de vida y nombres
def dibujar_vida_y_nombres():
    # Personaje 1
    pygame.draw.rect(screen, ROJO, (50, 30, 300, 20))
    pygame.draw.rect(screen, VERDE, (50, 30, personaje1["vida"] * 3, 20))
    texto1 = fuente.render("Player 1", True, NEGRO)
    screen.blit(texto1, (50, 5))

    # Personaje 2
    pygame.draw.rect(screen, ROJO, (ANCHO - 350, 30, 300, 20))
    pygame.draw.rect(screen, VERDE, (ANCHO - 350, 30, personaje2["vida"] * 3, 20))
    texto2 = fuente.render("Player 2", True, NEGRO)
    screen.blit(texto2, (ANCHO - 350, 5))

# Función para dibujar personajes con imágenes rotadas
def dibujar_personaje_con_imagen(personaje, imagen):
    imagen_rotada = pygame.transform.rotate(imagen, -personaje["angulo"])
    rect_imagen = imagen_rotada.get_rect(center=(personaje["x"], personaje["y"]))
    screen.blit(imagen_rotada, rect_imagen)

# Fuente para los textos
fuente = pygame.font.SysFont("Arial", 24)

# Bucle principal
juego = True
while juego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False

        # Detectar botones del mando
        if event.type == pygame.JOYBUTTONDOWN:
            if event.joy == 0:
                if event.button == 0:  # Botón para disparar
                    disparos1.append({
                        "x": personaje1["x"], "y": personaje1["y"], 
                        "color": ROJO, "angulo": personaje1["angulo"]
                    })
                elif event.button == 2:  # Botón para duplicar velocidad
                    personaje1["velocidad"] *= 2
            elif event.joy == 1:
                if event.button == 0:  # Botón para disparar
                    disparos2.append({
                        "x": personaje2["x"], "y": personaje2["y"], 
                        "color": AZUL, "angulo": personaje2["angulo"]
                    })
                elif event.button == 2:  # Botón para duplicar velocidad
                    personaje2["velocidad"] *= 2

        if event.type == pygame.JOYBUTTONUP:
            if event.joy == 0 and event.button == 2:
                personaje1["velocidad"] = 4
            elif event.joy == 1 and event.button == 2:
                personaje2["velocidad"] = 4

    # Movimiento y rotación
    mando1 = mandos[0]
    eje_x1 = mando1.get_axis(0)
    eje_y1 = mando1.get_axis(1)
    personaje1["angulo"] = math.degrees(math.atan2(-eje_y1, eje_x1))
    personaje1["x"] += eje_x1 * personaje1["velocidad"]
    personaje1["y"] += eje_y1 * personaje1["velocidad"]

    mando2 = mandos[1]
    eje_x2 = mando2.get_axis(0)
    eje_y2 = mando2.get_axis(1)
    personaje2["angulo"] = math.degrees(math.atan2(-eje_y2, eje_x2))
    personaje2["x"] += eje_x2 * personaje2["velocidad"]
    personaje2["y"] += eje_y2 * personaje2["velocidad"]

    # Limitar los personajes dentro de la pantalla
    personaje1["x"] = max(0, min(ANCHO - personaje1["ancho"], personaje1["x"]))
    personaje1["y"] = max(0, min(ALTO - personaje1["alto"], personaje1["y"]))
    personaje2["x"] = max(0, min(ANCHO - personaje2["ancho"], personaje2["x"]))
    personaje2["y"] = max(0, min(ALTO - personaje2["alto"], personaje2["y"]))

    # Actualizar disparos
    disparos1 = actualizar_disparos(disparos1)
    disparos2 = actualizar_disparos(disparos2)

    # Chequear colisiones
    chequear_colisiones(disparos1, personaje2)
    chequear_colisiones(disparos2, personaje1)

    # Dibujar la pantalla
    screen.fill(BLANCO)
    dibujar_vida_y_nombres()
    dibujar_personaje_con_imagen(personaje1, imagen_nave1)
    dibujar_personaje_con_imagen(personaje2, imagen_nave2)
    for disparo in disparos1:
        pygame.draw.circle(screen, ROJO, (int(disparo["x"]), int(disparo["y"])), 5)
    for disparo in disparos2:
             pygame.draw.circle(screen, AZUL, (int(disparo["x"]), int(disparo["y"])), 5)

    pygame.display.flip()

pygame.quit()
sys.exit()
