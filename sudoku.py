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

# Draw 9x9 Sudoku grid
def draw_grid(surface):
    surface.fill(PASTEL_BLUE)
    cell_size = GRID_WIDTH // 9

    # Draw grid lines
    for i in range(10):
        thickness = 1 if i % 3 != 0 else 3  # Thicker lines for 3x3 subgrids
        pygame.draw.line(surface, BLACK, (0, i * cell_size), (GRID_WIDTH, i * cell_size), thickness)  # Horizontal
        pygame.draw.line(surface, BLACK, (i * cell_size, 0), (i * cell_size, GRID_HEIGHT), thickness)  # Vertical

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
                    draw_grid()
                elif medium_button.is_clicked(event.pos):
                    draw_grid()
                elif hard_button.is_clicked(event.pos):
                    draw_grid()

        pygame.display.flip()

# Start the game
start_game()
