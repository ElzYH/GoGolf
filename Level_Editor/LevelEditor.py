import pygame
import sys
import math
import os
import numpy 
import pickle

sys.path.append('../GoGolf')
from Logger import *


pygame.init()

# Logger
LOGGER = logging.getLogger(f"{__name__}")
starting_check()

# Game window
SCREEN_HEIGHT = 768 
SCREEN_WIDTH = 1366
LOWER_MARGIN = 100
SIDE_MARGIN = 300

#Grid
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS 
TILE_TYPES = 21

#FPS
FPS = 200
clock = pygame.time.Clock()

#Colours
BLUE = "#2596be"
WHITE = "#F5FEFD"

pygame.key.set_repeat(5, 5)
screen = pygame.display.set_mode(((SCREEN_WIDTH + SIDE_MARGIN), (SCREEN_HEIGHT + LOWER_MARGIN)))
pygame.display.set_caption("GoGolf Level Editor")


# Images
current_directory = os.getcwd()
print(current_directory)

background_img = pygame.image.load('Levels/Level1/bg.png').convert_alpha()
save_img = pygame.image.load(os.path.join(current_directory, 'Assests','save.png')).convert_alpha()
load_img = pygame.image.load(os.path.join(current_directory, 'Assests','load.png')) .convert_alpha()

#Fonts
WII_FONT = os.path.join(current_directory,"Assets", "Fonts", "AOTFShinGoProMedium.otf")

# #Tiles
# tile_list = []
# for x in range(TILE_TYPES):
#     img = pygame.image.load(os.path.join(current_directory, 'Assests', 'tile',f'{x}.png')) 
#     img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
#     tile_list.append(img)



