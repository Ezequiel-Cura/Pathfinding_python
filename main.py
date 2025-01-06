import pygame
import math
from queue import PriorityQueue
from heapq import heappush, heappop

# Colores
GRAY = (200, 200, 200)
RED = (255, 0, 0)
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
        self.btn_Astar = Button(x=0, y=0, width=0, height=0, text="A*", font=font, bg_color=GRAY, text_color=BLACK)
        self.btn_greedyFirstSearch = Button(x=0, y=0, width=0, height=0, text="Greedy Best First Search", font=font, bg_color=GRAY, text_color=BLACK)

        width, height = self.screen.get_size()
        self.grid = Grid(width, height, cell_size=20)

        # Flag to track the current mode (Menu or Grid)
        self.in_menu = True

        self.start_node_bool = False
        self.end_node_bool = False

        self.start_node = ""
        self.end_node = ""

        self.choosed_algoritmo = ""

  
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
                        width, height = self.screen.get_size()
                        self.grid.update_dimensions(width, height)
                        self.start_node_bool = False
                        self.end_node_bool = False
                        
                    else:
                        self.running = False
                if e.key == pygame.K_SPACE and not self.in_menu:
                    if self.start_node_bool and self.end_node_bool:
                        if self.choosed_algoritmo == "dijkstra":
                            self.dijkstra = Dijkstra(self.grid, self.start_node, self.end_node)
                            self.dijkstra.initialize()
                        elif self.choosed_algoritmo == "GreedyBestFirstSearch":
                            self.gbfs = GreedyBestfirstSearch(self.grid, self.start_node, self.end_node)
                            self.gbfs.initialize()
                        elif self.choosed_algoritmo == "Astar":
                            self.astar = Astar(self.grid, self.start_node, self.end_node)
                            self.astar.initialize()

            # elif e.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_x, mouse_y = e.pos  # Obtener la posición del clic
            #     print(f"Mouse clicked at position: ({mouse_x}, {mouse_y})")
            elif e.type == pygame.VIDEORESIZE:
                window_width = (e.w // 10) * 10
                window_height = (e.h // 10) * 10
                
                if self.in_menu == True:
                    self.update_layout(window_width, window_height)
                else:
                    self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
                    width, height = self.screen.get_size()
                    self.grid.update_dimensions(width, height)
                    self.start_node_bool = False
                    self.end_node_bool = False

                print(f"New window size: {window_width}x{window_height}")
            
            if pygame.mouse.get_pressed()[0]: # LEFT mouse button
                mouse_x, mouse_y = e.pos  # Get the mouse click position
                print(f"Mouse clicked at position: ({mouse_x}, {mouse_y})-")

                if not self.in_menu:  # Only handle grid clicks if not in the menu
                    # Calculate the grid cell coordinates (row, col)
                    col = mouse_x // self.grid.cell_size
                    row = mouse_y // self.grid.cell_size

                    # Check if the click is within grid bounds
                    if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
                        # clicked_square = self.grid.grid[row][col]
                        if self.start_node_bool == False:
                            self.start_node_bool = True
                            self.grid.grid[row][col].color = BLUE  # Change color to BLUE = START
                            self.start_node = self.grid.grid[row][col] 

                        elif self.end_node_bool == False and self.grid.grid[row][col].color != BLUE :
                            self.end_node_bool = True
                            self.grid.grid[row][col].color = ORANGE  # Change color to ORANGE = end
                            self.end_node = self.grid.grid[row][col] 


            if pygame.mouse.get_pressed()[2]: # RIGHT mouse button    
                mouse_x, mouse_y = e.pos  # Get the mouse click position
                print(f"Mouse clicked at position: ({mouse_x}, {mouse_y})")

                if not self.in_menu:  # Only handle grid clicks if not in the menu
                    # Calculate the grid cell coordinates (row, col)
                    col = mouse_x // self.grid.cell_size
                    row = mouse_y // self.grid.cell_size

                    # Check if the click is within grid bounds
                    if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
                        # clicked_square = self.grid.grid[row][col]
                        self.grid.grid[row][col].color = BLACK  # Change color to BLUE = START
           

            if self.btn_dijstra.is_clicked(e) and self.in_menu:
                print("Clicked Dijkstra")
                self.choosed_algoritmo = "dijkstra"
                self.in_menu = False  # Cambiar al modo de grilla
            
            if self.btn_Astar.is_clicked(e) and self.in_menu:
                print("Clicked Astar")
                self.choosed_algoritmo = "Astar"
                self.in_menu = False  # Cambiar al modo de grilla

            if self.btn_greedyFirstSearch.is_clicked(e) and self.in_menu:
                print("Clicked GreedyBestFirstSearch")
                self.choosed_algoritmo = "GreedyBestFirstSearch"
                self.in_menu = False  # Cambiar al modo de grilla

    def update_layout(self, window_width, window_height):

        # Centrar el botón y ajustar su tamaño al 20% del ancho de la ventana
        btn_x = (window_width) // 2
        btn_y = (window_height) // 2  # Centrar verticalmente
        self.btn_dijstra.update_rect(btn_x, btn_y)
        self.btn_greedyFirstSearch.update_rect(btn_x,btn_y + 50)
        self.btn_Astar.update_rect(btn_x, btn_y + 100)

    def update(self, dt):

        if not self.in_menu and hasattr(self, 'dijkstra') and not self.dijkstra.finished:
            self.dijkstra.run()
        if not self.in_menu and hasattr(self, 'gbfs') and not self.gbfs.finished:
            self.gbfs.run()
        if not self.in_menu and hasattr(self, 'astar') and not self.astar.finished:
            self.astar.run()
        

    def draw(self):
        if self.in_menu:
            # Dibujar el menú de botones
            self.btn_dijstra.draw(self.screen)
            self.btn_Astar.draw(self.screen)
            self.btn_greedyFirstSearch.draw(self.screen)
        else:
            # Dibujar la grilla
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

            # pygame.display.flip()
            pygame.display.update()

class Astar:
    def __init__(self,grid, start_node, end_node):
        self.grid = grid
        self.start_node = start_node # The start node
        self.end_node = end_node # the end node
        self.parents = {} # this is directory of the previos nodes, in other words the parents of the nodes visited, with this we will know the shortest path
        self.distances = {} # distances to nodes, every distance is 1 and that will be adding up till we find the end node
        self.visited = set() # a set o nodes that were visited, they cannot be repeated
        self.priority_queue = PriorityQueue() # data structure where it prioristse the node with the smaller distances
        self.in_queue = set()
        self.finished = False  # Flag to indicate if the algorithm is complete
        self.current_path = []  # Store the shortest path
        self.int = 1
    
    def initialize(self):
        # Initialize distances and parents
        for row in self.grid.grid:
            for square in row:
                self.distances[square] = float('inf')  # Start with infinity
                self.parents[square] = None  # No parent initially

        self.priority_queue.put((0,self.int, self.start_node)) # when initialize we put the only node we have the start node
        self.distances[self.start_node] = 0 # the first distance is always zero because from start node to start node is 0
        self.in_queue.add(self.start_node)
        self.int += 1


    def run(self):
        if not self.priority_queue.empty(): # if the priority queue is not empty run the lagorithm
            _, _, removed_node = self.priority_queue.get() # this a pop of the queue, we remove the priority node, with some information like distance and the node
            self.in_queue.remove(removed_node)


            # Mark as visited
            if removed_node != self.start_node and removed_node != self.end_node: # this is only to not over paint the important nodes
                removed_node.make_visited() # change color of the square to a red, it means that node was visited

            self.visited.add(removed_node) # we added it to the set of visited nodes

             # Stop the algorithm if we reach the end_node
            if removed_node == self.end_node: 
                self.reconstruct_path()
                self.finished = True
                # if we reach the end node there is no reason to keep searching a short path beacause you would not find it
                return
            

            for neighbor in removed_node.neighbors: # here we check all the neighbors node of the priority node we are analising
                if neighbor in self.visited or neighbor.is_barrier(): # if the neighbors was already visited or the node is a barrier we skip it
                    continue

                # Calculate the new distance (g(neighbor))
                new_distance = self.distances[removed_node] + 1  # Assuming all edges have weight 1
                
                priority = self.heuristic(neighbor, self.end_node)
                

                if new_distance < self.distances[neighbor]:
                    self.distances[neighbor] = new_distance
                    self.parents[neighbor] = removed_node
                    # Calculate f(n) = g(neighbor) + h(neighbor)
                    priority = new_distance + self.heuristic(neighbor, self.end_node)


                    if neighbor not in self.in_queue:
                        self.parents[neighbor] = removed_node
                        self.priority_queue.put((priority, self.int, neighbor))
                        self.in_queue.add(neighbor)  # Mark as in queue
                        self.int += 1
                        if neighbor != self.start_node and neighbor != self.end_node:
                            neighbor.make_in_queue()

        else:
            self.finished = True




    def reconstruct_path(self):
            """Reconstructs the shortest path by backtracking from the end_node."""
            current = self.end_node
            while current in self.parents:  # Backtrack the parents dictionary
                parent = self.parents[current]
                if parent is None:
                    break
                if parent != self.start_node:
                    parent.make_path()  # Visualize the path
                    self.current_path.append(parent)
                current = parent





    def heuristic(self,a, b):
        # not manhattan distance
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        return max(dx, dy)  # Diagonal distance   


class GreedyBestfirstSearch:
    def __init__(self,grid, start_node, end_node):
        self.grid = grid
        self.start_node = start_node # The start node
        self.end_node = end_node # the end node
        self.parents = {} # this is directory of the previos nodes, in other words the parents of the nodes visited, with this we will know the shortest path
        
        self.visited = set() # a set o nodes that were visited, they cannot be repeated
        self.priority_queue = PriorityQueue() # data structure where it prioristse the node with the smaller distances
        self.in_queue = set()
        self.finished = False  # Flag to indicate if the algorithm is complete
        self.current_path = []  # Store the shortest path
        self.int = 1
    
    def initialize(self):
        # Initialize distances and parents
        for row in self.grid.grid:
            for square in row:
                self.parents[square] = None  # No parent initially

        self.priority_queue.put((0,self.int, self.start_node)) # when initialize we put the only node we have the start node
        self.in_queue.add(self.start_node)
        self.int += 1

    def run(self):
        if not self.priority_queue.empty(): # if the priority queue is not empty run the lagorithm
            _, _, removed_node = self.priority_queue.get() # this a pop of the queue, we remove the priority node, with some information like distance and the node
            self.in_queue.remove(removed_node)

            # Mark as visited
            if removed_node != self.start_node and removed_node != self.end_node: # this is only to not over paint the important nodes
                removed_node.make_visited() # change color of the square to a red, it means that node was visited

            self.visited.add(removed_node) # we added it to the set of visited nodes

            # Stop the algorithm if we reach the end_node
            if removed_node == self.end_node: 
                self.reconstruct_path()
                self.finished = True
                # if we reach the end node there is no reason to keep searching a short path beacause you would not find it
                return

            for neighbor in removed_node.neighbors: # here we check all the neighbors node of the priority node we are analising
                if neighbor in self.visited or neighbor.is_barrier(): # if the neighbors was already visited or the node is a barrier we skip it
                    continue
                
                priority = self.heuristic(neighbor, self.end_node)

                if neighbor not in self.visited and neighbor not in self.in_queue and not neighbor.is_barrier():
                    self.parents[neighbor] = removed_node
                    self.priority_queue.put((priority, self.int, neighbor))
                    self.in_queue.add(neighbor)  # Mark as in queue
                    self.int += 1
                    if neighbor != self.start_node and neighbor != self.end_node:
                        neighbor.make_in_queue()
        else:
            self.finished = True
    
    def heuristic(self,a, b):
        # # Manhattan distance on a square grid
        # return abs(a.x - b.x) + abs(a.y - b.y)

        # not manhattan distance
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        return max(dx, dy)  # Diagonal distance
    
    def reconstruct_path(self):
        """Reconstructs the shortest path by backtracking from the end_node."""
        current = self.end_node # we backtrack the nodes to the start node to see the path
        while current in self.parents: # in the parents directory we have all the parents but we will use only the one that is the shortest
            current = self.parents[current] # 
            if current is None:  # Prevent issues if a node has no parent
                break
            if current != self.start_node: # here to check if we reach the start node
                current.make_path()  # Change color to indicate the shortest path
                self.current_path.append(current)  # Store the path nodes for reference
    





class Dijkstra:
    def __init__(self, grid, start_node, end_node):
        self.grid = grid
        self.start_node = start_node # The start node
        self.end_node = end_node # the end node
        self.parents = {} # this is directory of the previos nodes, in other words the parents of the nodes visited, with this we will know the shortest path
        self.visited = set() # a set o nodes that were visited, they cannot be repeated
        self.distances = {} # distances to nodes, every distance is 1 and that will be adding up till we find the end node
        self.priority_queue = PriorityQueue() # data structure where it prioristse the node with the smaller distances
        self.in_queue = set()
        self.finished = False  # Flag to indicate if the algorithm is complete
        self.current_path = []  # Store the shortest path

    def initialize(self):
        # Initialize distances and parents
        for row in self.grid.grid:
            for square in row:
                self.distances[square] = float('inf')  # Start with infinity
                self.parents[square] = None  # No parent initially

        self.priority_queue.put((0, id(self.start_node), self.start_node)) # when initialize we put the only node we have the start node
        self.in_queue.add(self.start_node)
        self.distances[self.start_node] = 0 # the first distance is always zero because from start node to start node is 0

    

    def run(self):
        """Runs one step of Dijkstra's algorithm."""
        if not self.priority_queue.empty(): # if the priority queue is not empty run the lagorithm
            removed_distance, _, removed_node = self.priority_queue.get() # this a pop of the queue, we remove the priority node, with some information like distance and the node
            self.in_queue.remove(removed_node)
            # Mark as visited
            if removed_node != self.start_node and removed_node != self.end_node: # this is only to not over paint the important nodes
                removed_node.make_visited() # change color of the square to a red, it means that node was visited

            self.visited.add(removed_node) # we added it to the set of visited nodes

            # Stop the algorithm if we reach the end_node
            if removed_node == self.end_node: 
                self.reconstruct_path()
                self.finished = True
                # if we reach the end node there is no reason to keep searching a short path beacause you would not find it
                return

            for neighbor in removed_node.neighbors: # here we check all the neighbors node of the priority node we are analising
                if neighbor in self.visited or neighbor.is_barrier(): # if the neighbors was already visited or the node is a barrier we skip it
                    continue

                new_distance = removed_distance + 1 # we add 1 to the distance, every time we pass to another node the distance is one

                if new_distance < self.distances[neighbor] and neighbor not in self.in_queue: # here we check if the new calculated distance is lower than distance of the neighbor that could be infinity, or a smaller distance to that node
                    self.distances[neighbor] = new_distance # we overwrite the distance with the shorter distance
                    self.parents[neighbor] = removed_node # we put the parent of the neighbor 
                    self.priority_queue.put((new_distance, id(neighbor), neighbor)) # and we put the neighbor in the priority queue
                    self.in_queue.add(neighbor)
                    # Mark as in queue
                    if neighbor != self.start_node and neighbor != self.end_node:
                        neighbor.make_in_queue()
        else:
            self.finished = True

    def reconstruct_path(self):
        """Reconstructs the shortest path by backtracking from the end_node."""
        current = self.end_node # we backtrack the nodes to the start node to see the path
        while current in self.parents: # in the parents directory we have all the parents but we will use only the one that is the shortest
            current = self.parents[current] # 
            if current is None:  # Prevent issues if a node has no parent
                break
            if current != self.start_node: # here to check if we reach the start node
                current.make_path()  # Change color to indicate the shortest path
                self.current_path.append(current)  # Store the path nodes for reference


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
        self.state = 0 

    def update_neighbors(self,grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():# UP
            self.neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier():# RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def get_pos(self):
        return self.row, self.col
        
    def is_barrier(self):
        return self.color == BLACK

    def make_end(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK
        self.is_barrier = True

    def make_visited(self):
        self.color = RED

    def make_path(self):
        self.color = PURPLE

    def make_in_queue(self):
        self.color = YELLOW

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        self.rect = pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def __str__(self):
        return f"Square(row={self.row}, col={self.col}), color={self.color}"
    

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

        for row in range(self.rows):
            for col in range(self.cols):
                    self.grid[row][col].update_neighbors(self.grid)

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
