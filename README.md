
# PATHFINDING 

### What is this project?

This is a project to visually see how a pathfinding algorithm works, the algorithm at the moment that are implemented are Dijkstra, GreedyBestFirstSearch and A*. This algorithms will find a path from the start node to end node even with barriers in the way.

#### Dijkstra

Dijkstra's algorithm finds the shortest path from a start node to an end node in a weighted graph. This Python implementation uses a grid-based approach to simulate graph traversal.
However it is the slowest one because it searches in all directions, so it consumes a lot of time in unnecesary directions.

- How it works

This implementation works with a grid structure where nodes represent graph vertices, and distances between them are uniform. The algorithm starts by initializing key attributes. Each node is assigned an initial distance of infinity, except for the starting node, which has a distance of zero since no movement is required to reach itself. A priority_queue is used to process nodes based on their shortest known distance, ensuring that the most promising node is explored first. Additionally, a parents dictionary is initialized to track the immediate predecessor of each node, enabling the reconstruction of the shortest path once the end node is reached.

When the algorithm runs, it extracts the node with the smallest distance from the priority_queue. This node becomes the focus of the current step, and its neighbors are evaluated. If a shorter path to a neighboring node is discovered, the algorithm updates the neighbor's distance and records the current node as its parent. The neighbor is then added to the queue to ensure further exploration in subsequent steps. Nodes already visited or marked as barriers are skipped to avoid unnecessary processing. This process repeats until the end node is removed from the queue, indicating that the shortest path to it has been found.

Once the end node is reached, the algorithm reconstructs the shortest path by backtracking through the parents dictionary. Starting from the end node, it moves to its recorded parent and continues this process until the starting node is reached. The nodes along this path are marked to visualize the solution, highlighting the shortest route discovered.

This implementation is efficient due to the use of a priority queue, which minimizes redundant computations by always processing nodes with the smallest known distance. It also accommodates barriers, allowing for constrained pathfinding scenarios. The design suggests integration with a graphical interface, as evidenced by methods to visually mark visited nodes and paths, making it suitable for applications like grid-based games or simulations where visual feedback is essential.


```python

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
```


#### Greedy best first search


- How it works


```python

```




#### A*

- How it works


```python

```



# Resources:

- [Redbloggame Article pathfinding](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [codeProject Article](https://www.codeproject.com/Articles/5758/Path-finding-in-C)
- [Youtube video Dijkstra](https://www.youtube.com/watch?v=_B5cx-WD5EA&ab_channel=Glassbyte)
- [Wikipedia Dijkstra](https://es.wikipedia.org/wiki/Algoritmo_de_Dijkstra)
- [Javatpoint Dijkstra](https://www.javatpoint.com/dijkstras-algorithm)
- [tech with Tim YT](https://www.youtube.com/watch?v=JtiK0DOeI4A&ab_channel=TechWithTim)

### Extra

- [Implementatio of A* by redbloblgames](https://www.redblobgames.com/pathfinding/a-star/implementation.html)
- [Reddit questions and answers](https://www.reddit.com/r/roguelikedev/comments/5bsdbo/confused_about_a_pathfinding/?rdt=49160)
- [Sebastian Lague YT](https://www.youtube.com/watch?v=-L-WgKMFuhE&t=1s&ab_channel=SebastianLague)