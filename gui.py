import sys, os, pygame
from go_game import GoGame
from position import Position
from button import Button


class GUI:
    BOARD_PIECE = pygame.image.load("./img/board_piece.png")
    BLACK_PIECE = pygame.image.load("./img/black_piece.png")
    WHITE_PIECE = pygame.image.load("./img/white_piece.png")
    SQUARE_SIZE = BOARD_PIECE.get_width()
    PIECE_SIZE = BLACK_PIECE.get_width()
    BORDER_SIZE = 35
    SIDEMENU_SIZE = 200
    WHITE = (255, 255, 255)
    GREY = (120, 120, 120)
    LIGHTGREY = (150, 150, 150)


    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.font = pygame.font.SysFont("arial", 15)
        self.game = GoGame()
        self.board_size = self.game.goban.size
        self.board_size_on_screen = self.board_size * self.SQUARE_SIZE
        self.screen = pygame.display.set_mode([self.board_size_on_screen + self.SIDEMENU_SIZE,
                                               self.board_size_on_screen])
        pygame.display.set_caption("GoGame")
        self.sidemenu = pygame.Surface((self.SIDEMENU_SIZE, self.screen.get_height())).get_rect(center = ((self.board_size_on_screen +  self.SIDEMENU_SIZE//2),
                                                                                                           self.screen.get_height()//2))
        self.place_stone_sound = pygame.mixer.Sound(os.path.join('sound','goclick.wav'))
        self.create_buttons()

        self.BOARD_PIECE.convert()
        self.BLACK_PIECE.convert()
        self.WHITE_PIECE.convert()

        self.new_game_sound.play()

    def create_buttons(self):
        self.buttons = []
        resign_button = self.create_resign_button()
        self.buttons.append(resign_button)

        new_game_button = self.create_new_game_button()
        self.buttons.append(new_game_button)

        pass_button = self.create_pass_button()
        self.buttons.append(pass_button)

        komi_5_button = self.create_komi_5_button()
        self.buttons.append(komi_5_button)

        komi_6_button = self.create_komi_6_button()
        self.buttons.append(komi_6_button)

    def create_resign_button(self):
        resign_label = "Resign"
        resign_width, resign_height = self.font.size(resign_label)
        surrounding = 10
        resign_sound = pygame.mixer.Sound(os.path.join('sound','goresign.wav'))
        resign_button = Button(resign_label, self.font, self.GREY, self.LIGHTGREY, self.WHITE,
                               resign_width + surrounding, resign_height + surrounding,
                               (self.sidemenu.centerx - (resign_width//2), 310),
                                self.game.resign, resign_sound)
        return resign_button

    def create_new_game_button(self):
        new_game_label = "New Game"
        surrounding = 10
        self.new_game_sound = pygame.mixer.Sound(os.path.join('sound','gonewgame.wav'))
        new_game_width, new_game_height = self.font.size(new_game_label)
        new_game_button = Button(new_game_label, self.font, self.GREY, self.LIGHTGREY, self.WHITE,
                               new_game_width + surrounding, new_game_height + surrounding,
                               (self.sidemenu.centerx - (new_game_width//2), 270),
                                self.new_game, self.new_game_sound)
        return new_game_button

    def create_pass_button(self):
        pass_label = "Pass"
        surrounding = 10
        pass_sound = pygame.mixer.Sound(os.path.join('sound','gopass.wav'))
        pass_width, pass_height = self.font.size(pass_label)
        pass_button = Button(pass_label, self.font, self.GREY, self.LIGHTGREY, self.WHITE,
                               pass_width + surrounding, pass_height + surrounding,
                               (self.sidemenu.centerx - (pass_width//2), 350),
                                self.game.pass_move, pass_sound)
        return pass_button


    def create_komi_5_button(self):
        komi_5_label = "Komi = 5.5"
        surrounding = 10
        komi_5_sound = pygame.mixer.Sound(os.path.join('sound','gokomi.wav'))
        komi_5_width, komi_5_height = self.font.size(komi_5_label)
        komi_5_button = Button(komi_5_label, self.font, self.GREY, self.LIGHTGREY, self.WHITE,
                               komi_5_width + surrounding, komi_5_height + surrounding,
                               (self.sidemenu.centerx - (komi_5_width//2), 390),
                                self.change_komi_5, komi_5_sound)
        return komi_5_button

    def create_komi_6_button(self):
        komi_6_label = "Komi = 6.5"
        surrounding = 10
        komi_6_sound = pygame.mixer.Sound(os.path.join('sound','gokomi.wav'))
        komi_6_width, komi_6_height = self.font.size(komi_6_label)
        komi_6_button = Button(komi_6_label, self.font, self.GREY, self.LIGHTGREY, self.WHITE,
                               komi_6_width + surrounding, komi_6_height + surrounding,
                               (self.sidemenu.centerx - (komi_6_width//2), 430),
                                self.change_komi_6, komi_6_sound)
        return komi_6_button


    def update_buttons(self):
        for button in self.buttons:
            if button.label == "Resign":
                self.buttons.remove(button)

            elif button.label ==  "Pass":
                self.buttons.remove(button)

        new_resign_button = self.create_resign_button()
        new_pass_button = self.create_pass_button()
        self.buttons.append(new_resign_button)
        self.buttons.append(new_pass_button)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                move = self.get_move(position)
                
                if self.inside_board(move) and self.game.running:
                    self.game.make_move(move)
                    self.place_stone_sound.play()

                for button in self.buttons:
                    if button.check_hover(position):
                        button.function()
                        button.play_sound()

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

    def draw(self):
        self.clear_screen()
        self.draw_squares()
        self.draw_borders()
        self.draw_player_pieces()
        self.draw_buttons()
        self.show_score()
        self.show_komi()

        if not self.game.running:
            self.show_winner()

        pygame.display.flip()

    def draw_buttons(self):
        mouse = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse)

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

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def show_score(self):
        self.draw_text("Black's Score:", 150)
        self.draw_text(str(self.game.black_player.score), 170)

        self.draw_text("White's Score:", 200)
        self.draw_text(str(self.game.white_player.score + self.game.komi), 220)

    def show_komi(self):
        self.draw_text("Komi:", 100)
        self.draw_text(str(self.game.komi), 120)

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
        goban_upper_right_corner = (self.board_size_on_screen, 0)
        goban_lower_right_corner = (self.board_size_on_screen, self.board_size_on_screen)

        pygame.draw.line(self.screen, self.GREY, upper_left_corner, upper_right_corner, self.BORDER_SIZE)
        pygame.draw.line(self.screen, self.GREY, upper_left_corner, lower_left_corner, self.BORDER_SIZE)
        pygame.draw.line(self.screen, self.GREY, lower_right_corner, upper_right_corner, self.BORDER_SIZE)
        pygame.draw.line(self.screen, self.GREY, lower_right_corner, lower_left_corner, self.BORDER_SIZE)
        pygame.draw.line(self.screen, self.GREY, goban_upper_right_corner, goban_lower_right_corner, self.BORDER_SIZE)


    def show_winner(self):
        self.draw_text("Winner:", 500)

        if self.game.winner == self.game.black_player:
            winner = "Black"
        elif self.game.winner == self.game.white_player:
            winner = "White"
        else:
            winner = "TIE"

        self.draw_text(winner, 520)

    def change_komi_5(self):
        self.game.komi = 5.5

    def change_komi_6(self):
        self.game.komi = 6.5

    def new_game(self, goban_size=19, komi=6.5):
        self.game = GoGame(goban_size, komi)
        self.update_buttons()


    def get_inner_rectangle(self, position):
        x_coord = position.x * self.SQUARE_SIZE + (self.SQUARE_SIZE - self.PIECE_SIZE) // 2
        y_coord = position.y * self.SQUARE_SIZE + (self.SQUARE_SIZE - self.PIECE_SIZE) // 2
        return pygame.Rect(x_coord, y_coord, self.PIECE_SIZE, self.PIECE_SIZE)

    def get_rectangle(self, position):
        row = position.x * self.SQUARE_SIZE
        col = position.y * self.SQUARE_SIZE
        return pygame.Rect(row, col, self.SQUARE_SIZE, self.SQUARE_SIZE)


GUI = GUI()
while True:
    GUI.handle_events()
    GUI.draw()