import numpy as np
import pygame
import sys

# Constants
size = width, height = (800, 800)
cell_count = cells_horizontal, cells_vertical = (15, 15)
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

def display_grid(screen, grid, font, insert_modes, mode):
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
            elif square.visited:
                square_color = blue
            elif square.current:
                square_color = purple

            # Draw the square in the appropriate color
            pygame.draw.rect(screen, square_color, (i * cell_width, j * cell_height, cell_width, cell_height), 0)
            # Draw square outline
            pygame.draw.rect(screen, black, (i * cell_width, j * cell_height, cell_width, cell_height), 1)
    
    # Overlay the current insert mode
    text = font.render(f"Insert mode: {insert_modes[mode]}", True, blue)
    screen.blit(text, (10, 5))

    # Update the display
    pygame.display.update()

def check_user_input():
    """
    Checks for user input and returns a dictionary
    containing information about certain keypresses 
    and whether or not the mouse state has been toggled.
    Returns:
    user_input -> Dict[Bool]
    """
    user_input = {
        "MTOGGLE": False,
        "ENTER": False, 
        "LCTRL": False, 
        "DELETE": False
    }

    # Check system events
    for event in pygame.event.get():
        # Quit if desired
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        # Check for key presses
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                user_input["ENTER"] = True
            elif event.key == pygame.K_LCTRL:
                user_input["LCTRL"] = True
            elif event.key == pygame.K_DELETE:
                user_input["DELETE"] = True

        # If mouse is clicked or released
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            user_input["MTOGGLE"] = True
    
    # Return the dictionary
    return user_input
        

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

def set_start(grid, start_pos_old=None):
    # Get mouse position
    x, y = mouse_to_coord()

    # If another start exists, remove it
    if start_pos_old != None:
        x_old, y_old = start_pos_old
        grid[y_old][x_old].start = False

    # Set the selected square to be the start
    grid[y][x].start = True
    
    # return the new start position
    return (x, y)

def set_finish(grid, finish_pos_old=None):
    # Get mouse position
    x, y = mouse_to_coord()

    # If another finish exists, remove it
    if finish_pos_old != None:
        x_old, y_old = finish_pos_old
        grid[y_old][x_old].finish = False

    # Set the selected square to be the finish
    grid[y][x].finish = True
    
    # return the new finish position
    return (x, y)

def erase(grid):
    # Get mouse position
    x, y = mouse_to_coord()

    # Reset the type of the square
    grid[y][x].reset_type()


class Square:
    # list to keep track of which squares / nodes should be analyzed in 
    # the next iteration of the algorithm 
    up_next = []
    # 2d list to keep track of visited squares /  nodes
    visited = [[False for _ in range(cells_horizontal)] for _ in range(cells_vertical)]

    def __init__(self, x, y):
        # location
        self.x = x
        self.y = y
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

    def reset_type(self):
        # reset square type
        self.obstacle = False
        self.start = False
        self.finish = False

    def add_to_up_next(self):
        Square.up_next.append((self.x, self.y))
    
    @classmethod
    def clear_up_next(cls):
        cls.up_next = []



def update_nearest_neighbors(grid, pos):
    """
    Takes the pos of a node and updates the distance 
    attribute on all of its unvisited neighboring nodes
    that are not obstacles.
    """
    x, y = pos
    node = grid[y][x]
    current_distance = node.distance
    # vectors from any given node to all its possible neighbors 
    vectors_to_neighbors = ((1, 0), (0, -1), (-1, 0), (0, 1))
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
                # Add the neighbor to Square.up_next
                neighbor.add_to_up_next()
    
    # Count the current node as visited and update Square.visited to reflect this
    node.visited = True
    Square.visited[y][x] = True

def dijkstra(screen, grid, start_node_pos, stop_node_pos, font, insert_modes, mode):
    # list to keep track of current nodes
    current_nodes_pos = [start_node_pos]

    finished = False
    while not finished:
        # While the algorithm is not finished, loop through
        # all current nodes and update their neighbors

        # Usually there would have to be a check here to select the
        # unvisited node with the smallest tentative distance but the
        # distance between all nodes is 1 so they will all have an 
        # equal tentative distancd on each iteration
        for node_pos in current_nodes_pos:
            # Set the node to current
            x, y = node_pos 
            node = grid[y][x] 
            node.current = True
            # Update its neighbors
            update_nearest_neighbors(grid, node_pos)

            # Update the screen
            display_grid(screen, grid, font, insert_modes, mode)

            # Change the current nodes current attribute to false
            node.current = False

        # Get the positions of the nodes to be iterated over next
        current_nodes_pos = Square.up_next
        Square.clear_up_next()

        # Check if the target node has been found (i.e it is in the 
        # list of nodes to be analyzed next)
        if stop_node_pos in current_nodes_pos:
            finished = True
        # stop_x, stop_y = stop_node_pos
        # if Square.visited[stop_y][stop_x] == True:
        #     finished = True
            
    


def main():

    # Setup the screen and set font type
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Path Finding")
    font = pygame.font.SysFont("Times New Roman", 30, True)
    
    # Setup the grid
    grid = setup_grid()
    
    # Initialize variables
    end_program = False
    drawing_mode = False
    insert_modes = ("obstacle", "start", "stop", "erase")
    mode = 0 

    start_pos = None
    finish_pos = None

    while not end_program:
        selection_complete = False
        while not selection_complete:
            # Display the grid
            display_grid(screen, grid, font, insert_modes, mode)

            # Get user input
            user_input = check_user_input()

            # Check for a LCTRL keypress 
            if user_input["LCTRL"]:
                # toggle insert mode
                mode = (mode + 1) % len(insert_modes) 
            # Check for a mouse press or release
            if user_input["MTOGGLE"]:
                # toggle drawing mode
                drawing_mode = not drawing_mode   
            # Check for Enter keypress 
            if user_input["ENTER"]:
                print("Start algorithm")
            # Check for Delete keypress 
            if user_input["DELETE"]:
                print("Reset screen")       

            # If drawing mode is enabled set selected squares to appropriate
            # selection.
            if drawing_mode:
                if insert_modes[mode] == "obstacle":
                    set_obstacles(grid)
                elif insert_modes[mode] == "start":
                    start_pos = set_start(grid, start_pos)
                elif insert_modes[mode] == "stop":
                    finish_pos = set_finish(grid, finish_pos)
                elif insert_modes[mode] == "erase":
                    erase(grid)

            # Run the algorithm when Enter key is pressed
            if user_input["ENTER"]:
                selection_complete = True

        dijkstra(screen, grid, start_pos, finish_pos, font, insert_modes, mode)
        
    # End program
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    pygame.init()
    main()