class LevelEditor():
    def __init__(self):
        self.__editor_running = True
        self.__current_level = Level()
        self.__save_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 75, save_img, 1)
        self.__load_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 75, load_img, 1)
        self.__speed_muiltplier = 1
        self.__scroll_left = False
        self.__scroll_right = False


    def __UpdateSpeedMuilplier(self, keys):
        if keys[pygame.K_LSHIFT]:
            self.__speed_muiltplier = 5
        else:
            self.__speed_muiltplier = 1


    def LevelControls(self, keys):
        # Modify background_scroll based on user input or scrolling mechanism
        # For example, you can use the arrow keys:
        
        scroll = self.__current_level.Get_TotalScroll()
        scroll_speed = 5*self.__speed_muiltplier
        if keys[pygame.K_LEFT]:
            if not scroll > (2*TILE_SIZE):
                self.__current_level._UpdateScrollLeft(scroll_speed)
                

        if keys[pygame.K_RIGHT]:
            if abs(scroll) < (MAX_COLS*TILE_SIZE) - SCREEN_WIDTH:
                self.__current_level._UpdateScrollRight(scroll_speed)


    def __DisplayLevelInfomation(self):
        #Text
        text = Text()
        text.set_all(f'Level: {self.__current_level.Get_Level():2}', "Black", WII_FONT, 35, 10 , SCREEN_HEIGHT + LOWER_MARGIN - 90 )
        text.draw_text()
        text.set_text(f'Press Q or E to change level')
        text.set_y(SCREEN_HEIGHT + LOWER_MARGIN - 30)
        text.draw_text()


    def __DrawEditor(self):
        self.__current_level._DrawBackground()
        self.__current_level._DrawWorld()
        self.__current_level._DrawGrid()
        pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))


    def __EventHandler(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                LOGGER.info("Quit Application")
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.__current_level.UpdateSelectedLevel(1)
                if event.key == pygame.K_q:  
                    if not self.__current_level.Get_Level() <= 1: 
                        self.__current_level.UpdateSelectedLevel(-1)

        pygame.display.update()
        clock.tick(FPS)

        #self.__ChangeLevel(event)
    
            
        

    def __ChangeLevel(self, event):
        pass
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_e:
        #         self.__current_level.UpdateSelectedLevel(1)
        #     if event.key == pygame.K_q:  
        #         if not self.__current_level.Get_Level() <= 1: 
        #             self.__current_level.UpdateSelectedLevel(-1)

    
    def Editor(self):
        #self.__current_level._Level__SetupTileButtons()
        
        while self.__editor_running:
            keys = pygame.key.get_pressed()
            self.__UpdateSpeedMuilplier(keys)
            self.LevelControls(keys)
            self.__EventHandler()
            
            self.__DrawEditor()
            
            button_list = self.__current_level.get_button_tile_list()
            self._DrawTileButtons(button_list)
            pygame.draw.rect(screen, WHITE, button_list[self.__current_level.Get_ButtonTileCount()].rect, 3)

            self.__DisplayLevelInfomation()
            self.__current_level.EditorControls()


            if self.__save_button.draw():
                self.__current_level.SaveWorld()

            if self.__load_button.draw():
                self.__current_level.LoadWorld()

            self.__EventHandler()

                


    def _DrawTileButtons(self, button_list):
        #Tile buttons
        #Selecting  a tile
        for i in range(0, TILE_TYPES):
            if button_list[i].draw():
                self.__current_level.set_button_count(i)
            





class Level():
    def __init__(self):
        self.__level_background_img = pygame.image.load('Levels/Level1/bg.png').convert_alpha()
        self.__tiles_background = math.ceil((SCREEN_WIDTH - SIDE_MARGIN) / self.__level_background_img.get_width()) + 1
        self.__background_widith = background_img.get_width()
        self.__background_scroll = 0
        self.__total_scroll = 0 
        self.__world_data = self.__CreateBlankWorld()
        self.__tile_list = self.__CreateTileList()
        self.__level = 0
        self.__button_tile_list = self.__SetupTileButtons()
        self.__button_tile_count = 0

        
    def __SetupTileButtons(self):
        # Make button list
        button_tile_list = []
        button_tile_col = 0
        button_tile_row = 0
        for i in range(0, TILE_TYPES):
            tile_button = Button(
                SCREEN_WIDTH + (75 * button_tile_col) + 50,
                75 * button_tile_row + 50,
                self.__tile_list[i],1)

            button_tile_list.append(tile_button)
            button_tile_col += 1
            if button_tile_col > 2:
                button_tile_col = 0
                button_tile_row += 1
        return button_tile_list



    def __CreateTileList(self):
        tile_list = []
        for x in range(TILE_TYPES):
            img = pygame.image.load(os.path.join(current_directory, 'Assests', 'tile',f'{x}.png')) 
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            tile_list.append(img)

        return tile_list


    def __CreateBlankWorld(self):
        #Create emptylist 2d array
        world_data = [[-1] * 150 for _ in range(16)]
        
        #Ground
        world_data[-1] = [2 for i in world_data[-1]]

        return world_data


    def __ResetBackgroundScroll(self):
        #For going forwards
        if abs(self.__background_scroll) > self.__background_widith:
                self.__background_scroll = 0
                

        #For going backward
        if abs(self.__background_scroll) < self.__background_widith and self.__background_scroll > 0:
            self.__background_scroll = self.__background_scroll - self.__background_widith
            


    def __AddTiles(self, x, y):
        if pygame.mouse.get_pressed()[2] == 1:
            if self.__world_data[y][x] != self.__button_tile_count:
                self.__world_data[y][x] = self.__button_tile_count

    def __RemoveTiles(self, x, y):
        self.__world_data[y][x] = -1


    def _UpdateScrollRight(self, value):
        self.__background_scroll -= value 
        self.__total_scroll -= value 

    def _UpdateScrollLeft(self, value):
        self.__background_scroll += value 
        self.__total_scroll += value 



    def _DrawGrid(self):
        # Vertical lines
        for c in range(-2 ,MAX_COLS + 1):
            pygame.draw.line(screen, WHITE, (c * TILE_SIZE +  self.__total_scroll, 0), (c * TILE_SIZE +  self.__total_scroll, SCREEN_HEIGHT))

        # Horizontal lines
        for c in range(ROWS + 1):
            pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


    #Draw background
    def _DrawBackground(self):
        screen.fill(BLUE)
        for i in range(0, self.__tiles_background):

            screen.blit(self.__level_background_img, (i * self.__background_widith + self.__background_scroll, 0))
        
        self.__ResetBackgroundScroll()



    #Function for drrawing the world tiles dictionary
    def _DrawWorld(self):
        for y, row in enumerate(self.__world_data):
            for x, tile in enumerate(row):
                if tile >= 0: 
                    screen.blit(self.__tile_list[tile], (x * TILE_SIZE + self.__total_scroll, y *TILE_SIZE))


    def EditorControls(self):
        pos = pygame.mouse.get_pos()
        x = (pos[0] - self.__total_scroll) // TILE_SIZE
        y = pos[1] // TILE_SIZE

        #check if cordiantes are in tile area sp mouse clicks are only recorded in game area
        if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
            self.__AddTiles(x,y)

            if pygame.mouse.get_pressed()[0] == 1:
                self.__RemoveTiles(x,y)


    def SaveWorld(self):
        pickle_out = open(f'Levels/level{self.__level}_data', 'wb')
        pickle.dump(self.__world_data, pickle_out)
        pickle_out.close()


    def LoadWorld(self):
        self.__total_scroll = 0
        self.__background_scroll = 0
        self.__world_data = []
        pickle_in = open(f'Levels/level{self.__level}_data', 'rb')
        self.__world_data = pickle.load(pickle_in)
    
    def Get_TotalScroll(self):
        return self.__total_scroll

    def Get_BackgroundScroll(self):
        return self.__background_scroll

    def UpdateSelectedLevel(self, value):
        self.__level += value

    def Get_TileList(self):
        return self.__tile_list

    def Get_ButtonTileCount(self):
        return self.__button_tile_count 

    def Get_Level(self):
        return self.__level

    def get_button_tile_list(self):
        return self.__button_tile_list

    def set_button_tile_list(self, value):
        self.__button_tile_list = value

    def set_button_count(self, value):
        self.__button_tile_count = value



    




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

    def brighten_image(self):
        #Convets iamge to numpy array
        pixel = pygame.surfarray.array3d(self.image)
        #Apply brightness
        pixel = numpy.clip(pixel * 1.5, 0, 255)
        #convert back
        image_hi = pygame.surfarray.make_surface(pixel)
        return image_hi


    def draw(self):
        """Returns action and changes self.clicked if the user press the mouse ontop of the image"""
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))

        else:
            screen.blit(self.image, (self.rect.x,self.rect.y))
        return action


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


    def draw_text(self):
        text_surface = self.__font.render(self.__text, True, pygame.Color(self.__colour))
        screen.blit(text_surface, (self.__x, self.__y))











if __name__ == "__main__":
    LOGGER.info('Hello')
    level_editor = LevelEditor()
    level_editor.Editor()
    