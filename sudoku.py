import pygame
import sys
from sudoku_generator import *
pygame.init()
pygame.mixer.init()

# Window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# backgrounds
welcome_bg = pygame.image.load("background2.jpg")
won_bg = pygame.image.load("background2.jpg")
over_bg = pygame.image.load("background2.jpg")
game_bg = (200, 215, 235)

# Scale the backgrounds
welcome_bg = pygame.transform.scale(welcome_bg, (WIDTH, HEIGHT))
won_bg = pygame.transform.scale(won_bg, (WIDTH, HEIGHT))
over_bg = pygame.transform.scale(over_bg, (WIDTH, HEIGHT))
pygame.mixer.music.load("intense-intense-chase-investigation-music-412316.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Fonts
font_large = pygame.font.SysFont(None, 70)
font_small = pygame.font.SysFont(None, 40)

# Game states
WELCOME = "welcome"
GAME = "game"
WON = "won"
OVER = "over"
state = WELCOME

# Button class
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 165, 0)
        self.text_surface = font_small.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, width=2)
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# welcome buttons
buttons = [
    Button("Easy",   WIDTH//2 - 100, 250, 200, 50),
    Button("Medium", WIDTH//2 - 100, 330, 200, 50),
    Button("Hard",   WIDTH//2 - 100, 410, 200, 50),
]

# buttons for game won / game over screens
exit_button = Button("Exit", WIDTH//2 - 100, 400, 200, 50)
restart_button = Button("Restart", WIDTH//2 - 100, 400, 200, 50)

# buttons for game screen
game_buttons = [
    Button("Reset", WIDTH//2 - 300, HEIGHT - 80, 180, 50),
    Button("Restart", WIDTH//2 - 90, HEIGHT - 80, 180, 50),
    Button("Exit", WIDTH//2 + 120, HEIGHT - 80, 180, 50)
]


board = None
selected_row = 0
selected_col = 0

# Game loop
clock = pygame.time.Clock()

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle clicks depending on the screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if state == WELCOME:
                for b in buttons:
                    if b.is_clicked(mouse_pos):
                        state = GAME  # starts game
                        difficulty = b.text  # stores difficulty
                        board = Board(513, 513, screen, difficulty)

                        selected_row, selected_col = 0,0
                        for r in range(9):
                            for c in range(9):
                                board.cells[r][c].selected = (r == selected_row and c == selected_col)


            if state == GAME:
                for b in game_buttons:
                    if b.is_clicked(mouse_pos):
                        if b.text == "Reset":
                            # RESETS BOARD (ADD THIS)
                            pass
                        elif b.text == "Restart":
                            state = WELCOME
                        elif b.text == "Exit":
                            # exits out the program
                            pygame.quit()

            elif state == WON:
                if exit_button.is_clicked(mouse_pos):
                    state = WELCOME

            elif state == OVER:
                if restart_button.is_clicked(mouse_pos):
                    state = WELCOME
        # Handles keys
        if event.type == pygame.KEYDOWN and state == GAME and board is not None:
            if event.key == pygame.K_LEFT and selected_col > 0:
                selected_col -= 1
            elif event.key == pygame.K_RIGHT and selected_col < 8:
                selected_col += 1
            elif event.key == pygame.K_UP and selected_row > 0:
                selected_row -= 1
            elif event.key == pygame.K_DOWN and selected_row < 8:
                selected_row += 1

            for r in range(9):
                for c in range(9):
                    board.cells[r][c].selected = (r == selected_row and c == selected_col)

    # Draw depending on state
    if state == WELCOME:
        screen.blit(welcome_bg, (0, 0))
        title1 = font_large.render("Welcome to Sodoku", True, (0, 0, 0))
        font_small = pygame.font.SysFont(None, 48)
        title2 = font_small.render("Select Game Mode:", True, (0, 0, 255))
        screen.blit(title1, (WIDTH//2 - title1.get_width()//2, 120))
        screen.blit(title2, (WIDTH//2 - title2.get_width()//2, 120 + title1.get_height() + 10))
        for b in buttons:
            b.draw(screen)

    elif state == GAME:
        screen.fill(game_bg)
        # draw board
        board.draw()


        for r in range(9):
            for c in range(9):
                board.cells[r][c].draw()

        for b in game_buttons:
            b.draw(screen)

    elif state == WON:
        screen.blit(won_bg, (0, 0))
        text = font_large.render("You Won!", True, (0, 0, 0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 100))
        exit_button.draw(screen)

    elif state == OVER:
        screen.blit(over_bg, (0, 0))
        text = font_large.render("Game Over", True, (0, 0, 0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 100))
        restart_button.draw(screen)

    pygame.display.update()
    clock.tick(60)