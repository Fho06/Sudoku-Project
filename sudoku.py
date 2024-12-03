import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
GRID_WIDTH, GRID_HEIGHT = 600, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PASTEL_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
DARK_BLUE = (50, 100, 200)

# Fonts
pygame.font.init()
TITLE_FONT = pygame.font.Font(None, 50)
BUTTON_FONT = pygame.font.Font(None, 36)
CELL_VALUE_FONT = pygame.font.Font(None, 36)

# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)
        pygame.draw.rect(surface, DARK_BLUE, self.rect, 3)  # Border
        text_surf = BUTTON_FONT.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Buttons
button_width, button_height = 120, 50
easy_button = Button(WIDTH // 2 - button_width - 100, HEIGHT // 2, button_width, button_height, "Easy")
medium_button = Button(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height, "Medium")
hard_button = Button(WIDTH // 2 + button_width // 2 + 40, HEIGHT // 2, button_width, button_height, "Hard")

# Cell Class
class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched = False

    def set_cell_value(self, value):
        self.sketched = False
        self.value = value

    def set_sketched_value(self, value):
        self.sketched = True
        self.value = False

    def draw(self):
        if(self.sketched):
            textColor = GRAY
        else:
            textColor = BLACK
    
        self.screen.blit(CELL_VALUE_FONT.render(self.value, False, textColor), (self.row,self.col))

# Board Class
class Board:
    def __init__(self, width, height, screen, difficulty):
        pass
        #Constructor for the Board class.
        #screen is a window from PyGame.
        #difficulty is a variable to indicate if the user chose easy medium, or hard.

    def draw(self):
        pass
        #Draws an outline of the Sudoku grid, with bold lines to delineate the 3x3 boxes.
        #Draws every cell on this board.

    def select(self, row, col):
        pass
        #Marks the cell at (row, col) in the board as the current selected cell.
        #Once a cell has been selected, the user can edit its value or sketched value.

    def click(self, row, col):
        pass
        #If a tuple of (x,y) coordinates is within the displayed board, 
        #this function returns a tuple of the (row, col) of the cell which was clicked. 
        #Otherwise, this function returns None.

    def clear(self):
        pass
        #Clears the value cell. 
        #Note that the user can only remove the cell values and 
        #sketched values that are filled by themselves.

    def sketch(self, value):
        pass
        #Sets the sketched value of the current selected cell equal to the user entered value.
        #It will be displayed at the top left corner of the cell using the draw() function.

    def place_number(self, value):
        pass
        #Sets the value of the current selected cell equal to the user entered value. 
        #Called when the user presses the Enter key.

    def reset_to_original(self):
        pass
        #Resets all cells in the board to their original values 
        #(0 if cleared, otherwise the corresponding digit).

    def is_full(self):
        pass
        #Returns a Boolean value indicating whether the board is full or not.

    def update_board(self):
        pass
        #Updates the underlying 2D board with the values in all cells.

    def find_empty(self):
        pass
        #Finds an empty cell and returns its row and col as a tuple (x,y).

    def check_board(self):
        pass
        #Check whether the Sudoku board is solved correctly.


# Draw 9x9 Sudoku grid
def draw_grid(surface):
    surface.fill(PASTEL_BLUE)
    cell_size = GRID_WIDTH // 9

    # Draw grid lines
    for i in range(10):
        thickness = 1 if i % 3 != 0 else 3  # Thicker lines for 3x3 subgrids
        pygame.draw.line(surface, BLACK, (0, i * cell_size), (GRID_WIDTH, i * cell_size), thickness)  # Horizontal
        pygame.draw.line(surface, BLACK, (i * cell_size, 0), (i * cell_size, GRID_HEIGHT), thickness)  # Vertical

def launch_grid():
    grid_running = True
    grid_screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
    pygame.display.set_caption("Sudoku Grid")
    while grid_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_grid(grid_screen)
        pygame.display.flip()

# Game loop
def start_game():
    running = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    while running:
        screen.fill(WHITE)

        # Title
        title_text = TITLE_FONT.render("Welcome to Sudoku", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Subtitle
        subtitle_text = BUTTON_FONT.render("Select a Game Mode:", True, BLACK)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 50))
        screen.blit(subtitle_text, subtitle_rect)

        # Draw buttons
        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.is_clicked(event.pos):
                    launch_grid()
                elif medium_button.is_clicked(event.pos):
                    launch_grid()
                elif hard_button.is_clicked(event.pos):
                    launch_grid()

        pygame.display.flip()

# Start the game
start_game()
