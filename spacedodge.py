import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space dodge")

BG = pygame.transform.scale(pygame.image.load("outerspace.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
STAR_WIDTH, STAR_HEIGHT = 10, 20
PLAYER_VEL = 5
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 50)


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.ellipse(WIN, "white", star)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, 
                         PLAYER_WIDTH, PLAYER_HEIGHT) 
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    
    stars = []  # Initialize empty stars list
    star_add_increment = 2000  # Add new star every 2000 milliseconds
    star_count = 0
    hit = False
    
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Add new stars
        if star_count > star_add_increment:
            for _ in range(3):  # Add 3 stars at a time
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, 
                                 STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_count = 0  # Add this line inside the while loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -=PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)  # Add this line inside the while loop

    pygame.quit()

if __name__ == "__main__":
    main()