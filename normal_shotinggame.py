import pygame
import sys
import random  # 用於敵人隨機移動

pygame.init()
pygame.mixer.init()

# 音樂設定
pygame.mixer.music.load("assets/bgm.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# 字型與顏色
font = pygame.font.SysFont(None, 28)
text_color = (255, 255, 255)
ready = (255, 0, 0)

# 分數與時間
score = 0
start_time = pygame.time.get_ticks()  # 記錄開始時間

# 射擊冷卻
shoot_cooldown = 12000
last_shot_time = 0

# 音效
shoot_sound = pygame.mixer.Sound("assets/pew.wav")

# 視窗設定
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("EZ pygame")

# 顏色
black = (0, 0, 0)
yellow = (255, 255, 0)

# 角色設定
player_x = 300
player_y = 220
player_speed = 10
player_w = 77
player_h = 96

# 敵人設定
enemy_x = 100
enemy_y = 100
enemy_size = 50
enemy_speed = 3
enemy_dir = random.choice(["up", "down", "left", "right"])
enemy_change_time = pygame.time.get_ticks()
enemy_change_interval = 1000

# 圖片
enemy_img = pygame.image.load("assets/c00lkidd.png").convert_alpha()
player_img = pygame.image.load("assets/chance_flipnote.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_w, player_h))
enemy_img = pygame.transform.scale(enemy_img, (player_w, player_h))

# 子彈
bullet_speed = 10
bullets = []

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(black)

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 發射子彈（Q鍵）
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time >= shoot_cooldown:
                    bullet_rect = pygame.Rect(
                        player_x + player_w,
                        player_y + player_h // 2 - 5,
                        10, 10
                    )
                    bullets.append(bullet_rect)
                    shoot_sound.play()
                    last_shot_time = current_time

    # 敵人移動
    current_time = pygame.time.get_ticks()
    if current_time - enemy_change_time >= enemy_change_interval:
        enemy_dir = random.choice(["up", "down", "left", "right"])
        enemy_change_time = current_time

    if enemy_dir == "up":
        enemy_y -= enemy_speed
    elif enemy_dir == "down":
        enemy_y += enemy_speed
    elif enemy_dir == "left":
        enemy_x -= enemy_speed
    elif enemy_dir == "right":
        enemy_x += enemy_speed

    enemy_x = max(0, min(enemy_x, screen_width - player_w))
    enemy_y = max(0, min(enemy_y, screen_height - player_h))

    # 玩家移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: player_x -= player_speed
    if keys[pygame.K_d]: player_x += player_speed
    if keys[pygame.K_w]: player_y -= player_speed
    if keys[pygame.K_s]: player_y += player_speed

    player_x = max(0, min(player_x, screen_width - player_w))
    player_y = max(0, min(player_y, screen_height - player_h))

    # 子彈移動
    for bullet in bullets[:]:
        bullet.x += bullet_speed
        if bullet.x > screen_width:
            bullets.remove(bullet)
        else:
            # 判斷是否打中敵人
            enemy_rect = pygame.Rect(enemy_x, enemy_y, player_w, player_h)
            if bullet.colliderect(enemy_rect):
                bullets.remove(bullet)
                score += 1
                # 敵人重生在新位置
                enemy_x = random.randint(0, screen_width - player_w)
                enemy_y = random.randint(0, screen_height - player_h)

    # 畫角色與敵人
    screen.blit(player_img, (player_x, player_y))
    screen.blit(enemy_img, (enemy_x, enemy_y))

    # 畫子彈
    for bullet in bullets:
        pygame.draw.rect(screen, yellow, bullet)

    # 冷卻時間顯示
    cooldown_remaining = shoot_cooldown - (pygame.time.get_ticks() - last_shot_time)
    if cooldown_remaining <= 0:
        cooldown_text = font.render("Ready to shoot", True, ready)
    else:
        cooldown_text = font.render(f"Cooldown: {cooldown_remaining} ms", True, text_color)
    screen.blit(cooldown_text, (screen_width - 200, screen_height - 40))

    # 顯示分數
    score_text = font.render(f"Score: {score}", True, text_color)
    screen.blit(score_text, (20, 20))

    # 顯示計時（秒數）
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = font.render(f"Time: {elapsed_time}s", True, text_color)
    screen.blit(timer_text, (screen_width - 120, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
