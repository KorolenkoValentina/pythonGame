

import random
from os import listdir
import pygame 
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
pygame.init()

FPS = pygame.time.Clock()

screen = width, height=800,600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player = player_imgs[1]
player_rect = player.get_rect()
player_speed = 5

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

def create_enemy():
    
    enemy = pygame.image.load('enemy.png').convert_alpha()

    enemy_rect = pygame.Rect(width, random.randint(0, height - enemy.get_height()), *enemy.get_size())
    enemy_speed = random.randint(4, 6)
    return [enemy, enemy_rect, enemy_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

def create_bonus():
   
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(0, width - bonus.get_width()), random.randint(0, height - bonus.get_height()), *bonus.get_size())
    bonus_speed = random.randint(4, 6)
    return [bonus, bonus_rect, bonus_speed]


CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)

img_index = 0
scores = 0
bonuses =[]

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

is_working = True

while is_working:

    FPS.tick(60)
     
    for event in  pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
               img_index = 0
            player = player_imgs[img_index]
    
    
    pressed_keys= pygame.key.get_pressed()

   
    bgX -= bg_speed
    bgX2 -= bg_speed
    if bgX < -bg.get_width():
       bgX = bg.get_width()

    if bgX2 < -bg.get_width():
       bgX2 = bg.get_width() 

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(player, player_rect)

    main_surface.blit(font.render(str(scores), True, RED), (width - 30, 0))
    

    for enemy in  enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
           enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
           is_working= False

    for bonus in  bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1
    

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height :
     player_rect = player_rect.move((0, player_speed))

    if pressed_keys[K_UP] and player_rect.top >= 0:
     player_rect = player_rect.move((0, -player_speed))

    if pressed_keys[K_LEFT] and player_rect.left >= 0:
     player_rect = player_rect.move((-player_speed, 0))

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
     player_rect = player_rect.move((player_speed, 0))
    
    
    pygame.display.flip()

