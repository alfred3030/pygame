import pygame
from pygame.locals import *

pygame.init()

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

#define game variadles
tile_size = 50


# 載入並縮放圖片
bg_img = pygame.image.load('assets/img/sky.png')
sun_img = pygame.image.load('assets/img/sun.png')

def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))



class Worls():
      def __init__(self, data):
            
            #load images
            dirt_img = pygame.image.load('assets/img/dirt.png')



world_data = [

]
# 遊戲迴圈
run = True
while run:
      
    # 畫背景和太陽
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
