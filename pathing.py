import numpy as np
import pygame
import sys

# Constants
size = width, height = (800, 800)
cell_count = cells_horizontal, cells_vertical = (50, 50)
cell_size = cell_width, cell_height = (width // cells_horizontal, height // cells_vertical)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
dark_green = (0, 100, 0)
light_green = (100, 255, 100)
blue = (0, 0, 255)
purple = (255, 0, 255)



def setup_grid():
    # Initialize a place holder array
    grid = np.zeros(cell_count, dtype=Square)
    # Populate the grid with square objects
    for j, row in enumerate(grid):
        for i, _ in enumerate(row):
            grid[j][i] = Square(i, j)

    return grid

def display_grid(screen, grid):
    # Set the background to black
    screen.fill(black)
    # Loop through all elements in the grid
    for j, row in enumerate(grid):
        for i, square in enumerate(row):
            # Set the square color - defaults to white
            square_color = white 
            if square.obstacle:
                square_color = black
            elif square.start:
                square_color = light_green
            elif square.finish:
                square_color = dark_green

            # Draw the square in the appropriate color
            pygame.draw.rect(screen, square_color, (i * cell_width, j * cell_height, cell_width, cell_height), 0)
            # Draw square outline
            pygame.draw.rect(screen, black, (i * cell_width, j * cell_height, cell_width, cell_height), 1)
    # Update the display
    pygame.display.update()

def check_drawing_mode_toggle():
    # Check system events
    for event in pygame.event.get():
        # Quit if desired
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        # If mouse is clicked toggle drawing mode
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
        elif event.type == pygame.MOUSEBUTTONUP:
            return True
        else:
            return False


def mouse_to_coord():
    """
    Gets the mouse position as a coordinate of a field in the grid.
    Returns:
    Tuple(x, y)
    """
    # Get mouse position
    x_mouse, y_mouse = pygame.mouse.get_pos()
    
    # Convert coordinates to a position on the board
    x_coord, y_coord = x_mouse // cell_width, y_mouse // cell_height

    return (x_coord, y_coord)

def set_obstacles(grid):
    # Get mouse position
    x, y = mouse_to_coord()

    # Set the selected squares to be obstacles
    grid[y][x].obstacle = True


class Square:
    # 2d list to keep track of visited squares /  nodes
    visited = [[False for _ in range(cells_horizontal)] for _ in range(cells_vertical)]

    def __init__(self, x, y):
        # location
        self.x = x
        self.y = x
        # type
        self.obstacle = False
        self.start = False
        self.finish = False
        # node information
        self.current = False
        self.visited = False
        self.distance = float("inf")
    

    def __repr__(self):
        return f"Square({self.x}, {self.y})"

    def __str__(self):
        return f"Square() x: {self.x}, y: {self.y}, obstacle: {self.obstacle}"



def nearest_neighbor_distance(grid, pos):
    """
    Takes the pos of a node and updates the distance 
    attribute on all of its unchecked neighboring nodes
    that are not obstacles.
    """
    x, y = pos
    current_node = grid[y][x]
    current_distance = current_node.distance
    # vectors from any given node to all its possible neighbors 
    vectors_to_neighbors = ((1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1))
    # Calculate nearest neighbor distance for each neighbor
    for vector in vectors_to_neighbors:
        dx, dy = vector
        new_x, new_y = x + dx, y + dy
        # Check if neighbor exists on the grid
        if new_x >= 0 and new_x < cells_horizontal and new_y >= 0 and new_y < cells_vertical:
            neighbor = grid[new_y][new_x]
            # Unless it is an obstacle or has been visited, update its distance attribute
            if not neighbor.obstacle and not neighbor.visited:
                neighbor.distance = min(neighbor.distance, current_distance + 1)
    
    # Count the current node as visited and update Square.visited to reflect this
    current_node.visited = True
    Square.visited[y][x] = True

def dijkstra(start_node):


def main():

    # Setup the screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Path Finding")

    # Setup the grid
    grid = setup_grid()
    
    # Initialize variables
    end_program = False
    drawing_mode = False
    insert_modes = ("obstacle", "start", "stop", "erase")
    mode = 0 



    # FIX - added temporary start and finish fields
    start_pos = start_x, start_y = (3, 4)
    finish_pos = finish_x, finish_y = (35, 42)

    start = grid[start_y][start_x]
    finish = grid[finish_y][finish_x]
    # set start and finish node settings
    start.start = True
    finish.finish = True 

    start.distance = 0
    start.current = True




    while not end_program:
        for event in pygame.event.get():
            # Check for quit
            if event.type == pygame.QUIT:
                end_program = True

        # Check for a toggle of insert mode
        #print(type(pygame.K_LCTRL)) # returns int: 306
        # print(pygame.key)   
       
        # Display the grid
        display_grid(screen, grid)

        # Check for a toggle of drawing mode 
        if check_drawing_mode_toggle():
            drawing_mode = not drawing_mode            

        # If drawing mode is enabled set the obstacles
        if drawing_mode and insert_modes[mode] == "obstacle":
            set_obstacles(grid)
        
    # End program
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    pygame.init()
    main()
