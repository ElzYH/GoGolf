import pygame
import logging
from math import ceil, degrees, sqrt, cos, atan2, sin
import sys
import pickle
import gogolf_lilbray
import sqlite3
from random import randint
import numpy as np
import pandas as pd
import openpyxl 

#pygame.init()

LOGGER = logging.getLogger(f"{__name__}")

#Create display window
SCREEN_HEIGHT = 768 
SCREEN_WIDTH = 1366
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


#FPS
clock = pygame.time.Clock()
FPS = 60 #100

pygame.display.set_caption("Go Golf")
#icon = pygame.image.load('Assets/uno_icon.ico')
#pygame.display.set_icon(icon)
pygame.key.set_repeat(0,0)

#Load Images

GOLFBALL_IMG = pygame.image.load('Assests/white_ball.png')


#Image Widiths and Heights
background_1 = pygame.image.load('Background_Img/1.png').convert_alpha()
background_2 = pygame.image.load('Background_Img/2.png').convert_alpha()
background_3 = pygame.image.load('Background_Img/4.png').convert_alpha()


GOLFBALL_WIDITH = GOLFBALL_IMG.get_width()
GOLFBALL_HEIGHT = GOLFBALL_IMG.get_height()


#Colours
BLUE = "#2596be"
WHITE = "#F5FEFD"
ORANGE = "#edc9af"

#Fonts
WII_FONT = "Assests/Fonts/AOTFShinGoProMedium.otf"
P2 = "Assests/Fonts/Retro Gaming.ttf"

#Grid
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS 
TILE_TYPES = 21


