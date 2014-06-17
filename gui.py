import pygame
import sys
from go_game import GoGame
from position import Position


BOARD_PIECE = pygame.image.load("./img/board_piece.png")
BLACK_PIECE = pygame.image.load("./img/black_piece.png")
WHITE_PIECE = pygame.image.load("./img/white_piece.png")

BOARD_SIZE = 19
SQUARE_SIZE = BOARD_PIECE.get_width()
PIECE_SIZE = BLACK_PIECE.get_width()

pygame.init()
game = GoGame(BOARD_SIZE)
screen = pygame.display.set_mode([BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE])

def get_inner_rectangle(row, col):
    x_coord, y_coord, width, height = get_rectangle(row, col)
    padding = (SQUARE_SIZE - PIECE_SIZE) // 2
    x_coord += padding
    y_coord += padding
    width = SQUARE_SIZE - padding
    height = SQUARE_SIZE - padding
    return [x_coord, y_coord, width, height]

def get_rectangle(row, col):
    row *= SQUARE_SIZE
    col *= SQUARE_SIZE
    return [row, col, SQUARE_SIZE, SQUARE_SIZE]

def draw_piece(row, col, piece):
    rectangle = get_inner_rectangle(row, col)
    screen.blit(piece, rectangle)

def draw_player_pieces(board):
    for i in range(board.size):
        for j in range(board.size):
            position = Position(i, j)
            if game.goban.at(position) == game.BLACK:
                draw_piece(i, j, BLACK_PIECE)
            elif game.goban.at(position) == game.WHITE:
                draw_piece(i, j, WHITE_PIECE)

def draw_squares(board):
    for i in range(board.size):
        for j in range(board.size):
            rectangle = get_rectangle(i, j)
            screen.blit(BOARD_PIECE, rectangle)

def draw_surface(board):
    screen.blit(GOBAN, [0, 0, BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE])

def draw_board(board):
    draw_squares(board)
    draw_player_pieces(board)
    pygame.display.flip()

def within(point, rectangle):
    x, y = point
    l, t, w, h = rectangle

    return l <= x <= l + w and t <= y <= t + h
 
def square_for(position):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            rectangle = get_inner_rectangle(i, j)
            if within(position, rectangle):
                return Position(i, j)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos()
            square = square_for(position)
            if square is not None:
                game.make_move(square)
    
    draw_board(game.goban)