import pygame
import sys
from sudoku_generator import *
pygame.init()

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

            elif state == GAME:
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