class GoGolf():
    def __init__(self, username, level, random, BALL_SKIN):
        self.__game_running = True #is the game running
        self.__current_player = Player(username, BALL_SKIN) #Current player
        self.__currentlevel = Level(1) #Current level
        self.__muitplier = 1.5 #Muilplier
        self.__distance_moved = 0 #Distance moved from the start
        self.__world = World()
        self.__player_text = gogolf_lilbray.Text()
        self.__count = -10  #Offset
        self.__random = random #If the game should select levels at random
        self.__world_queue = self.__create_world_queue(level)
        self.__skin_of_golfball = BALL_SKIN #Colour of ball
        self.ticks = ticks_data = [] #Test FPS by addding all recored Frame rates to list

    def __create_world_queue(self, level):
        """Creates a Queue that hold each level"""
        
        worlds = gogolf_lilbray.queue(level) #Holds a queue of each level loaded
        for i in range(level):
            
            if self.__random:
                #Picks a random level
                pickle_in = open(f'Levels/level{randint(1, 7)}_data', 'rb')

            else:
                #Finds the level
                pickle_in = open(f'Levels/level{i+1}_data', 'rb')
    
            #Load the level 
            worlds.enqueue(pickle.load(pickle_in))

        return worlds

    def __UI_playerinfo(self):
        """Displays UI elements such as amount of strokes and
        score"""

        self.__player_text.set_all(f"Strokes: {self.__current_player.get_strokes():3}", ORANGE, P2, 22, SCREEN_WIDTH - 167, SCREEN_HEIGHT - 30)
        self.__player_text.draw_text(screen)
        self.__player_text.set_text(f"Time: {str(self.__current_player.get_time()//60).zfill(2):1}:{str(self.__current_player.get_time() % 60).zfill(2):1}")
        self.__player_text.set_y(10)
        self.__player_text.draw_text(screen)

    def __prepare_next_level(self):
        """Reset level conditions and changes the current level"""

        self.__current_player.score_calculator(len(self.__world.get_goal_list()))
        self.__current_player.reset()
        self.__world = World()
        self.__current_player.new_ball(self.__skin_of_golfball)
        self.__currentlevel.set_World_data([])
        self.__currentlevel.next_level(1)

    def __change_level(self):
        """Proccess new data for the new level and reset level postions"""

        self.__world.proccess_data(self.__currentlevel.get_world_data(), self.__currentlevel.get_block_list(), self.__current_player.get_golfball())
        self.__current_player.get_golfball().set_spawn_location(self.__world.get_spawn_location())
        self.__current_player.get_golfball().set_ball_postion(self.__world.get_spawn_location()[0] + self.__distance_moved, self.__world.get_spawn_location()[1])
        self.__currentlevel.set_control_background(True)


    def __timer(self):
        """Timer that uses FPS as timer, meaning timer is linked
        to the game and not the computer"""

        self.__count += 1
        if self.__count > clock.get_fps():
            self.__current_player.add_to_time(1)
            self.__count = 0

    def __coin_update(self, value):
        conn = sqlite3.connect("database/GoGolfDB.db")
        c = conn.cursor()

        #Finds the amount of coins and the AccountID for that user
        c.execute("""SELECT Player_Skins.Coins, Player_Skins.AccountID
            FROM Player_Skins INNER JOIN Users
            ON Player_Skins.AccountID = Users.AccountID
            WHERE Users.Username = ?""", (self.__current_player.get_username(),))
        AccountID = c.fetchone()

        c.execute("UPDATE Player_Skins SET Coins = ? WHERE AccountID = ?",
                  (AccountID[0] + 16 * value, AccountID[1]))

        conn.commit()
        conn.close()

        


    def __save_game_records(self, level):
        """Records game results"""

        if level not in (3, 5):
            raise ValueError(f"Invalid level {level}")

        conn = sqlite3.connect("database/GoGolfDB.db")
        c = conn.cursor()

        #Finds the UserID
        c.execute("SELECT UserID FROM Users WHERE Username = ?",
                  (self.__current_player.get_username(),))
        UserID = c.fetchone()

        #Inserts Data to the game DB
        c.execute(f"INSERT INTO Holes{level} (UserID, Score, Strokes, Time) VALUES (?, ?, ?, ?)",
                  (UserID[0],
                   self.__current_player.get_total_score(),
                   self.__current_player.get_total_stokes(),
                   self.__current_player.get_total_time()))

        conn.commit()
        conn.close()


    def __is_level_completed(self, level):
        """Checks to either to load level or
        to save user data"""

        if self.__world.level_completed():
            self.__prepare_next_level()

            #Checks if the current level exceeds the amount of levels for the gamemode
            if not self.__currentlevel.get_level() > level:
                self.LoadWorld()
                self.__change_level()
            else:
                #Game does not save random gamemode results
                if not self.__random:
                    self.__save_game_records(level)
                self.__coin_update(level)
                self.__scoreboard()
                self.__game_running = False

        
    def __scoreboard(self):
        """Displays end of game results """

        self.__currentlevel.set_scroll_background(2000) #Still loaded on the level however far away from the level platforms
        time = 5
        count = 0
        x_pos = -300
        game_result = gogolf_lilbray.Text()

        #Time Limit For Scoreboard
        while time < 15:
            count += 1
            if count > clock.get_fps():
                self.__current_player.add_to_time(1)
                count = 0
                time+=1
            
            self.__currentlevel.create_background()
            self.__currentlevel.set_scroll_background(self.__currentlevel.get_scroll_background() + 5)

            #Draws and moves texts accross the screen
            x_pos +=2
            game_result.set_all(f"Score: {self.__current_player.get_total_score()}", "#ff8500", P2, 30, x_pos, 200)
            game_result.draw_text(screen)
            game_result.set_all(f"Strokes: {self.__current_player.get_total_stokes()}", "#ff8500", P2, 30, x_pos, 400)
            game_result.draw_text(screen)
            game_result.set_all(f"Time: {str(self.__current_player.get_total_time()//60).zfill(2):1}:{str(self.__current_player.get_total_time() % 60).zfill(2):1}", "#ff8500", P2, 30, x_pos , 600)
            game_result.draw_text(screen)
            self.EventHandler()
            



    def PlayGame(self, level):
        """Main Game Loop """

        #Load first level
        self.LoadWorld()
        self.__world.proccess_data(self.__currentlevel.get_world_data(), self.__currentlevel.get_block_list(), self.__current_player.get_golfball())
        #Sets spawn location
        self.__current_player.get_golfball().set_spawn_location(self.__world.get_spawn_location())
        
        while self.__game_running:

            self.__timer()
            self.__is_level_completed(level)
            self.__currentlevel.create_background()

            #Before the player sets up the shot
            if self.__currentlevel.get_control_backgorund():

                self.level_controls() #Can control the camera
                self.__current_player.get_golfball().display_ball()
                self.__world.draw(self.__distance_moved)
                if not self.__currentlevel.get_control_backgorund():
                    self.set_camera_pos() 
                    
            #Player wants to shoot
            else:
                self.__world.draw(self.__distance_moved)
                self.player_can_shoot(self.__current_player)
                self.__current_player.get_golfball().display_ball()
                self.__player_text.draw_text(screen)

                #If the player does not want to take the shot anymore
                if self.__current_player.get_golfball().get_stop(): #Checks the player wants to stop wanting to shoot
                    self.__current_player.get_golfball().set_stop(False)

                    #Activates the control of the camera again
                    self.__currentlevel.set_control_background(True) 
                    self.__current_player.get_golfball().set_clicked(False)

            #If the player shot
            if  self.__current_player.get_golfball().get_clicked():
                self.__current_player.get_golfball().display_ball()
                self.__world.draw(self.__distance_moved)
                self.__player_text.draw_text(screen)

            self.__UI_playerinfo()
            self.EventHandler()

        
    def EventHandler(self):
        """Event Handler """
 
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                LOGGER.info("Quit Application")

                #temp #Test FPS
                data = {'Ticks': ticks_data}
                df = pd.DataFrame(data, index=range(len(self.ticks)))  # Specify index as a range
                df.to_excel('ticks_data.xlsx', index=False)
                #Test FPS


                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    #temp #Test FPS
                    data = {'Ticks': self.ticks}
                    df = pd.DataFrame(data, index=range(len(self.ticks)))  #Specify index as a range
                    df.to_excel('ticks_data.xlsx', index=False)
                    #Test FPS

                    self.__game_running = False

        pygame.display.update()
        clock.tick(FPS)
        self.ticks.append(clock.get_fps()) #Test FPS




    def update_camera_postion(self):
        """Follows the ball in the air """

        player_ball = self.__current_player.get_golfball()
        ball_postion = player_ball.get_postion_of_ball()
        speed_movement = player_ball.get_x_velocityofball()//115 #120
        self.__muitplier = 2.7
        
        #Forwards movement
        if ball_postion[0] > self.__currentlevel.get_threshold_left() and self.__current_player.get_golfball().get_direction() == 1:               

            offset_x = self.__muitplier * speed_movement
            self.__currentlevel.update_scroll_right(offset_x)
            player_ball.update_ball_to_right(offset_x)
            self.__distance_moved -= offset_x

        #Backwards movement
        elif ball_postion[0] < self.__currentlevel.get_threshold_right() and self.__current_player.get_golfball().get_direction() == -1:

            offset_x = self.__muitplier * speed_movement
            self.__currentlevel.update_scroll_right(offset_x)
            player_ball.update_ball_to_right(offset_x)
            self.__distance_moved -= offset_x



    def set_camera_pos(self):
        """Centers the ball in middle of the screen """

        golfball = self.__current_player.get_golfball()
        golfball_x_pos = golfball.get_postion_of_ball()[0]

        LOGGER.info(f"golfball x pos before {golfball_x_pos} ")
        LOGGER.info(f"Scroll Before {self.__currentlevel.get_scroll_background()}")

        #Calculate the offset to center the golf ball on the screen
        offset_x = -(golfball.get_postion_of_ball()[0] - SCREEN_WIDTH // 2) + self.__distance_moved 
        offset_y = golfball.get_postion_of_ball()[1]

        LOGGER.info(f"Distance camera from ball x of camera is {self.__distance_moved} ")
        LOGGER.info(f"Offset x of camera is {offset_x} ")

        #Center the golf ball on the screen
        golfball.set_ball_postion(SCREEN_WIDTH//2 , offset_y)
        
        #Update the background scroll to center the camera on the golf ball
        self.__currentlevel.set_scroll_background(offset_x)

        self.__distance_moved = (offset_x)
        LOGGER.info(f"golfball x pos after {golfball_x_pos} ")
        LOGGER.info(f"Scroll after {self.__currentlevel.get_scroll_background()}")


    def player_can_shoot(self, player):
        """Everything to do with stroke attempt """

        player_ball = self.__current_player.get_golfball()
        
        #If player wants to set up a new shot
        if not self.__currentlevel.get_control_backgorund():

        
            if pygame.mouse.get_pressed()[0] and not player_ball.get_clicked():
                self.__currentlevel.set_control_background(True)
                


            #Let player set up the shot and shoot it
            if not player_ball.get_clicked():
                player_ball.aim(player)
                player_ball.swing()

            #While ball is not stoped 
            if not player_ball.get_stop():
                player_ball.trajecotry(self.__world.get_obstacle_list(), self.__distance_moved, self.__current_player)
                if player_ball.get_clicked():
                    self.update_camera_postion()



    def level_controls(self):
        """Level control for scrolling left and right, ready to shoot and a muitlplier
        to move faster """
        
        if self.__currentlevel.get_control_backgorund():

            keys = pygame.key.get_pressed()
            spped_muiltplayer = 1

            #Muiltplier
            if keys[pygame.K_LSHIFT]:
                spped_muiltplayer = 5
                
            speed = 5*spped_muiltplayer

            #PLayer moves to the right
            if keys[pygame.K_d] and abs(self.__distance_moved)//TILE_SIZE < 150:
                self.__currentlevel.update_scroll_right(speed)
                self.__current_player.get_golfball().update_ball_to_right(speed)
                self.__distance_moved -= speed

            #PLayer moves to the left
            if keys[pygame.K_a] and self.__distance_moved //TILE_SIZE < 2:
                self.__currentlevel.update_scroll_left(speed)
                self.__current_player.get_golfball().update_ball_to_left(speed)
                self.__distance_moved += speed

            #Player ready to swing
            if keys[pygame.K_RETURN]:
                self.__currentlevel.set_control_background(False)



    def LoadWorld(self):
        """Load selected level world"""

        #Create empty world /2d array
        world_data = [[-1] * 150 for _ in range(16)]

        LOGGER.info("Save Level")

        #Finds the level
        level_in = self.__world_queue.dequeue()

        #Reset World
        self.__currentlevel.set_scroll_background(0)
        self.__currentlevel.set_World_data(world_data)

        #Load the level 
        self.__currentlevel.set_World_data(level_in)
        LOGGER.info(f"Level {self.__currentlevel.get_level()} has been loaded ")



class World():
    def __init__(self):
        self.obstacle_list = [] #All tile/blocks in the wrold
        self.__ball_spawn_location = [0, 0]
        self.__goals_list = []

    def proccess_data(self, world_data, tile_img_list, golfball):
        """Proccess the world data and gives all tiles it own properties"""

        for y, row in enumerate(world_data):
            for x, block in enumerate(row):
                if block >= 0:
                    img = tile_img_list[block]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)

                    #Normal Block
                    if block <= 7 or block >= 12 and block <= 17:
                        tile_data = Tile(img, img_rect, x, y, "obstacle")
                        self.obstacle_list.append(tile_data)
                    
                    #Water Block
                    elif block >= 8 and block <= 11:
                        tile_data = Water(img, img_rect, x, y, "water")
                        self.obstacle_list.append(tile_data)

                    #Goal Block
                    elif block >= 18 and block <= 19:
                        tile_data = Goal(img, img_rect, x, y, "goal")
                        self.obstacle_list.append(tile_data)
                        self.__goals_list.append(tile_data)

                    #Golfball Postion
                    elif block == 20:
                        golfball.set_ball_postion(x*TILE_SIZE, y*TILE_SIZE + 28)
                        self.__ball_spawn_location = (x*TILE_SIZE, y*TILE_SIZE + 28)


    def draw(self, distance_moved):
        """Draws game tile """

        #Turns the level block/tile location back to pygame coords in numpy array
        x_coordinates = np.array([block.get_rect().x // TILE_SIZE for block in self.obstacle_list]) 

        #Checks for blocks that range in coords that would be dispalyed on screen at that time 
        mask = (x_coordinates * TILE_SIZE + distance_moved >= -TILE_SIZE) & (x_coordinates * TILE_SIZE + distance_moved <= SCREEN_WIDTH + TILE_SIZE)
        visible_blocks = np.array(self.obstacle_list)[mask]

        #Renders the visbale blocks
        for block in visible_blocks:
            temp = block.get_rect().x
            screen.blit(block.get_img(), (temp + distance_moved, block.get_rect().y))
            if block.get_block_type() == "goal":
                block.Display_Goal(distance_moved)


    def level_completed(self):
        """Checks if all goals have been hit"""

        holes = 0 #Holes starts at zero because every level should have one or more holes
        for goal in self.__goals_list:
            if not goal.get_goal_active():
                holes += 1 #Adds everyhole that been entered 

        if holes == len(self.__goals_list):
            return True #If the holes enteted is same amount as goals then the level is completed
        return False

                
    def get_obstacle_list(self):
        return self.obstacle_list

    def get_goal_list(self):
        return self.__goals_list

    def get_spawn_location(self):
        return self.__ball_spawn_location

                        

class Tile():
    def __init__(self, img, img_rect, x, y, img_type):
        self.__img = img #Tile Image
        self.__rect = img_rect #Tile Rectangle
        self.__rect.midtop = (x + TILE_SIZE //2, y + (TILE_SIZE - self.__img.get_height())) #Changes midtop postion
        self.__rect.x = x * TILE_SIZE #Tile Rectangle x postion
        self.__rect.y = y * TILE_SIZE #Tile Rectangle y postion
        self.__type = img_type #Image Type

    def get_img(self):
        return self.__img

    def get_rect(self):
        return self.__rect

    def get_block_type(self):
        return self.__type

    def set_rectx(self ,v):
        self.__rect.x = v

    def set_recty(self, v):
        self.__rect.y = v

    def set_rect(self, distnace):
        self.__rect.x += distnace



class Water(Tile):
    def __init__(self, img, img_rect, x, y, img_type):
        super().__init__(img, img_rect, x, y, img_type)



class Goal(Tile):
    def __init__(self, img, img_rect, x, y, img_type):
        super().__init__(img, img_rect, x, y, img_type)
        self._goal_post = pygame.image.load("Assests/tile/19.png").convert_alpha()
        self._goal_post = pygame.transform.scale(self._goal_post, (TILE_SIZE, TILE_SIZE))
        self.__goal_active = True

    def Display_Goal(self, distance_moved):
        """Displays that the goal is active"""

        if self.__goal_active == True:
            screen.blit(self._goal_post, (self.get_rect().x + distance_moved, self.get_rect().y -1*TILE_SIZE))
        
    def set_goal_active(self, value):
        self.__goal_active = value

    def get_goal_active(self):
        return self.__goal_active


class Player():
    def __init__(self, username, GOLFBALL):
        self.__username = username #Player Name
        self.__totalstrokes = 0 #Total stokes
        self.__totalscore = 0 #Total score
        self.__totaltime = 0
        self.__playergolfball = Golf_Ball(GOLFBALL) #Player ball
        self.__time = 0
        self.__strokes = 0

    def __divider(self):
        """Diver is way of measuring rewaring a player
        with higher divider for fewer strokes"""
        
        if self.__strokes >= 0 and self.__strokes <= 9:
            return 14
        elif self.__strokes >= 10 and self.__strokes <= 15:
            return 10
        elif self.__strokes >= 16 and self.__strokes <= 20:
            return 8
        elif self.__strokes >= 21 and self.__strokes <= 28:
            return 6
        elif self.__strokes >= 29 and self.__strokes <= 35:
            return 2
        return -(self.__strokes/10)

    def add_to_totalstokes(self, strokes):
        self.__totalstrokes += strokes

    def add_to_stokes(self, strokes):
        self.__strokes += strokes

    def add_to_time(self, value):
        self.__time += value

    def add_to_total_time(self, value):
        self.__time += value

    def new_ball(self, GOLFBALL):
        self.__playergolfball = Golf_Ball(GOLFBALL)

    def reset(self):
        """Reset strokes and time"""

        self.__totalstrokes += self.__strokes
        self.__totaltime += self.__time
        self.__strokes = 0
        self.__time = 0

    def score_calculator(self, amount_of_goals):
        """Calculates score"""

        starting_score = amount_of_goals * 1000 #Starting Score
        LOGGER.info(f"starting score: {starting_score}")
        divder = self.__divider()  #Divider
        LOGGER.info(f"divider: {divder} and strokes: {self.__strokes}")
        LOGGER.info(f"Time {self.__time} and score {(round(starting_score / (self.__time / divder)))*10}")
        self.__totalscore += round(((starting_score / (self.__time / divder))*100)) #Algorithm
        LOGGER.info(f"Total score: {self.__totalscore}")
        
        
    def get_username(self):
        return self.__username
    
    def get_total_stokes(self):
        return self.__totalstrokes

    def get_strokes(self):
        return self.__strokes

    def get_golfball(self):
        return self.__playergolfball

    def get_time(self):
        return self.__time

    def get_total_time(self):
        return self.__totaltime 

    def set_time(self):
        return self.__time
    
    def get_total_score(self):
        return self.__totalscore

    def set_username(self, username):
        self.__username = username

    def set_totalstrokes(self, strokes):
        self.__totalstrokes = strokes

    def set_strokes(self, strokes):
        self.__strokes = strokes




class Level():
    def __init__(self, levelname):
        self.__level = levelname #Current level
        self.__backgroundscroll = 0 #Background scroll starts at zero
        self.__backgrond_widith = background_1.get_width()
        self.__backgrond_height = background_2.get_height()
        self.__background_threshold_right= 1000 #Camera threshold to the right
        self.__background_threshold_left = 100  ##Camera threshold to the left
        self.__background_threshold_middle = SCREEN_WIDTH//2 #Camera threshold to the middle
        self.__tiles = ceil(SCREEN_WIDTH /  self.__backgrond_widith) + 1 #how many images needed to display background
        self.__control_background = True #If the user allowed use scroll
        self.__block_list = self.__CreateBlockList() #Creates a list of all images of tiles/blocks
        self.__world_data = [] #All infomation about the current world
    

    def __CreateBlockList(self):
        """Creates a list of all images of tiles/blocks """

        LOGGER.info("Create List Of Image Tiles")
        tile_list = []
        for x in range(TILE_TYPES):
            img = pygame.image.load(f'Assests/tile/{x}.png') #Loads the image
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) #Scales it
            tile_list.append(img) #Add to list
        return tile_list

    def draw_background(self):
        """Draw the background for the game """

        #Draw all three layers of images
        for i in range(0, self.__tiles):
            screen.blit(background_1, (((i * self.__backgrond_widith) + self.__backgroundscroll) , 0))
            screen.blit(background_2, (((i * self.__backgrond_widith) + self.__backgroundscroll), 0))
            screen.blit(background_3, (((i * self.__backgrond_widith) + self.__backgroundscroll), 0)) 

    def update_backgorund(self):
        """Add a new tile in either vertical direction"""

        #Reset Scroll (For going forward)
        if abs(self.__backgroundscroll) > self.__backgrond_widith:
            self.__backgroundscroll = 0

        #Reset Scroll (For going backward)
        if abs(self.__backgroundscroll) < self.__backgrond_widith and self.__backgroundscroll > 0:
            self.__backgroundscroll = self.__backgroundscroll - self.__backgrond_widith

    def create_background(self):
        """Creates the game backgorund and updates it """
        self.draw_background()
        self.update_backgorund()

    def update_scroll_right(self, number):
        """Scroll backgorund right """
        self.__backgroundscroll -= number

    def update_scroll_left(self, number):
        """Scroll backgorund left """
        self.__backgroundscroll += number

    def next_level(self, value):
        self.__level += value

    def get_block_list(self):
        return self.__block_list

    def get_control_backgorund(self):
        return self.__control_background

    def get_scroll_background(self):
        return self.__backgroundscroll

    def get_threshold_right(self):
        return self.__background_threshold_right

    def get_threshold_left(self):
        return self.__background_threshold_left

    def get_threshold_middle(self):
        return self.__background_threshold_middle

    def get_level(self):
        return self.__level

    def get_world_data(self):
        return self.__world_data

    def set_control_background(self, locked):
        self.__control_background = locked

    def set_scroll_background(self, number):
        self.__backgroundscroll = number

    def set_level(self, level):
        self.__level = level

    def set_World_data(self, value):
        self.__world_data = value



class Golf_Ball():
    def __init__(self, GOLFBALL):
        self.__GOLFBALL_image = pygame.transform.scale(GOLFBALL,(int(GOLFBALL.get_width()*1.3), 
        int(GOLFBALL.get_height()*1.3)))
        self.__BallPostion = [0,0] #[x,y] Where image of the ball postioned within the game 
        self.__GOLFBALL_rect = GOLFBALL_IMG.get_rect() #Rectangle for collison for golfball
        self.__GOLFBALL_rect.x = self.__BallPostion[0] #Rectangele x postion
        self.__GOLFBALL_rect.y = self.__BallPostion[1] #Rectangele y postion
        self.__GRAVITY = 10 #Gravity
        self.__BALL_MASS = 0.037 #The weight of the ball
        self.__AirResistance = 0.005 #The amount air resitance
        self.__BallSpeed = 0 #The power of the swing
        self.__BallAngle = 0 #The angle of the swing
        self.__clicked = False #If the player has swang
        self.__stop = False #If the turn is over
        self.__display_shot_info = gogolf_lilbray.Text() #Create text object to display text
        self.__direction = 1 #Direction the ball is going in the x directions
        self.__r_colour = 247 #Colour of line when aiming from a cetian distnace
        self.__ball_spawn_location = (0, 0) #Ball spawn location
        self.__ball_pre_pos = (0, 0) #Set old postion of ball location

        
    def __shot_infomation(self):
        """Displays infomation about the shot, including speed and angle"""
        self.__display_shot_info.set_all(f"Ball Speed: {round(self.__BallSpeed)} ", ORANGE, P2, 22, 10, 10)
        self.__display_shot_info.draw_text(screen)
        self.__display_shot_info.set_text(f"Ball Angle: {abs(round(degrees(self.__BallAngle))-180)}") 
        self.__display_shot_info.set_y(45)
        self.__display_shot_info.draw_text(screen)


    def __power_increaser(self):
        """Allows the user to have sharper increase in power to helps in tight situations"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            return 4
        return 1


    def __shot_calculator(self, mouse_position):
        """Calculates the power/angle of the user shot based on distance from distance and the user angle postion from the ball.
        In additon also sets the direction the ball intially travelling"""

        #Difference between mouse pos and ball pos
        dx = mouse_position[0] - self.__BallPostion[0]
        dy = mouse_position[1] - self.__BallPostion[1]

        #Finds the distance
        self.__BallSpeed = sqrt(dx**2 + dy**2) * 1.5

        #Finds the angle
        self.__BallAngle = atan2(dy, dx) #Radians
        self.__BallSpeed = self.__power_increaser()*self.__BallSpeed 
        
        #Cap for distance 
        if self.__BallSpeed > 1000:
            self.__BallSpeed = 1000

        #Checks for intial direction
        if degrees(self.__BallAngle) < 90 and degrees(self.__BallAngle) > -90:
            self.__direction = -1

        if abs(degrees(self.__BallAngle)) > 90 :
            self.__direction = 1


    def __line_up(self, mouse_position):
        """Displays line to help player player see where the ball will go and the amount power with 
        change the line colour as another indaicator"""
        self.__r_colour = self.__BallSpeed//4
        pygame.draw.line(screen, (self.__r_colour, 180, 47), (self.__BallPostion[0] + 8, self.__BallPostion[1] + 8), mouse_position, 3)


    def __handle_y_collsion(self, tile, distance):
        """Handle y collsions of the ball with tiles """

        if abs(self.__VelocityOfBall[1]) > 75 and  abs(self.__VelocityOfBall[0]) > 0.1:
            #Affects the game y ball velocity (flips it to going opposite way and losing energy)
            self.__VelocityOfBall[1] = -self.__VelocityOfBall[1]  / 4

            #Affects the game x ball velocity
            if abs(self.__VelocityOfBall[0]  / 6)*self.__direction > 0.1:
                self.__VelocityOfBall[0] -= abs(self.__VelocityOfBall[0]  / 6)*self.__direction


        elif abs(self.__VelocityOfBall[1]) > 0.2 and  abs(self.__VelocityOfBall[0]) > 0.1:
            
            #Affects the game y ball velocity (flips it to going opposite way and losing energy)
            self.__VelocityOfBall[1] = -self.__VelocityOfBall[1]  / 3

            #Affects the game x ball velocity
            if abs(self.__VelocityOfBall[0]  / 6)*self.__direction > 0.1:
                self.__VelocityOfBall[0] -= abs(self.__VelocityOfBall[0]  / 5.5)*self.__direction
            

            LOGGER.info(f"hit y {tile.get_rect().y}")

        else:
            #Ball has stop moving, so this tell the program that
            self.__stop = True
            self.__ball_pre_pos = (self.__BallPostion[0] - distance, tile.get_rect().y - 20)
            #Set ball postion above tile to help ball be above the ties
            self.set_ball_postion(self.__BallPostion[0], tile.get_rect().y - 20)


    def __handle_x_collsion(self):
        """Handle x collsions of the ball with tiles """

        self.__direction = self.__direction*-1
        self.__VelocityOfBall[0] = -self.__VelocityOfBall[0]  / 2.5



    def __handle_goal_collsion(self, tile, distance, update_step):
        """Handle goal collsions of the ball with goal tiles """

        #Checks if ball gone in the hole
        if tile.get_rect().y - TILE_SIZE*0.12 < self.__GOLFBALL_rect.y and tile.get_goal_active():

            tile.set_goal_active(False)
            self.__reset_ball_location(distance)


    def __reset_ball_location(self, distance):
        """Reset ball location to back to the starting point """

        self.__VelocityOfBall[0] = 0
        self.__VelocityOfBall[1] = 0
        self.set_ball_postion(distance + self.__ball_spawn_location[0], self.__ball_spawn_location[1])


    def __collison(self, tile, distance ,update_step ,player):
        """Checks for collisons"""

        #CHECK ball fell of the map or touches water
        if self.__BallPostion[1] > SCREEN_HEIGHT + 50 or (tile.get_block_type() == "water" and tile.get_rect().colliderect(-distance + self.__GOLFBALL_rect.x , 
        self.__GOLFBALL_rect.y + (self.__VelocityOfBall[1]*update_step), self.__GOLFBALL_image.get_width(), self.__GOLFBALL_image.get_height())):

            #Kill ball velocity
            self.__VelocityOfBall[0] = 0
            self.__VelocityOfBall[1] = 0

            #Set ball postion
            if not self.__ball_pre_pos == (0,0):
                self.set_ball_postion(self.__ball_pre_pos[0] + distance, self.__ball_pre_pos[1])
            else:
                self.__reset_ball_location(distance)
            player.add_to_stokes(1)
        
        #Checks if ball hit a goal tile/block
        if tile.get_block_type() == "goal" and tile.get_rect().colliderect(-distance + self.__GOLFBALL_rect.x , 
        self.__GOLFBALL_rect.y, self.__GOLFBALL_image.get_width(), self.__GOLFBALL_image.get_height()):

            self.__handle_goal_collsion(tile, distance, update_step)
            LOGGER.info(f"Goal hit: {tile.get_rect().y - 1*TILE_SIZE//3 > self.__GOLFBALL_rect.y}")
            LOGGER.info(f"TILE pos: {tile.get_rect().y - 1*TILE_SIZE//3} BAll pos: {self.__GOLFBALL_rect.y}")

        #If ball dosent hit a goal tile
        else:

            #CHECK Y collsions
            if tile.get_rect().colliderect(-distance + self.__GOLFBALL_rect.x , self.__GOLFBALL_rect.y + (self.__VelocityOfBall[1]*update_step) + 1, self.__GOLFBALL_image.get_width(), self.__GOLFBALL_image.get_height()):
                self.__handle_y_collsion(tile, distance)

            #CHECK X collsions
            if tile.get_rect().colliderect(-distance + self.__GOLFBALL_rect.x + (self.__VelocityOfBall[0] *update_step), self.__GOLFBALL_rect.y, self.__GOLFBALL_image.get_width(), self.__GOLFBALL_image.get_height()):
                    self.__handle_x_collsion()


    def aim(self, player):
        """Use to set the force of ball (ball speed) and the ball angle"""

        mouse_position = pygame.mouse.get_pos()
        self.__line_up(mouse_position)
        self.__shot_infomation()
        self.__shot_calculator(mouse_position)
            
        if pygame.mouse.get_pressed()[2] and self.__clicked == False:
            self.__clicked = True
            LOGGER.info("Player set his aim")
            LOGGER.info(f"Mouse postions: {mouse_position}")
            LOGGER.info(f"Direction: {self.__direction}")
            LOGGER.info(f"Ball postion: {self.__BallPostion}")
            LOGGER.info(f"Ball Speed: {self.__BallSpeed} Ball Angle: {degrees(self.__BallAngle)}")
            player.add_to_stokes(1)


    def swing(self):
        """Sets velocitys in x and y"""

        #Intial Velocitys 
        XVelocity = -self.__BallSpeed*cos(self.__BallAngle)
        YVelocity = -self.__BallSpeed*sin(self.__BallAngle)
        self.__VelocityOfBall = [XVelocity, YVelocity]
        
    
    def update_flight(self, update_step):
        """Update the ball flight path"""

        #Calculation forr flight [x,y]
        gravity_acceleration = np.array([0, self.__GRAVITY])
        air_resistance_acceleration = -self.__AirResistance * np.array(self.__VelocityOfBall) #Apply AirResistance to the x, y velcoity
        acceleration = gravity_acceleration + air_resistance_acceleration #Finds total accleration

        #Updates velocity 
        self.__VelocityOfBall += acceleration / self.__BALL_MASS * update_step
    

        #Updates Ball position 
        self.__BallPostion += self.__VelocityOfBall * update_step

        #Updates Ball rectangle position
        self.__GOLFBALL_rect.x, self.__GOLFBALL_rect.y = self.__BallPostion.astype(int)

    def trajecotry(self, obstacles, distance, player):
        update_step = 0.028 #Slows the ball movemnet

        if self.__clicked:
            self.update_flight(update_step)

            if not self.__stop:
                for tile in obstacles:
                    self.__collison(tile, distance, update_step, player)


    def display_ball(self):
        """Displays ball on screen """
        screen.blit(self.__GOLFBALL_image, (int(self.__BallPostion[0]), int(self.__BallPostion[1])))

    def update_ball_to_right(self, number):
        """Moves ball to right within world movemnet"""
        self.__BallPostion[0] -=number

    def update_ball_to_left(self, number):
        """Moves ball to left within world movemnet"""
        self.__BallPostion[0] +=number
        
    def get_stop(self):
        """Returns stop"""
        return self.__stop

    def get_clicked(self):
        """Returns clicked """
        return self.__clicked

    def get_x_velocityofball(self):
        """Returns velocity x"""
        return self.__VelocityOfBall[0]

    def get_y_velocityofball(self):
        """Returns velocity y"""
        return self.__VelocityOfBall[1]

    def get_postion_of_ball(self):
        """Returns ball postion"""
        return self.__BallPostion

    def get_direction(self):
        """Returns direction"""
        return self.__direction

    def get_ball_speed(self):
        """Returns ball power/speed"""
        return self.__BallSpeed

    def set_air_resistance(self, Resistance):
        """Set air restiacne value"""
        self.__AirResistance = Resistance

    def set_stop(self, value):
        """Set stop value"""
        self.__stop = value
    
    def set_clicked(self, value):
        """Change clicked value """
        self.__clicked = value

    def set_spawn_location(self, location):
        """Set spawn location, location value needs to be a tuple/list"""
        self.__ball_spawn_location = location

    def set_ball_postion(self, x, y):
        """Sets ball postion postion and the golfball rectangle"""
        self.__BallPostion = [x, y]
        self.__GOLFBALL_rect.x = x
        self.__GOLFBALL_rect.y = y


