import pygame
from pygame.locals import *

pygame.init()

screen_width = 1000
screen_height = 1000
width = 150
height = 150
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# 設定幀率
clock = pygame.time.Clock()
fps = 60

# 載入並縮放圖片
bg_img = pygame.image.load('assets/bg.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

sun_img = pygame.image.load('assets/sun.png')
sun_img = pygame.transform.scale(sun_img, (width, height))

# 遊戲迴圈
run = True
while run:
    clock.tick(fps)

    # 畫背景和太陽
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
