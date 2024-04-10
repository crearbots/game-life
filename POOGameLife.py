import pygame
import numpy as np
import time

class GameOfLife:
    """Clase que representa el juego en sí mismo."""
    def __init__(self, width, height, nxC, nyC):
        self.width = width
        self.height = height
        self.nxC = nxC
        self.nyC = nyC
        self.cells = np.zeros((nxC, nyC))

    def set_pattern(self, pattern, x_offset=0, y_offset=0):
        """Establece un patrón específico en el tablero."""
        pattern_width = len(pattern[0])
        pattern_height = len(pattern)
        for y in range(pattern_height):
            for x in range(pattern_width):
                self.cells[(x + x_offset) % self.nxC][(y + y_offset) % self.nyC] = pattern[y][x]

    def update(self):
        """Actualiza el estado del juego según las reglas del Juego de la Vida."""
        new_cells = np.zeros((self.nxC, self.nyC))
        for y in range(self.nyC):
            for x in range(self.nxC):
                n_neigh = np.count_nonzero([
                self.cells[(x - 1) % self.nxC][(y - 1) % self.nyC],
                self.cells[x % self.nxC][(y - 1) % self.nyC],
                self.cells[(x + 1) % self.nxC][(y - 1) % self.nyC],
                self.cells[(x - 1) % self.nxC][y % self.nyC],
                self.cells[(x + 1) % self.nxC][y % self.nyC],
                self.cells[(x - 1) % self.nxC][(y + 1) % self.nyC],
                self.cells[x % self.nxC][(y + 1) % self.nyC],
                self.cells[(x + 1) % self.nxC][(y + 1) % self.nyC] ])
                if self.cells[x][y] == 0 and n_neigh == 3:
                    new_cells[x][y] = 1
                elif self.cells[x][y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    new_cells[x][y] = 0
                else:
                    new_cells[x][y] = self.cells[x][y]
        self.cells = np.copy(new_cells)

class GameWindow:
    """Clase que maneja la ventana del juego."""
    def __init__(self, width, height, nxC, nyC):
        self.width = width
        self.height = height
        self.nxC = nxC
        self.nyC = nyC
        self.cell_width = width / nxC
        self.cell_height = height / nyC
        self.game = GameOfLife(width, height, nxC, nyC)
        self.bg = (25, 25, 25)
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

    def draw(self):
        """Dibuja el estado actual del juego en la ventana."""
        self.screen.fill(self.bg)
        for y in range(self.nyC):
            for x in range(self.nxC):
                color = (128, 128, 128) if self.game.cells[x][y] == 0 else (255, 255, 255)
                pygame.draw.rect(self.screen, color, (x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height), 1)
        pygame.display.flip()

    def handle_events(self):
        """Maneja los eventos de usuario."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def run(self):
        """Inicia el bucle principal del juego."""
        while True:
            self.handle_events()
            self.game.update()  # Actualiza el estado del juego en cada iteración
            self.draw()
            time.sleep(0.1)

# Definimos el patrón "Planeador" (Glider)
pattern_glider = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1]
]

# Crear y ejecutar la ventana del juego
game_window = GameWindow(700, 700, 50, 50)
game_window.game.set_pattern(pattern_glider, x_offset=10, y_offset=10)  # Establece el patrón "Planeador"
game_window.run()

