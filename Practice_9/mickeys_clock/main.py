import pygame
import sys
import os
from clock import MickeyClock


os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()


WIDTH, HEIGHT = 1000, 1000 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

WHITE = (255, 255, 255)

try:

    mickey_bg = pygame.image.load("images/mickey_body.png").convert_alpha()

    mickey_bg = pygame.transform.scale(mickey_bg, (WIDTH, HEIGHT))
except Exception as e:
    mickey_bg = None
    print(f"Фон mickey_body.png не найден: {e}")


clock_logic = MickeyClock(screen, (WIDTH // 2, HEIGHT // 2), "images/mickey_hand.png")

clock = pygame.time.Clock()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        

        if mickey_bg:
            screen.blit(mickey_bg, (0, 0))


        clock_logic.update()

        pygame.display.flip()
        

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()