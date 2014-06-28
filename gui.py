import pygame
import sys
from go_game import GoGame
from position import Position


class GUI:
    BOARD_PIECE = pygame.image.load("./img/board_piece.png")
    BLACK_PIECE = pygame.image.load("./img/black_piece.png")
    WHITE_PIECE = pygame.image.load("./img/white_piece.png")
    SQUARE_SIZE = BOARD_PIECE.get_width()
    PIECE_SIZE = BLACK_PIECE.get_width()
    BORDER_SIZE = 35
    SIDEMENU_SIZE = 200
    WHITE = (255, 255, 255)

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 15)
        self.game = GoGame()
        self.board_size = self.game.goban.size
        self.board_size_on_screen = self.board_size * self.SQUARE_SIZE
        self.screen = pygame.display.set_mode([self.board_size_on_screen + self.SIDEMENU_SIZE,
                                               self.board_size_on_screen])
        pygame.display.set_caption("GoGame")
        self.sidemenu = pygame.Surface((self.SIDEMENU_SIZE, self.screen.get_height())).get_rect(center = ((self.board_size_on_screen +  self.SIDEMENU_SIZE//2), self.screen.get_height()//2))

        self.BOARD_PIECE.convert()
        self.BLACK_PIECE.convert()
        self.WHITE_PIECE.convert()


    def get_inner_rectangle(self, position):
        x_coord = position.x * self.SQUARE_SIZE + (self.SQUARE_SIZE - self.PIECE_SIZE) // 2
        y_coord = position.y * self.SQUARE_SIZE + (self.SQUARE_SIZE - self.PIECE_SIZE) // 2
        return pygame.Rect(x_coord, y_coord, self.PIECE_SIZE, self.PIECE_SIZE)

    def get_rectangle(self, position):
        row = position.x * self.SQUARE_SIZE
        col = position.y * self.SQUARE_SIZE
        return pygame.Rect(row, col, self.SQUARE_SIZE, self.SQUARE_SIZE)

    def draw_piece(self, position, piece):
        rectangle = self.get_inner_rectangle(position)
        self.screen.blit(piece, rectangle)

    def draw_player_pieces(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                position = Position(i, j)
                
                if self.game.goban.at(position) == self.game.BLACK:
                    self.draw_piece(position, self.BLACK_PIECE)
                
                elif self.game.goban.at(position) == self.game.WHITE:
                    self.draw_piece(position, self.WHITE_PIECE)

    def draw_squares(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                position = Position(i, j)
                rectangle = self.get_rectangle(position)
                self.screen.blit(self.BOARD_PIECE, rectangle)

    def draw(self):
        self.clear_screen()
        self.draw_squares()
        self.draw_borders()
        self.draw_player_pieces()
        self.show_score()
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def show_score(self):
        self.draw_text("Black's Captured Stones:", 150)
        self.draw_text(str(self.game.black_player.captured_stones_count), 170)

        self.draw_text("White's Captured Stones:", 250)
        self.draw_text(str(self.game.white_player.captured_stones_count), 270)

    def draw_text(self, text, coord_y):
        rendered_text = self.font.render(text, True, self.WHITE)
        text_rect = rendered_text.get_rect()
        text_rect.centerx = self.sidemenu.centerx
        text_rect.centery = coord_y
        self.screen.blit(rendered_text, text_rect)

    def draw_borders(self):
        upper_left_corner = (0, 0)
        upper_right_corner = (self.screen.get_width(), 0)
        lower_left_corner = (0, self.screen.get_height())
        lower_right_corner = (self.screen.get_width(), self.screen.get_height())
        goban_upper_right_corner = (self.board_size_on_screen - 35, 0)
        goban_upper_right_corner = (self.board_size_on_screen - 35, self.board_size_on_screen)

        pygame.draw.line(self.screen, self.WHITE, upper_left_corner, upper_right_corner, self.BORDER_SIZE)
        pygame.draw.line(self.screen, self.WHITE, upper_left_corner, lower_left_corner, self.BORDER_SIZE)
        pygame.draw.line(self.screen, self.WHITE, lower_right_corner, upper_right_corner, self.BORDER_SIZE)
        pygame.draw.line(self.screen, self.WHITE, lower_right_corner, lower_left_corner, self.BORDER_SIZE)
        pygame.draw.line(self.screen, self.WHITE, goban_upper_right_corner, goban_upper_right_corner, self.BORDER_SIZE)

    def within(self, point, rectangle):
        rect = pygame.Rect(rectangle)
        return rect.collidepoint(point)
     
    def get_move(self, position):
        for i in range(self.board_size):
            for j in range(self.board_size):
                move = Position(i, j)
                rectangle = self.get_inner_rectangle(move)
                if self.within(position, rectangle):
                    return move

    def inside_board(self, move):
        return move is not None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                move = self.get_move(position)
                
                if self.inside_board(move):
                    self.game.make_move(move)


GUI = GUI()
while True:
    GUI.handle_events()
    GUI.draw()