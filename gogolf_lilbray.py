import pygame

class Text:
    def __init__(self):
        """Creates and display text with differnt fonts and sizes"""
        self.__text = ""
        self.__colour = ""
        self.__font = None
        self.__x = -1
        self.__y = -1

    def set_text(self, value):
        self.__text = value

    def set_colour(self, value):
        self.__colour = value

    def set_font(self, value):
        self.__font = value

    def set_x(self, value):
        self.__x = value

    def set_y(self, value):
        self.__y = value

    def set_font(self, font, font_size):
        self.__font = pygame.font.SysFont(font, font_size)

    def set_all(self , text, colour, font, font_size, x, y):
        self.set_colour(colour)
        self.set_text(text)
        self.set_font(font, font_size)
        self.set_x(x)
        self.set_y(y)


    def draw_text(self, screen):
        text_surface = self.__font.render(self.__text, True, pygame.Color(self.__colour))
        screen.blit(text_surface, (self.__x, self.__y))
