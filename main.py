import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()
fps = 60

# 2048 game colour Library
colours = {0: (204, 192, 179),
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
           'light text': (249, 246, 242),
           'dark text': (119, 110, 101),
           'other': (250, 248, 239),
           'bg': (187, 173, 160),
           }

board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score.txt', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high


def draw_over():
    go_bg = pygame.rect.Rect(50, 50, 300, 100)
    rec = pygame.draw.rect(win, "black", go_bg, 0, 10)

    game_over_text = pygame.font.SysFont("Comfortaa-Regular.ttf", 48).render("Game Over", True, colours['light text'])
    game_over_text1 = pygame.font.SysFont("Comfortaa-Regular.ttf", 24).render("Press Enter to Restart", True,
                                                                         colours['light text'])

    text_rect = game_over_text.get_rect(center=(rec.center[0], rec.center[1] - 20))
    text_rect1 = game_over_text1.get_rect(center=(rec.center[0], rec.center[1] + 40))

    win.blit(game_over_text, text_rect)
    win.blit(game_over_text1, text_rect1)


def take_turn(dirc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if dirc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif dirc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True
    elif dirc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift - 1] == board[i][j - shift] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True
    elif dirc == 'RIGHT':
        for i in range(4):
            for j in range(3):
                shift = 0
                for q in range(j + 1):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][2 - j + shift] = board[i][2 - j]
                    board[i][2 - j] = 0
                if 3 - j + shift <= 3:
                    if board[i][2 - j + shift] == board[i][3 - j + shift] and not merged[i][3 - j + shift] \
                            and not merged[i][2 - j + shift]:
                        board[i][3 - j + shift] *= 2
                        score += board[i][3 - j + shift]
                        board[i][2 - j + shift] = 0
                        merged[i][3 - j + shift] = True

    return board, True


def new_piece(board):
    full = False
    count = 0

    while any(0 in row for row in board) and count < 1:

        i, j = random.randint(0, 3), random.randint(0, 3)

        if board[i][j] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[i][j] = 4
            else:
                board[i][j] = 2

    if count < 1:
        full = True

    return board, full


def draw_board():
    pygame.draw.rect(win, colours['bg'], [0, 0, 400, 400], 0, 10)
    score_text = pygame.font.SysFont("freesansbold.ttf", 24).render(f'Score: {score}', True, colours['dark text'])
    high_score_text = pygame.font.SysFont("freesansbold.ttf", 24).render(f'High Score: {high_score}', True,
                                                                         colours['dark text'])
    win.blit(score_text, (20, 420))
    win.blit(high_score_text, (200, 420))


def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_colour = colours['light text']
            else:
                value_colour = colours['dark text']
            if value <= 2048:
                colour = colours[value]
            else:
                colour = colours['other']

            pygame.draw.rect(win, colour, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 10)

            if value > 0:
                value_len = len(str(value))
                font = pygame.font.SysFont("freesansbold.ttf", 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_colour)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                win.blit(value_text, text_rect)
                pygame.draw.rect(win, "black", [j * 95 + 20, i * 95 + 20, 75, 75], 3, 10)


run = True
while run:
    clock.tick(60)
    win.fill('gray')

    draw_board()
    draw_pieces(board_values)

    if spawn_new:
        board_values, game_over = new_piece(board_values)
        game_over = False
        spawn_new = False

    if direction != '':
        board_values, spawn_new = take_turn(direction, board_values)
        direction = ''

    if game_over:
        draw_over()
        if score > high_score:
            high_score = score
            file = open('high_score.txt', 'w')
            file.write(str(high_score))
            file.close()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    game_over = False
                    init_count = 0
                    direction = ''
                    spawn_new = True
                    score = 0

    pygame.display.flip()
