import pygame
import random

pygame.init()
screen = pygame.display.set_mode((580, 781))
pygame.display.set_caption("Racer")

icon = pygame.image.load('Practice_10/racer/images/icon.png')
pygame.display.set_icon(icon)


player_speed = 3
player_x = 30
player_y = 520

enemy_1_list_in_game = []
enemy_2_list_in_game = []
enemy_3_list_in_game = []
coin_list_in_game = []

score = 0

fon = pygame.image.load('Practice_10/racer/images/fon.png')
player = pygame.image.load('Practice_10/racer/images/player.png')
enemy_1 = pygame.image.load('Practice_10/racer/images/enemy_1.png')
enemy_2 = pygame.image.load('Practice_10/racer/images/enemy_2.png')
enemy_3 = pygame.image.load('Practice_10/racer/images/enemy_3.png')
coin = pygame.image.load('Practice_10/racer/images/coin.png')

label = pygame.font.Font('Practice_10/racer/fonts/Font.ttf', 40)
lose_label = label.render('You Lose!', False, (255, 255, 255))
restart_label = label.render('Restart', False, (255, 0, 0))
restart_label_rect = restart_label.get_rect(topleft=(240, 500))

enemy_timer_1 = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer_1, 500)

enemy_timer_2 = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer_2, 1500)

enemy_timer_3 = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer_3, 1900)

coin_timer = pygame.USEREVENT + 4
pygame.time.set_timer(coin_timer, 1200)

running = True
gameplay = True


def spawn_coin():
    attempts = 0
    while attempts < 20:
        x_pos = random.randint(30, 440)
        
        bad_position = False
        
        for el in enemy_1_list_in_game:
            if abs(el.x - x_pos) < 70:   
                bad_position = True
                break
        if bad_position:
            attempts += 1
            continue
            
        for el in enemy_2_list_in_game:
            if abs(el.x - x_pos) < 70:
                bad_position = True
                break
        if bad_position:
            attempts += 1
            continue
            
        for el in enemy_3_list_in_game:
            if abs(el.x - x_pos) < 70:
                bad_position = True
                break
        if bad_position:
            attempts += 1
            continue
            
        coin_list_in_game.append(coin.get_rect(topleft=(x_pos, -50)))
        return

while running:
    screen.blit(fon, (0, 0))

    if gameplay:
        screen.blit(player, (player_x, player_y))
        player_rect = player.get_rect(topleft=(player_x, player_y))
        player_rect.inflate_ip(-40, -40)

        for i, el in enumerate(enemy_1_list_in_game[:]):
            screen.blit(enemy_1, el)
            el.y += 5
            if el.y > 790:
                enemy_1_list_in_game.pop(i)
                continue
            enemy_rect = el.copy()
            enemy_rect.inflate_ip(-40, -40)
            if player_rect.colliderect(enemy_rect):
                gameplay = False

        for i, el in enumerate(enemy_2_list_in_game[:]):
            screen.blit(enemy_2, el)
            el.y += 5
            if el.y > 790:
                enemy_2_list_in_game.pop(i)
                continue
            enemy_rect = el.copy()
            enemy_rect.inflate_ip(-40, -40)
            if player_rect.colliderect(enemy_rect):
                gameplay = False

        for i, el in enumerate(enemy_3_list_in_game[:]):
            screen.blit(enemy_3, el)
            el.y += 5
            if el.y > 790:
                enemy_3_list_in_game.pop(i)
                continue
            enemy_rect = el.copy()
            enemy_rect.inflate_ip(-40, -40)
            if player_rect.colliderect(enemy_rect):
                gameplay = False

        for i, el in enumerate(coin_list_in_game[:]):
            screen.blit(coin, el)
            el.y += 4

            if el.y > 781:
                coin_list_in_game.pop(i)
                continue

            if player_rect.colliderect(el):
                coin_list_in_game.pop(i)
                score += 1
                continue

        score_text = label.render(f"Score: {score}", False, (255, 255, 0))
        screen.blit(score_text, (10, 10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 10:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < 440:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 10:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < 520:
            player_y += player_speed

    else:
        screen.fill((0, 0, 0))
        screen.blit(lose_label, (240, 390))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 30
            player_y = 520
            score = 0
            enemy_1_list_in_game.clear()
            enemy_2_list_in_game.clear()
            enemy_3_list_in_game.clear()
            coin_list_in_game.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == enemy_timer_1:
            enemy_1_list_in_game.append(enemy_1.get_rect(topleft=(30, -400)))

        if event.type == enemy_timer_2:
            enemy_2_list_in_game.append(enemy_2.get_rect(topleft=(230, -1000)))

        if event.type == enemy_timer_3:
            enemy_3_list_in_game.append(enemy_3.get_rect(topleft=(430, -1600)))

        if event.type == coin_timer:
            spawn_coin()        