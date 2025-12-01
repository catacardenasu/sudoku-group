import pygame

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((500, 700))
        running = True
        while running:
            screen.fill("white")
            for i in range(9):
                pygame.draw.line(screen, "black", (i * 32, 0), (i * 32, 512))
            for i in range(9):
                pygame.draw.line(screen, "black", (0, i * 32), (640, i * 32))
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()


