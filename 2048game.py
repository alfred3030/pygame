import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 遊戲參數
SIZE = 4
TILE_SIZE = 100
MARGIN = 10
WIDTH = SIZE * TILE_SIZE + (SIZE + 1) * MARGIN
HEIGHT = WIDTH
FONT = pygame.font.SysFont("Arial", 36, bold=True)


BACKGROUND_COLOR = (187, 173, 160)
EMPTY_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}


def new_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board


def add_new_tile(board):
    empty_cells = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if not empty_cells:
        return
    r, c = random.choice(empty_cells)
    board[r][c] = 4 if random.random() < 0.1 else 2


def compress(board):
    new_board = [[0] * SIZE for _ in range(SIZE)]
    for r in range(SIZE):
        pos = 0
        for c in range(SIZE):
            if board[r][c] != 0:
                new_board[r][pos] = board[r][c]
                pos += 1
    return new_board

def merge(board):
    for r in range(SIZE):
        for c in range(SIZE - 1):
            if board[r][c] != 0 and board[r][c] == board[r][c + 1]:
                board[r][c] *= 2
                board[r][c + 1] = 0
    return board

def reverse(board):
    return [row[::-1] for row in board]

def transpose(board):
    return [list(row) for row in zip(*board)]

def move_left(board):
    new_board = compress(board)
    new_board = merge(new_board)
    new_board = compress(new_board)
    return new_board

def move_right(board):
    new_board = reverse(board)
    new_board = move_left(new_board)
    new_board = reverse(new_board)
    return new_board

def move_up(board):
    new_board = transpose(board)
    new_board = move_left(new_board)
    new_board = transpose(new_board)
    return new_board

def move_down(board):
    new_board = transpose(board)
    new_board = move_right(new_board)
    new_board = transpose(new_board)
    return new_board


def can_move(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return True
            if c < SIZE - 1 and board[r][c] == board[r][c + 1]:
                return True
            if r < SIZE - 1 and board[r][c] == board[r + 1][c]:
                return True
    return False


def draw_board(screen, board):
    screen.fill(BACKGROUND_COLOR)
    for r in range(SIZE):
        for c in range(SIZE):
            value = board[r][c]
            rect_x = c * TILE_SIZE + (c + 1) * MARGIN
            rect_y = r * TILE_SIZE + (r + 1) * MARGIN
            pygame.draw.rect(screen, TILE_COLORS.get(value, EMPTY_COLOR), (rect_x, rect_y, TILE_SIZE, TILE_SIZE))
            if value != 0:
                text = FONT.render(str(value), True, (119, 110, 101))
                text_rect = text.get_rect(center=(rect_x + TILE_SIZE // 2, rect_y + TILE_SIZE // 2))
                screen.blit(text, text_rect)
    pygame.display.flip()


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    board = new_board()

    running = True
    while running:
        draw_board(screen, board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                old_board = [row[:] for row in board]
                if event.key == pygame.K_LEFT:
                    board = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    board = move_right(board)
                elif event.key == pygame.K_UP:
                    board = move_up(board)
                elif event.key == pygame.K_DOWN:
                    board = move_down(board)
                if board != old_board:
                    add_new_tile(board)
                if not can_move(board):
                    print("遊戲結束！")
                    running = False
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
