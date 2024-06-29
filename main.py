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


def take_turn(dirc, board):
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
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif dirc == 'DOWN':
        board = move_down(board)
    elif dirc == 'LEFT':
        board = move_left(board)
    elif dirc == 'RIGHT':
        board = move_right(board)

    return board


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
spawn_new = True
direction = ''
while run:
    clock.tick(fps)
    win.fill('gray')

    draw_board()
    draw_pieces(board_values)

    if spawn_new:
        board_values, game_over = new_piece(board_values)
        spawn_new = False

    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''

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

    pygame.display.flip()
