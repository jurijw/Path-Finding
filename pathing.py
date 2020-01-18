import numpy as np
import pygame
import sys

# Constants
size = width, height = (800, 800)
cell_count = cells_horizontal, cells_vertical = (50, 50)
cell_size = cell_width, cell_height = (width // cells_horizontal, height // cells_vertical)

white = (255, 255, 255)
black = (0, 0, 0)

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = x
        self.obstacle = False

    def __repr__(self):
        return f"Square({self.x}, {self.y})"

    def __str__(self):
        return f"Square() x: {self.x}, y: {self.y}, obstacle: {self.obstacle}"


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
            # Set the square color
            square_color = black if square.obstacle else white

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


def main():

    # Setup the screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Path Finding")

    # Setup the grid
    grid = setup_grid()

    # Initialize variables
    drawing_mode = False
    end_program = False
    while not end_program:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_program = True
       
        # Display the grid
        display_grid(screen, grid)

        # Check for a toggle of drawing mode 
        if check_drawing_mode_toggle():
            drawing_mode = not drawing_mode            

        # If drawing mode is enabled get the mouse position
        if drawing_mode:
            x, y = mouse_to_coord()

            # Set the selected squares to be obstacles
            grid[y][x].obstacle = True

    # End program
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    pygame.init()
    main()
