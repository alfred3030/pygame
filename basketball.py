import pygame
import sys
import random
from pygame.math import Vector2

# ---------- 初始化 ----------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("拖曳投籃 - 特效版")
clock = pygame.time.Clock()

# ---------- 球 ----------
ball_start = Vector2(200, 500)
ball_pos = ball_start.copy()
ball_radius = 20
dragging = False
drag_origin = None
velocity = Vector2(0, 0)

GRAVITY = 1
POWER = 0.3

# ---------- 籃框 ----------
hoop_x, hoop_y = 600, 200
hoop_width, hoop_height = 60, 10
rim_thickness = 5
left_rim = pygame.Rect(hoop_x, hoop_y, rim_thickness, hoop_height*4)
right_rim = pygame.Rect(hoop_x + hoop_width - rim_thickness, hoop_y, rim_thickness, hoop_height*4)

# ---------- 草地 ----------
grass = pygame.Rect(0, HEIGHT - 10, WIDTH, 10)

# ---------- 計分 ----------
score = 0
font = pygame.font.SysFont(None, 48)
scored = False

# ---------- 特效 ----------
particles = []
flash_timer = 0
confetti = []
effect_index = 0   # 用來切換特效

def effect_explosion(pos):
    """爆炸粒子"""
    for _ in range(30):
        vel = Vector2(random.uniform(-4, 4), random.uniform(-4, 4))
        particles.append([pos.copy(), vel, 30])

def update_explosion():
    for p in particles[:]:
        p[0] += p[1]
        p[2] -= 1
        pygame.draw.circle(screen, (255, 200, 0), (int(p[0].x), int(p[0].y)), 5)
        if p[2] <= 0:
            particles.remove(p)

def effect_flash(_pos):
    """閃光畫面"""
    global flash_timer
    flash_timer = 20

def update_flash():
    global flash_timer
    if flash_timer > 0:
        if flash_timer % 2 == 0:
            screen.fill((255, 255, 255))
        flash_timer -= 1

def effect_confetti(_pos):
    """彩帶落下"""
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(-100, 0)
        color = random.choice([(255,0,0), (0,255,0), (0,0,255), (255,255,0)])
        confetti.append([x, y, color])

def update_confetti():
    for c in confetti[:]:
        c[1] += 3
        pygame.draw.circle(screen, c[2], (c[0], c[1]), 4)
        if c[1] > HEIGHT:
            confetti.remove(c)

# 特效清單
effect_triggers = [effect_explosion, effect_flash, effect_confetti]
effect_updates  = [update_explosion, update_flash, update_confetti]

# ---------- 拋物線預覽 ----------
def draw_preview(origin, velocity):
    sim_pos = origin.copy()
    sim_vel = velocity.copy()
    for i in range(50):
        sim_pos += sim_vel
        sim_vel.y += GRAVITY
        pygame.draw.circle(screen, (0,0,0), (int(sim_pos.x), int(sim_pos.y)), 3)

# ---------- 重生球 ----------
def reset_ball():
    global ball_pos, velocity, dragging, scored
    ball_pos = ball_start.copy()
    velocity = Vector2(0, 0)
    dragging = False
    scored = False

# ---------- 主迴圈 ----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 拖曳開始
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = Vector2(event.pos)
            if (mouse - ball_pos).length() < ball_radius:
                dragging = True
                drag_origin = ball_pos.copy()

        # 拖曳結束 → 投出
        if event.type == pygame.MOUSEBUTTONUP and dragging:
            mouse = Vector2(event.pos)
            direction = drag_origin - mouse
            velocity = direction * POWER
            dragging = False

    # ---------- 更新球 ----------
    if not dragging:
        ball_pos += velocity
        velocity.y += GRAVITY

        # ---------- 邊界限制 ----------
        # 左右牆反彈
        if ball_pos.x - ball_radius < 0:
            ball_pos.x = ball_radius
            velocity.x *= -0.5
        if ball_pos.x + ball_radius > WIDTH:
            ball_pos.x = WIDTH - ball_radius
            velocity.x *= -0.5
        # 上邊界反彈
        if ball_pos.y - ball_radius < 0:
            ball_pos.y = ball_radius
            velocity.y *= -0.5
        # 下邊界停止
        if ball_pos.y + ball_radius > HEIGHT:
            ball_pos.y = HEIGHT - ball_radius
            velocity.y = 0

    # ---------- 球矩形 ----------
    ball_rect = pygame.Rect(int(ball_pos.x - ball_radius),
                            int(ball_pos.y - ball_radius),
                            ball_radius*2, ball_radius*2)

    # ---------- 碰撞草地 ----------
    if ball_rect.colliderect(grass):
        if velocity.y > 0:
            ball_pos.y = grass.top - ball_radius
            velocity.y = 0

    # ---------- 防止穿透籃框兩側 ----------
    if ball_rect.colliderect(left_rim):
        if velocity.y > 0:
            ball_pos.y = left_rim.top - ball_radius
            velocity.y = 0
    if ball_rect.colliderect(right_rim):
        if velocity.y > 0:
            ball_pos.y = right_rim.top - ball_radius
            velocity.y = 0

    # ---------- 判斷進球 ----------
    if hoop_x + rim_thickness < ball_pos.x < hoop_x + hoop_width - rim_thickness and ball_pos.y > hoop_y:
        if not scored:
            scored = True
            score += 1
            print("進球！")

            # 觸發特效（輪流）
            effect_triggers[effect_index % len(effect_triggers)](ball_pos)
            effect_index += 1

            reset_ball()

    # ---------- 畫面 ----------
    screen.fill((200, 230, 255))

    # 籃框
    pygame.draw.rect(screen, (255,0,0), left_rim)
    pygame.draw.rect(screen, (255,0,0), right_rim)

    # 草地
    pygame.draw.rect(screen, (0,200,0), grass)

    # 球
    pygame.draw.circle(screen, (255,100,0), (int(ball_pos.x), int(ball_pos.y)), ball_radius)

    # 拖曳預覽
    if dragging:
        mouse = Vector2(pygame.mouse.get_pos())
        pygame.draw.line(screen, (0,0,255), drag_origin, mouse, 2)
        direction = drag_origin - mouse
        preview_vel = direction * POWER
        draw_preview(drag_origin, preview_vel)

    # 分數
    score_text = font.render(f"Score: {score}", True, (0,0,0))
    screen.blit(score_text, (20,20))

    # 更新特效
    for updater in effect_updates:
        updater()

    pygame.display.flip()
    clock.tick(60)

