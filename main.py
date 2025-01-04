import pygame
import math
from queue import PriorityQueue


# Colores
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Main:
    def __init__(self):
        pygame.init()
        
        font = pygame.font.Font(None, 36)  # Fuente predeterminada de Pygame

        self.screenDim = (500, 500)
        self.screen = pygame.display.set_mode(self.screenDim, pygame.RESIZABLE)
        self.background = BLACK
        self.running = False

        # Tamaño inicial del botón (se recalculará en `update_layout`)
        self.btn_dijstra = Button(x=0, y=0, width=0, height=0, text="Dijstra", font=font, bg_color=GRAY, text_color=BLACK)
        self.grid = Grid(self.screenDim[0], self.screenDim[1], cell_size=20)

        # Configurar elementos en función del tamaño de la ventana
        self.update_layout(*self.screenDim)

    def poll(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_ESCAPE:
                    self.running = False
            elif e.type == pygame.VIDEORESIZE:
                window_width, window_height = e.w, e.h
                self.screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
                self.grid.update_dimensions(window_width, window_height)
                self.update_layout(window_width, window_height)
                print(f"New window size: {window_width}x{window_height}")

            if self.btn_dijstra.is_clicked(e):
                print("clicked dijstra")

    def update_layout(self, window_width, window_height):
        # Centrar el botón y ajustar su tamaño al 20% del ancho de la ventana
        btn_width = int(window_width * 0.2)
        btn_height = int(window_height * 0.1)
        btn_x = (window_width - btn_width) // 2
        btn_y = window_height - btn_height - 20  # 20px desde el borde inferior
        self.btn_dijstra.update_rect(btn_x, btn_y, btn_width, btn_height)

    def update(self, dt):
        pass

    def draw(self):
        self.grid.draw(self.screen)
        self.btn_dijstra.draw(self.screen)

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(40) / 1000.0
            
            self.screen.fill(self.background)
            
            self.poll()
            self.update(dt)
            self.draw()

            pygame.display.flip()


class Square:
    
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.neighbors = []
        
        self.color = WHITE

    def update_neighbors(self):
        pass



class Grid:
    def __init__(self, screen_width, screen_height, cell_size):
        self.cell_size = cell_size
        self.update_dimensions(screen_width, screen_height)

    def update_dimensions(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cols = screen_width // self.cell_size
        self.rows = screen_height // self.cell_size
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size
                )
                pygame.draw.rect(screen, WHITE, rect, 1)  # Borde de la celda

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def update_rect(self, x, y, width, height):
        self.rect.update(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botón izquierdo del mouse
            return self.rect.collidepoint(event.pos)
        return False

if __name__ == '__main__':
    main = Main()
    print("Starting...")
    main.run()
    print("Shutting down...")
