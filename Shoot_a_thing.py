import pygame
import sys

pygame.init()
pygame.mixer.init()  # 初始化音效模組

# 載入音效檔案（shoot.wav 必須跟 .py 檔在同一資料夾）
shoot_sound = pygame.mixer.Sound("assets/pew.wav")

# 視窗設定
screen = pygame.display.set_mode((640, 480)) 
pygame.display.set_caption("角色射擊 + 音效")

# 顏色
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# 角色與子彈設定
player_x = 300
player_y = 220
player_size = 50
player_speed = 5
bullet_speed = 10
bullets = []

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 發射子彈 + 播放音效
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_rect = pygame.Rect(
                    player_x + player_size,
                    player_y + player_size // 2 - 5,
                    10, 10
                )
                bullets.append(bullet_rect)
                shoot_sound.play()  # 播放砰的聲音！

    # 控制角色移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # 限制角色不出畫面
    player_x = max(0, min(player_x, 640 - player_size))
    player_y = max(0, min(player_y, 480 - player_size))

    # 移動子彈
    for bullet in bullets[:]:
        bullet.x += bullet_speed
        if bullet.x > 640:
            bullets.remove(bullet)

    # 畫角色
    pygame.draw.rect(screen, red, (player_x, player_y, player_size, player_size))

    # 畫子彈
    for bullet in bullets:
        pygame.draw.rect(screen, yellow, bullet)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
