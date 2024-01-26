import pygame
import os
import pygame_textinput
current_directory = os.getcwd()

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

    def set_font(self, value, size):
        self.__font = pygame.freetype.Font(value, size)

    def set_x(self, value):
        self.__x = value

    def set_y(self, value):
        self.__y = value

    def set_font(self, font, font_size):
        self.__font = pygame.freetype.Font(os.path.join(current_directory,font), font_size)

    def set_all(self , text, colour, font, font_size, x, y):
        self.set_colour(colour)
        self.set_text(text)
        self.set_font(font, font_size)
        self.set_x(x)
        self.set_y(y)


    def draw_text(self, screen):
        text_surface, rect = self.__font.render(self.__text, pygame.Color(self.__colour))
        screen.blit(text_surface, (self.__x, self.__y))




class Button():
    """Creates Buttons that change image when the user mouse postion is over the button"""
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.image_hi = self.brighten_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.hold = False

    def brighten_image(self):
        # Convert image to a copy
        image_copy = self.image.copy()
        brightness_factor = 1.5

        # Iterate through pixels
        for x in range(image_copy.get_width()):
            for y in range(image_copy.get_height()):
                # Get the color of the pixel
                color = image_copy.get_at((x, y))

                # Brighten RGB channels while leaving alpha channel unchanged
                new_color = (
                    min(int(color.r * brightness_factor), 255),
                    min(int(color.g * brightness_factor), 255),
                    min(int(color.b * brightness_factor), 255),
                    color.a
                )

                # Set the new color to the pixel
                image_copy.set_at((x, y), new_color)

        return image_copy


    def draw(self, screen):
        """Returns action and changes self.clicked if the user press the mouse ontop of the image"""
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))
            if pygame.mouse.get_pressed()[2] == 1 and self.clicked == False:
                self.hold = True



        if pygame.mouse.get_pressed()[2] == 0 and self.hold:
            self.clicked = True
            action = True
            self.hold = False
            


        if pygame.mouse.get_pressed()[2] == 0:
            self.clicked = False


        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))

        else:
            screen.blit(self.image, (self.rect.x,self.rect.y))
        return action


class Enter_Text:
    """Text that the user can type into and can be saved"""
    def __init__(self,x,y,font,font_size,anti,text_manger):
        self.font = pygame.font.SysFont(font,font_size)
        self.anti = anti
        self.cords = x, y
        self.textinput = pygame_textinput.TextInputVisualizer(manager=text_manger,font_object=self.font)
        self.textinput.antialias = self.anti
        self.name = ""

    def draw(self,events,screen,rect_x,rect_y,rect_w,rect_h):
        """Draws a box for the user to type in and to contrast with the background"""
        self.textinput.update(events)
        input_rect = pygame.Rect(rect_x,rect_y,rect_w,rect_h)
        colour = pygame.Color("#F5FEFD")
        pygame.draw.rect(screen,colour ,input_rect)
        screen.blit(self.textinput.surface, (self.cords))

    def enter(self,events):
        """If Enter button is clicked it would save the text input"""
        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            self.name = str(self.textinput.value)


    def access(self):
        """Returns the user username"""
        return self.name 

    def clear_text(self):
        """Clears the Current text"""
        self.name = ""
        self.textinput.value = ""