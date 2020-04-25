x = 380
y = 40
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

import numpy as np
import pygame

import time

pygame.init()

# Ancho y alto de la pantalla
width, height = 700, 700

# Creacion de la pantalla
screen = pygame.display.set_mode((height, width))
time.sleep(2)
# Color del fondo
bg = 25, 25, 25
# color del fondo elegido
screen.fill(bg)

nxC, nyC = 50, 50
dimCw = width / nxC
dimCh = height / nyC

# Estado de las celdas. Vivas = 1
gameState = np.zeros((nxC, nyC))
# Bucle de ejecucion

# Automata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1
# Automata movil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

while True:
    pygame.event.pump()

    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    for y in range(0, nxC):
        for x in range(0, nyC):
            # Calculamos el numero de vecinos cercanos.
            n_neigh = gameState[(x - 1) % nxC,     (y - 1) % nyC] + \
                      gameState[(x) %     nxC,     (y - 1) % nyC] + \
                      gameState[(x + 1) % nxC,     (y - 1) % nyC] + \
                      gameState[(x - 1) % nxC,         (y) % nyC] + \
                      gameState[(x + 1) % nxC,         (y) % nyC] + \
                      gameState[(x - 1) % nxC,     (y + 1) % nyC] + \
                      gameState[(x) %     nxC,     (y + 1) % nyC] + \
                      gameState[(x + 1) % nxC,     (y + 1) % nyC]
            # Rule #1 : Una celula muerta con exactamente 3 vecinas vivas, "revive"
            if gameState[x, y] == 0 and n_neigh == 3:
                newGameState[x, y] = 1
            # Rule #2 : Una celula viva con 2 o mas de 3 vecinas vivas, "muere"
            elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                newGameState[x, y] = 0

            # Creamos el poligo de cada celda a dibujar.
            poly = [((x) * dimCw, y * dimCh),
                    ((x + 1) * dimCw, y * dimCh),
                    ((x + 1) * dimCw, (y + 1) * dimCh),
                    ((x) * dimCw, (y + 1) * dimCh)]

            # Y dibujamos la celda para cada par de x e y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)

# Actualizamos la pantalla.
    pygame.display.flip()
