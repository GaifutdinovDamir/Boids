import pygame
from logic import *


FPS = 30
HUNTERVEL = 2
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Boyds')


def draw_window(bx, by, hunter):
    WIN.fill(BLACK)
    boarder = pygame.Rect(LEFTMARGIN, TOPMARGIN, RIGHTMARGIN - LEFTMARGIN, BOTTOMMARGIN - TOPMARGIN)
    pygame.draw.rect(WIN, WHITE, boarder, 1)
    for x, y in zip(bx, by):
        boid_part = pygame.Rect(x, y, 3, 3)
        pygame.draw.rect(WIN, WHITE, boid_part)
    pygame.draw.rect(WIN, RED, hunter)
    pygame.display.update()

def hunter_move(hunter, keys_pressed):
    if keys_pressed[pygame.K_w]:
        hunter.y -= HUNTERVEL
    elif keys_pressed[pygame.K_s]:
        hunter.y +=  HUNTERVEL
    elif keys_pressed[pygame.K_d]:
        hunter.x += HUNTERVEL
    elif keys_pressed[pygame.K_a]:
        hunter.x -= HUNTERVEL


def main():
    clock = pygame.time.Clock()
    Hunter = pygame.Rect(WIDTH // 2 - 5, HEIGHT // 2 - 5, 10, 10)
    Boids = generate_random_boids(SIZE)
    flock = FLock(Boids, SIZE)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        flock.step(Hunter.x, Hunter.y)
        keys_pressed = pygame.key.get_pressed()
        hunter_move(Hunter, keys_pressed)
        draw_window(flock.get_bx(), flock.get_by(), Hunter)
    for boid in Boids:
        print(boid.vel)
    pygame.quit()
if __name__ == "__main__":
    main()