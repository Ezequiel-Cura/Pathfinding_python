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

        self.screenDim = (500, 600)
        self.screen = pygame.display.set_mode(self.screenDim, pygame.RESIZABLE)
        self.background = BLACK
        self.running = False

        # Tamaño inicial del botón (se recalculará en `update_layout`)
        self.btn_dijstra = Button(x=0, y=0, width=0, height=0, text="Dijkstra", font=font, bg_color=GRAY, text_color=BLACK)
        self.grid = Grid(200, 200, cell_size=20)

        # Flag to track the current mode (Menu or Grid)
        self.in_menu = True

        # Configurar elementos en función del tamaño de la ventana
        self.update_layout(*self.screenDim)

    def poll(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_ESCAPE:
                    if not self.in_menu:
                        self.in_menu = True  # Regresar al menú
                    else:
                        self.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = e.pos  # Obtener la posición del clic
                print(f"Mouse clicked at position: ({mouse_x}, {mouse_y})")
            elif e.type == pygame.VIDEORESIZE:
                window_width = (e.w // 10) * 10
                window_height = (e.h // 10) * 10
                
                if self.in_menu == True:
                    self.update_layout(window_width, window_height)
                else:
                    self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
                    width, height = self.screen.get_size()
                    self.grid.update_dimensions(width, height)

                print(f"New window size: {window_width}x{window_height}")

            if self.btn_dijstra.is_clicked(e) and self.in_menu:
                print("Clicked Dijkstra")
                self.in_menu = False  # Cambiar al modo de grilla

    def update_layout(self, window_width, window_height):

        # Centrar el botón y ajustar su tamaño al 20% del ancho de la ventana
        btn_x = (window_width) // 2
        btn_y = (window_height) // 2  # Centrar verticalmente
        self.btn_dijstra.update_rect(btn_x, btn_y)

    def update(self, dt):
        pass

    def draw(self):
        if self.in_menu:
            # Dibujar el menú de botones
            self.btn_dijstra.draw(self.screen)
        else:
            # Dibujar la grilla
            width, height = self.screen.get_size()
            self.grid.update_dimensions(width,height)
            self.grid.draw(self.screen)


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
    
    def __init__(self,row,col,width,total_rows,total_cols):
        self.row = row
        self.col = col
        self.cell_size = width
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.width = width

        self.x = col * width  # Corrected for column-based positioning
        self.y = row * width  # Corrected for row-based positioning

        self.color = WHITE
        self.state = 0  # 0: walkable, 1: obstacle, etc.
  
# 0: Empty space (walkable).
# 1: Obstacle (non-walkable).
# 2: Start point.
# 3: End point.
# 4: Path node (part of the shortest path).
    

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def get_pos(self):
        return self.row, self.col
    
    def is_barrier(self):
        return self.color == BLACK

    def draw(self, win):
       
        self.rect = pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def __str__(self):
        return f"Square(row={self.row}, col={self.col})"
    

class Grid:
    def __init__(self, screen_width, screen_height, cell_size):
        self.cell_size = cell_size
        self.grid = []
        self.rows = 0
        self.cols = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.update_dimensions(screen_width, screen_height)
        
    def update_dimensions(self, screen_width, screen_height):
        self.grid = []  # Clear the grid
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Calculate the new number of rows and columns
        self.cols = self.screen_width // self.cell_size
        self.rows = self.screen_height // self.cell_size

        # Reinitialize the grid with new dimensions
        for row in range(self.rows):
            new_row = []
            for col in range(self.cols):
                new_row.append(Square(row, col, self.cell_size, self.rows, self.cols))
            self.grid.append(new_row)


    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].draw(screen)
                pygame.draw.rect(screen, GREY, self.grid[row][col].rect, 1)  # Borde de la celda

                
        

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def update_rect(self, x, y, width = 100, height=30):
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
