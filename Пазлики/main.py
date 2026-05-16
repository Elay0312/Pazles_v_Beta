import math
import os
import random

import pygame
from pygame.constants import  *
from random import choice, randint
from All_colors import *

pygame.init()

info = pygame.display.Info()
size = (800, 600)
ROWS = 5
COLS = 5
MARGIN = 2
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Пазлики')
BACKGROUND = BLACK
screen.fill(BACKGROUND)
pygame.display.flip()

game_time = 0

def game_over():

    minecraft_font = pygame.font.Font('../minecraft.ttf', 50)
    text = minecraft_font.render('Ура! Ты собрал картинку!', True, GREEN)
    text_rect = text.get_rect()
    text_rect.center = (size[0] // 2, size[1] // 2)
    pygame.draw.rect(screen, BLACK, text_rect.inflate(4, 4))
    screen.blit(text, text_rect)

def draw_swaps():

    minecraft_font = pygame.font.Font('../minecraft.ttf', 32)
    text = minecraft_font.render(f'Количество перестановок: {swaps}', True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (size[0] // 2, size[1] - 20)
    pygame.draw.rect(screen, BLACK, text_rect.inflate(4, 4))
    screen.blit(text, text_rect)

def draw_time():

    minecraft_font = pygame.font.Font('../minecraft.ttf', 32)
    text = minecraft_font.render(f'Время: {game_time // 60}', True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (size[0] // 2, size[1] // 2 + 250)
    pygame.draw.rect(screen, BLACK, text_rect.inflate(4, 4))
    screen.blit(text, text_rect)

def draw_tiles():

    for i in range(len(tiles)):
        tile = tiles[i]
        row = i // ROWS
        col = i % COLS
        x = col * (TILE_WIDTH + MARGIN) + MARGIN
        y = row * (TILE_HEIGHT + MARGIN) + MARGIN

        if i == selected:
            pygame.draw.rect(screen, GREEN, (x - MARGIN, y - MARGIN, TILE_WIDTH + MARGIN * 2, TILE_HEIGHT + MARGIN * 2))

        screen.blit(tile, (x,y))

fps = 60
clock = pygame.time.Clock()
pictures = os.listdir('Images')
picture = random.choice(pictures)
image = pygame.image.load('Images/' + picture)
image_width, image_height = image.get_size()
TILE_WIDTH = image_width // COLS
TILE_HEIGHT = image_height // ROWS

tiles = []
for i in range(ROWS):
    for j in range(COLS):
        rect = pygame.Rect(j *  TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
        tile = image.subsurface(rect)

        tiles.append(tile)

origin_tiles = tiles.copy()

random.shuffle(tiles)

selected = None

swaps = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for i in range(len(tiles)):
                row = i // ROWS
                col = i % COLS
                x = col * (TILE_WIDTH + MARGIN) + MARGIN
                y = row * (TILE_HEIGHT + MARGIN) + MARGIN

                if x <= mouse_x <= x + TILE_WIDTH and y <= mouse_y <= y + TILE_HEIGHT:
                    if selected is not None and selected != i:
                        tiles[i], tiles[selected] = tiles[selected], tiles[i]
                        selected = None

                        swaps += 1

                    elif selected == i:
                        selected = None

                    else:
                        selected = i

    game_time += 1

    # Отрисовка объектов
    screen.fill(BACKGROUND)
    draw_tiles()
    draw_swaps()
    draw_time()
    if tiles == origin_tiles:
        game_over()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()