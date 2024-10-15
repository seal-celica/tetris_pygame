import pygame
import random

# スケーリング係数
SCALE_FACTOR = 1.5

# ウィンドウサイズ
BASE_WINDOW_WIDTH = 800
BASE_WINDOW_HEIGHT = 600
WINDOW_WIDTH = int(BASE_WINDOW_WIDTH * SCALE_FACTOR)
WINDOW_HEIGHT = int(BASE_WINDOW_HEIGHT * SCALE_FACTOR)
BASE_BLOCK_SIZE = 30
BLOCK_SIZE = int(BASE_BLOCK_SIZE * SCALE_FACTOR)

# ゲームボードのサイズと位置
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_X = int(100 * SCALE_FACTOR)
BOARD_Y = 0

# 色の定義 (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# テトリミノの定義
TETROMINOS = {
    'I': {'shape': [(0, 0), (1, 0), (2, 0), (3, 0)], 'color': CYAN},
    'O': {'shape': [(0, 0), (1, 0), (0, 1), (1, 1)], 'color': YELLOW},
    'T': {'shape': [(1, 0), (0, 1), (1, 1), (2, 1)], 'color': PURPLE},
    'S': {'shape': [(1, 0), (2, 0), (0, 1), (1, 1)], 'color': GREEN},
    'Z': {'shape': [(0, 0), (1, 0), (1, 1), (2, 1)], 'color': RED},
    'J': {'shape': [(0, 0), (0, 1), (1, 1), (2, 1)], 'color': BLUE},
    'L': {'shape': [(2, 0), (0, 1), (1, 1), (2, 1)], 'color': ORANGE}
}

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")

# フォントの初期化
pygame.font.init()
font = pygame.font.Font(None, int(36 * SCALE_FACTOR))

# ゲーム状態の変数
score = 0
level = 1
lines_cleared_total = 0
paused = False

# グローバル変数として定義
SCALE_FACTOR = 1.5
FONT_SIZE = 36

# ウィンドウサイズと関連する変数を更新する関数（更新版）
def update_sizes():
    global WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE, BOARD_X, font
    WINDOW_WIDTH = int(BASE_WINDOW_WIDTH * SCALE_FACTOR)
    WINDOW_HEIGHT = int(BASE_WINDOW_HEIGHT * SCALE_FACTOR)
    BLOCK_SIZE = int(BASE_BLOCK_SIZE * SCALE_FACTOR)
    BOARD_X = int(100 * SCALE_FACTOR)
    font = pygame.font.Font(None, int(FONT_SIZE * SCALE_FACTOR))
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 初期化時に一度呼び出す
update_sizes()

