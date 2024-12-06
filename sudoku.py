import pygame
import sys
import sudoku_generator


# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_WIDTH, GRID_HEIGHT = 450, 450
GRID_X = (WIDTH - GRID_WIDTH) // 2
GRID_Y = (HEIGHT - GRID_HEIGHT) // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PASTEL_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
DARK_BLUE = (50, 100, 200)

# Fonts
pygame.font.init()
TITLE_FONT = pygame.font.Font('PressStart2P-Regular.ttf', 30)
BUTTON_FONT = pygame.font.Font('PressStart2P-Regular.ttf',  15)
CELL_VALUE_FONT = pygame.font.Font('PressStart2P-Regular.ttf',  12)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

        text_surf = BUTTON_FONT.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Buttons
button_width, button_height = 120, 50
button_offset_y = 35
easy_button = Button(WIDTH // 2 - button_width - 100, HEIGHT // 2 + button_offset_y, button_width, button_height, "Easy", "button.png")
medium_button = Button(WIDTH // 2 - button_width // 2, HEIGHT // 2 + button_offset_y, button_width, button_height, "Medium", "button.png")
hard_button = Button(WIDTH // 2 + button_width // 2 + 40, HEIGHT // 2 + button_offset_y, button_width, button_height, "Hard", "button.png")

reset_button = Button(WIDTH // 2 - button_width - 100, GRID_Y + GRID_HEIGHT + 10, button_width, button_height, "Reset", "button.png")
restart_button = Button(WIDTH // 2 - button_width // 2, GRID_Y + GRID_HEIGHT + 10, button_width, button_height, "Restart", "button.png")
exit_button = Button(WIDTH // 2 + button_width // 2 + 40, GRID_Y + GRID_HEIGHT + 10, button_width, button_height, "Exit", "button.png")

# Cell Class
class Cell:
    def __init__(self, value, row, col, screen, cellSize):
        self.value = str(value)
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched = False
        self.cellSize = cellSize

    def set_cell_value(self, value):
        self.sketched = False
        self.value = str(value)

    def set_sketched_value(self, value):
        self.sketched = True
        self.value = str(value)

    def draw(self):
        if(self.value != "0"):
            if self.sketched:
                textColor = GRAY
                num = CELL_VALUE_FONT.render(self.value, False, textColor)
                offset_x = 0
                offset_y = 0
            else:
                textColor = BLACK
                num = CELL_VALUE_FONT.render(self.value, False, textColor)
                offset_x = self.cellSize / 2 - num.get_rect().width / 2
                offset_y = self.cellSize / 2 - num.get_rect().height / 2

            self.screen.blit(num, (self.col + offset_x, self.row + offset_y))

# Board Class
# Difficulty 1 = easy, 2 = medium, 3 = hard
class Board:
    def __init__(self, width, height, screen, difficulty):
        #Constructor for the Board class.
        #screen is a window from PyGame.
        #difficulty is a variable to indicate if the user chose easy medium, or hard.
        self.cell_size = None
        self.cell_list = None
        self.selected_cell = None
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cell_list = [[0 for _ in range(9)] for _ in range(9)]

        cellSize = GRID_WIDTH // 9
        
        # Generates solved sudoku board and starting board
        sudokuGen = sudoku_generator.SudokuGenerator(9, 20 + 10 * difficulty)
        sudokuGen.fill_values()
        self.solution =[row[:] for row in sudokuGen.get_board()]
        pass
        sudokuGen.remove_cells()
        self.startingBoard = sudokuGen.get_board()
        
        # sets up 2d list of cells
        # Format: cell_list[row][column]
        for row in range(height):
            for col in range(width):
                self.cell_list[row][col] = Cell(self.startingBoard[row][col], row * cellSize, col * cellSize, screen, cellSize) 

    def draw(self):
        #Draws an outline of the Sudoku grid, with bold lines to delineate the 3x3 boxes.
        #Draws every cell on this board.
        # draw each cell
        for row in range(self.height):
            for col in range(self.width):
                self.cell_list[row][col].draw()

        # draw grid lines with thicker lines for 3x3 boxes
        cell_size = GRID_WIDTH // 9
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK,
                             (0, i * cell_size),
                             (GRID_WIDTH, i * cell_size),
                             thickness)
            pygame.draw.line(self.screen, BLACK,
                             (i * cell_size, 0),
                             (i * cell_size, GRID_HEIGHT),
                             thickness)

    def select(self, row, col):
        #Marks the cell at (row, col) in the board as the current selected cell.
        #Once a cell has been selected, the user can edit its value or sketched value.
        # deselect previous cell if exists
        if self.selected_cell:
            self.selected_cell = None

        # select new cell
        self.selected_cell = self.cell_list[row][col]
        self.selected_cell.is_selected = True

    def click(self, row, col):
        if (175 <= row <= 625) and (75 <= col <= 525):
            x = ((col - 75) // 50)
            y = ((row - 175) // 50)
            position = (x, y)
            return position
        else:
            return None
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
        #Resets all cells in the board to their original values 
        #(0 if cleared, otherwise the corresponding digit).
        for row in range(self.height):
            for col in range(self.width):
                self.cell_list[row][col].set_cell_value(self.startingBoard[row][col])

    def is_full(self):
        #Returns a Boolean value indicating whether the board is full or not.
        for row in range(self.height):
            for col in range(self.width):
                if(self.cell_list[row][col].value() == "0"):
                    return False
        return True

    def update_board(self):
        pass
        #Updates the underlying 2D board with the values in all cells.

    def find_empty(self):
        pass
        #Finds an empty cell and returns its row and col as a tuple (x,y).

    def check_board(self):
        #Check whether the Sudoku board is solved correctly.
        for row in range(self.height):
            for col in range(self.width):
                if(self.cell_list[row][col].value() == self.solution[row][col]):
                    return False
        return True


# Draw 9x9 Sudoku grid
def draw_grid(surface):
    surface.fill(PASTEL_BLUE)
    cell_size = GRID_WIDTH // 9

    # Draw grid lines
    for i in range(10):
        thickness = 1 if i % 3 != 0 else 3  # Thicker lines for 3x3 subgrids
        pygame.draw.line(surface, BLACK, (0, i * cell_size), (GRID_WIDTH, i * cell_size), thickness)  # Horizontal
        pygame.draw.line(surface, BLACK, (i * cell_size, 0), (i * cell_size, GRID_HEIGHT), thickness)  # Vertical

def launch_grid(difficulty):
    grid_running = True
    grid_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Grid")

    background_image = pygame.image.load("background2.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Create board object
    grid_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
    boardObj = Board(9, 9, grid_surface, difficulty)

    while grid_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        grid_screen.fill(WHITE)
        grid_screen.blit(background_image, (0, 0))

        # draw buttons
        reset_button.draw(grid_screen)
        restart_button.draw(grid_screen)
        exit_button.draw(grid_screen)

        draw_grid(grid_surface)
        boardObj.draw()

#        grid_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))

        # Draw the grid (Sudoku board) onto this surface

        # Blit the grid onto the screen at the specified position
        grid_screen.blit(grid_surface, (GRID_X, GRID_Y))

        pygame.display.flip()

# Game loop
def start_game():
    runningTitle = True
    runningGame = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    difficulty = 1

    while runningTitle: # Title Menu
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        # Title
        title_text = TITLE_FONT.render("Welcome to Sudoku!", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 10))
        screen.blit(title_text, title_rect)

        # Subtitle
        subtitle_text = BUTTON_FONT.render("Select a Game Mode:", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 150))
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
                    launch_grid(1)
                elif medium_button.is_clicked(event.pos):
                    launch_grid(2)
                elif hard_button.is_clicked(event.pos):
                    launch_grid(3)
        
        pygame.display.flip()





# Start the game
start_game()

