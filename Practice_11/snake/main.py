import pygame
import random
import time

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
yellow = (255, 255, 0)

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


def generate_food(snake_list):
    while True:
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        if [foodx, foody] not in snake_list:
            r = random.random()

            if r < 0.7:
                weight = 1
                color = green
                lifetime = 6
            elif r < 0.9:
                weight = 2
                color = yellow
                lifetime = 5
            else:
                weight = 3
                color = red
                lifetime = 4

            return {
                "x": foodx,
                "y": foody,
                "weight": weight,
                "color": color,
                "spawn_time": time.time(),
                "lifetime": lifetime
            }


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

    food = generate_food(snake_List)

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

        x1 += x1_change
        y1 += y1_change

        if x1 >= dis_width:
            x1 = 0
        elif x1 < 0:
            x1 = dis_width - snake_block

        if y1 >= dis_height:
            y1 = 0
        elif y1 < 0:
            y1 = dis_height - snake_block

        dis.fill(black)

        current_time = time.time()
        time_left = food["lifetime"] - (current_time - food["spawn_time"])

        # если время вышло — новая еда
        if time_left <= 0:
            food = generate_food(snake_List)
        else:
            # мигание за 1 секунду до исчезновения
            if time_left < 1:
                if int(current_time * 10) % 2 == 0:
                    pygame.draw.rect(dis, food["color"], [food["x"], food["y"], snake_block, snake_block])
            else:
                pygame.draw.rect(dis, food["color"], [food["x"], food["y"], snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(score)
        Your_level(level)

        pygame.display.update()

        if x1 == food["x"] and y1 == food["y"]:
            Length_of_snake += 1
            score += food["weight"]
            food = generate_food(snake_List)

            if score // 4 + 1 > level:
                level += 1
                snake_speed += 2

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()