# ゲームボードの描画
def draw_board(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (BOARD_X + x * BLOCK_SIZE, BOARD_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, GRAY, (BOARD_X + x * BLOCK_SIZE, BOARD_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# テトリミノの描画
def draw_tetromino(tetromino, x, y):
    for block in TETROMINOS[tetromino]['shape']:
        pygame.draw.rect(screen, TETROMINOS[tetromino]['color'],
                         (BOARD_X + (x + block[0]) * BLOCK_SIZE, BOARD_Y + (y + block[1]) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# バッグシステムの実装
def get_bag():
    bag = list(TETROMINOS.keys())
    random.shuffle(bag)
    return bag

# 新しいテトリミノの生成
def new_tetromino():
    global next_tetrominos
    if not tetromino_bag:
        tetromino_bag.extend(get_bag())
    if not next_tetrominos:
        next_tetrominos = [new_tetromino_from_bag() for _ in range(3)]
    next_piece = next_tetrominos.pop(0)
    next_tetrominos.append(new_tetromino_from_bag())
    return next_piece

def new_tetromino_from_bag():
    if not tetromino_bag:
        tetromino_bag.extend(get_bag())
    return tetromino_bag.pop()

# ゲームボードの初期化
board = [[None for _ in range(10)] for _ in range(20)]

# テトリミノバッグの初期化
tetromino_bag = get_bag()

# next_tetrominos の初期化
next_tetrominos = []

# 現在のテトリミノと位置
current_tetromino = new_tetromino()
current_x, current_y = 3, 0

# NEXTピースの描画
def draw_next_pieces():
    for i, piece in enumerate(next_tetrominos):
        for block in TETROMINOS[piece]['shape']:
            pygame.draw.rect(screen, TETROMINOS[piece]['color'],
                             (WINDOW_WIDTH - int(150 * SCALE_FACTOR) + block[0] * BLOCK_SIZE,
                              int(100 * SCALE_FACTOR) + i * int(100 * SCALE_FACTOR) + block[1] * BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE))

# 衝突検出 (修正版)
def check_collision(tetromino, x, y, board, shape=None):
    if shape is None:
        shape = TETROMINOS[tetromino]['shape']
    for block in shape:
        check_x = x + block[0]
        check_y = y + block[1]
        if check_x < 0 or check_x >= 10 or check_y >= 20:
            return True
        if check_y >= 0 and board[check_y][check_x]:
            return True
    return False

# テトリミノを盤面に固定
def place_tetromino(tetromino, x, y, board):
    for block in TETROMINOS[tetromino]['shape']:
        board_x = x + block[0]
        board_y = y + block[1]
        if 0 <= board_x < 10 and 0 <= board_y < 20:  # 盤面の範囲内かチェック
            board[board_y][board_x] = TETROMINOS[tetromino]['color']

# 行が揃っているか確認し、揃っている行を削除
def clear_lines(board):
    lines_cleared = 0
    for y in range(20):
        if all(board[y]):
            del board[y]
            board.insert(0, [None for _ in range(10)])
            lines_cleared += 1
    return lines_cleared

# テトリミノの回転
def rotate_tetromino(tetromino, x, y, board):
    new_shape = [(-block[1], block[0]) for block in TETROMINOS[tetromino]['shape']]
    kicks = [(0, 0), (-1, 0), (1, 0), (0, -1)]  # 基本的な壁蹴りパターン

    for kick_x, kick_y in kicks:
        if not check_collision(tetromino, x + kick_x, y + kick_y, board, shape=new_shape):
            TETROMINOS[tetromino]['shape'] = new_shape
            return x + kick_x, y + kick_y

    return x, y  # 回転できない場合は元の位置を返す

# 落下速度の設定（フレーム数）
FALL_SPEED = 30
fall_counter = 0

# UIの描画
def draw_ui():
    # スコア表示
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (int(20 * SCALE_FACTOR), int(20 * SCALE_FACTOR)))

    # レベル表示
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (int(20 * SCALE_FACTOR), int(60 * SCALE_FACTOR)))

    # 消去したライン数の表示
    lines_text = font.render(f"Lines: {lines_cleared_total}", True, WHITE)
    screen.blit(lines_text, (int(20 * SCALE_FACTOR), int(100 * SCALE_FACTOR)))

    # HOLDの表示
    hold_text = font.render("HOLD", True, WHITE)
    screen.blit(hold_text, (int(20 * SCALE_FACTOR), int(160 * SCALE_FACTOR)))
    if held_tetromino:
        for block in TETROMINOS[held_tetromino]['shape']:
            pygame.draw.rect(screen, TETROMINOS[held_tetromino]['color'],
                             (int(20 * SCALE_FACTOR) + block[0] * BLOCK_SIZE,
                              int(200 * SCALE_FACTOR) + block[1] * BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE))

    # NEXTの表示
    next_text = font.render("NEXT", True, WHITE)
    screen.blit(next_text, (WINDOW_WIDTH - int(150 * SCALE_FACTOR), int(20 * SCALE_FACTOR)))
    draw_next_pieces()

# ポーズ画面の描画（簡略化版）
def draw_pause_screen():
    pause_text = font.render("PAUSED", True, WHITE)
    screen.blit(pause_text, (WINDOW_WIDTH // 2 - pause_text.get_width() // 2, WINDOW_HEIGHT // 2))
    instruction_text = font.render("Press ESC to resume", True, WHITE)
    screen.blit(instruction_text, (WINDOW_WIDTH // 2 - instruction_text.get_width() // 2, WINDOW_HEIGHT // 2 + 50))

# ウィンドウサイズ変更関数
def change_window_size():
    global SCALE_FACTOR
    while True:
        screen.fill(BLACK)
        draw_pause_screen()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    SCALE_FACTOR = min(SCALE_FACTOR + 0.1, 2.0)
                elif event.key == pygame.K_DOWN:
                    SCALE_FACTOR = max(SCALE_FACTOR - 0.1, 1.0)
                elif event.key == pygame.K_ESCAPE:
                    return
                update_sizes()
                break

# フォントサイズ変更関数
def change_font_size():
    global FONT_SIZE
    while True:
        screen.fill(BLACK)
        draw_pause_screen()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    FONT_SIZE = min(FONT_SIZE + 2, 72)
                elif event.key == pygame.K_DOWN:
                    FONT_SIZE = max(FONT_SIZE - 2, 24)
                elif event.key == pygame.K_ESCAPE:
                    return
                update_sizes()
                break

# プレビュー画面の描画
def draw_preview():
    preview_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    preview_surface.fill(BLACK)
    
    # プレビュー用のボードとテトリミノを描画
    preview_board = [[None for _ in range(10)] for _ in range(20)]
    draw_board(preview_board)
    draw_tetromino('T', 3, 0)
    
    # プレビュー用のUIを描画
    preview_ui()
    
    screen.blit(preview_surface, (0, 0))
    pygame.display.flip()
    
    # プレビューを表示し、キー入力を待つ
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        clock.tick(60)

# プレビュー用のUI描画
def preview_ui():
    score_text = font.render("Score: 1000", True, WHITE)
    screen.blit(score_text, (int(20 * SCALE_FACTOR), int(20 * SCALE_FACTOR)))
    
    level_text = font.render("Level: 5", True, WHITE)
    screen.blit(level_text, (int(20 * SCALE_FACTOR), int(60 * SCALE_FACTOR)))
    
    lines_text = font.render("Lines: 50", True, WHITE)
    screen.blit(lines_text, (int(20 * SCALE_FACTOR), int(100 * SCALE_FACTOR)))
    
    hold_text = font.render("HOLD", True, WHITE)
    screen.blit(hold_text, (int(20 * SCALE_FACTOR), int(160 * SCALE_FACTOR)))
    
    next_text = font.render("NEXT", True, WHITE)
    screen.blit(next_text, (WINDOW_WIDTH - int(150 * SCALE_FACTOR), int(20 * SCALE_FACTOR)))

# ゲームオーバー画面
def draw_game_over():
    game_over_text = font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - int(70 * SCALE_FACTOR), WINDOW_HEIGHT // 2 - int(18 * SCALE_FACTOR)))
    pygame.display.flip()
    pygame.time.wait(2000)  # 2秒間表示

# スコア計算
def calculate_score(lines_cleared):
    global score, level, lines_cleared_total
    lines_cleared_total += lines_cleared
    score += lines_cleared * 100 * level
    if lines_cleared_total >= level * 10:
        level += 1

# メインループ（更新版）
running = True
clock = pygame.time.Clock()

held_tetromino = None
can_hold = True

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            elif not paused: # pausedでない場合のみキー入力を受け付ける
                if event.key == pygame.K_LEFT:
                    if not check_collision(current_tetromino, current_x - 1, current_y, board):
                        current_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(current_tetromino, current_x + 1, current_y, board):
                        current_x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(current_tetromino, current_x, current_y + 1, board):
                        current_y += 1
                elif event.key == pygame.K_UP:
                    current_x, current_y = rotate_tetromino(current_tetromino, current_x, current_y, board)
                elif event.key == pygame.K_h:  # 'h' key for hold
                    if can_hold:
                        if held_tetromino is None:
                            held_tetromino = current_tetromino
                            current_tetromino = new_tetromino()
                        else:
                            held_tetromino, current_tetromino = current_tetromino, held_tetromino
                        can_hold = False
                        current_x, current_y = 3, 0  # Reset position


    if not paused:
        # テトリミノの自動落下（速度調整）
        fall_counter += 1
        if fall_counter >= max(FALL_SPEED - (level - 1) * 2, 1):  # レベルに応じて落下速度を上げる
            if not check_collision(current_tetromino, current_x, current_y + 1, board):
                current_y += 1
            else:
                place_tetromino(current_tetromino, current_x, current_y, board)
                lines_cleared = clear_lines(board)
                calculate_score(lines_cleared)
                current_tetromino = new_tetromino()
                current_x, current_y = 3, 0
                can_hold = True
                if check_collision(current_tetromino, current_x, current_y, board):
                    draw_game_over()
                    running = False
            fall_counter = 0

    screen.fill(BLACK)

    if paused:
        draw_pause_screen()
    else:
        draw_board(board)
        draw_tetromino(current_tetromino, current_x, current_y)
        draw_ui()

    pygame.display.flip()

pygame.quit()