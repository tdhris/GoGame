import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, label, font, default_color, hover_color, text_color, width, height, coordinates, function, sound=None):
        pygame.sprite.Sprite.__init__(self)
        self.label = label
        self.font = font
        self.default_color = default_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.coordinates = coordinates
        self.function = function
        self.sound = sound
        self.is_hover = False
        self.surface = pygame.Surface([width, height])

    def __eq__(self, other):
        return self.label == other.label and self.function == other.function

    @property
    def color(self):
        if self.is_hover:
            return self.hover_color
        else:
            return self.default_color

    def set_function(self, function):
        self.function = function

    def play_sound(self):
        if self.sound is not None:
            self.sound.play()

    def draw(self, screen, mouse):
        self.check_hover(mouse)
        self.surface.fill(self.color)
        screen.blit(self.surface, self.coordinates)
        text_width, text_height = self.font.size(self.label)
        x_padding = (self.surface.get_width() - text_width ) // 2
        y_padding = (self.surface.get_height() - text_height) // 2

        screen.blit(self.font.render(self.label, True, self.text_color), [self.coordinates[0] + x_padding, self.coordinates[1] + y_padding])

    def check_hover(self, mouse):
        mouse_x, mouse_y = mouse
        button_x, button_y = self.coordinates
        x_inside = (mouse_x > button_x) and (mouse_x < button_x + self.surface.get_width())
        y_inside = (mouse_y > button_y) and (mouse_y < button_y + self.surface.get_height())
        self.is_hover = x_inside and y_inside
        return self.is_hover