import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)

dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

snake_block = 10

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)


def Your_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [10, 10])


def Your_level(level):
    value = score_font.render("Level: " + str(level), True, white)
    dis.blit(value, [dis_width - 150, 10])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 4, dis_height / 3])


# Generate food position that is NOT inside the snake
def generate_food(snake_list):
    while True:
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        # Check collision with snake body
        if [foodx, foody] not in snake_list:
            return foodx, foody


def gameLoop():
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    score = 0
    level = 1
    snake_speed = 12

    # Initial food spawn
    foodx, foody = generate_food(snake_List)

    game_over = False
    game_close = False

    restart_rect = pygame.Rect(dis_width // 2 - 80, dis_height // 2 + 40, 160, 50)

    while not game_over:

        while game_close:
            dis.fill(black)

            message("You Lost!", red)
            Your_score(score)
            Your_level(level)

            pygame.draw.rect(dis, white, restart_rect)
            restart_text = font_style.render("Restart", True, black)
            dis.blit(restart_text, (restart_rect.x + 25, restart_rect.y + 10))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        return gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # Prevent instant reverse direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Update position
        x1 += x1_change
        y1 += y1_change

        # Screen wrapping (snake appears on opposite side)
        if x1 >= dis_width:
            x1 = 0
        elif x1 < 0:
            x1 = dis_width - snake_block

        if y1 >= dis_height:
            y1 = 0
        elif y1 < 0:
            y1 = dis_height - snake_block

        dis.fill(black)

        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        # Keep snake length constant unless food is eaten
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check self collision
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(score)
        Your_level(level)

        pygame.display.update()

        # Food collision
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List)

            Length_of_snake += 1
            score += 1

            # Level system: every 4 points → new level
            if score // 4 + 1 > level:
                level += 1
                snake_speed += 2  # Increase difficulty

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()