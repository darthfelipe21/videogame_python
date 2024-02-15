import pygame
import random
import math
from pygame import mixer
import io


"""# Transformar fuente a bytes
def fuente_byte(fuente_letras):
    # Abrir archivo TTF en binario
    with open(fuente_letras, 'rb') as f:
        # Leer todos los bytes del archivo
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)
"""

# Inicializar el pygame
pygame.init()

# Ajustar tamaño pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("estrella.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo-hiperespacial.jpg")

# Agregar musica
mixer.music.load("starwars theme.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Crear jugador
img_jugador = pygame.image.load("astronave.png")
jugador_x = 368  # 800 / 2 - cantidad de la mitad de pixeles de la imagen (64/2)
jugador_y = 536  # 0 es arriba 600 es abajo, 600 - 64
jugador_x_cambio = 0  # Movimiento inicial

# Crear enemigos
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("tiefighter.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Crear balas
img_bala = pygame.image.load("menos.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False


# Puntaje
puntaje = 0
# fuente_score = fuente_byte("soloistlaserital1.ttf")
fuente_score = "soloistlaserital1.ttf"
fuente = pygame.font.Font(fuente_score, 32)
texto_x = 10
texto_y = 10


# Texto game over
fuente_final = pygame.font.Font(fuente_score, 60)


def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255, 232, 31))
    pantalla.blit(mi_fuente_final, (200, 250))


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Score: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Funcion jugador
def jugador_pos(x, y):
    pantalla.blit(img_jugador, (x, y))


# Funcion enemigo
def enemigo_pos(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


def colision(x_1, y_1, x_2, y_2):
    operacion1 = x_2 - x_1
    operacion2 = y_2 - y_1
    distancia = math.sqrt(math.pow(operacion1, 2) + math.pow(operacion2, 2))
    if distancia < 27:
        return True
    else:
        return False


se_ejecuta = True
while se_ejecuta:
    """ # RGB
    pantalla.fill((0, 0, 153))"""
    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))

    # Iterar evento
    for evento in pygame.event.get():
        # Al darle cerrar termina la ejecución
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                laser = mixer.Sound('laser.mp3')
                laser.play()
                # Evitar que la bala se mueva de posicion si se presiona varias veces el disparador
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        # Evento soltar flecha
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
    # Modificar ubicación
    jugador_x += jugador_x_cambio

    # Mantener dentro de bordes
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:   # 800 menos los 64 pixeles
        jugador_x = 736

    # Modificar ubicación enemigo
    for i in range(cantidad_enemigos):
        # Game Over
        if enemigo_y[i] > 480:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[i] += enemigo_x_cambio[i]

        # Mantener dentro de bordes del enemigo
        if enemigo_x[i] <= 0:
            enemigo_x_cambio[i] = 0.5
            enemigo_y[i] += enemigo_y_cambio[i]
        elif enemigo_x[i] >= 736:   # 800 menos los 64 pixeles
            enemigo_x_cambio[i] = -0.5
            enemigo_y[i] += enemigo_x_cambio[i]
        enemigo_pos(enemigo_x[i], enemigo_y[i], i)

        # Colision
        hay_colision = colision(enemigo_x[i], enemigo_y[i], bala_x, bala_y)
        if hay_colision:
            explosion = mixer.Sound("explosion.mp3")
            explosion.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            #print(puntaje)
            enemigo_x[i] = random.randint(0, 736)
            enemigo_y[i] = random.randint(50, 200)

    # Movimiento bala
    if bala_y <= -16:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador_pos(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    # Actualizar
    pygame.display.update()








