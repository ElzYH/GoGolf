import pygame
import logging
import math
import sys
import pickle
import gogolf_lilbray

pygame.init()

LOGGER = logging.getLogger(f"{__name__}")

#Create display window
SCREEN_HEIGHT = 768 
SCREEN_WIDTH = 1366
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))



#FPS
clock = pygame.time.Clock()
FPS = 100

pygame.display.set_caption("Go Golf")
#icon = pygame.image.load('Assets/uno_icon.ico')
#pygame.display.set_icon(icon)
pygame.key.set_repeat(0,0)

#Load Images

GOLFBALL_IMG = pygame.image.load('Assests/20.png')


#Image Widiths and Heights
background_1 = pygame.image.load('Background_Img/1.png').convert_alpha()
background_2 = pygame.image.load('Background_Img/2.png').convert_alpha()
background_3 = pygame.image.load('Background_Img/4.png').convert_alpha()


GOLFBALL_WIDITH = GOLFBALL_IMG.get_width()
GOLFBALL_HEIGHT = GOLFBALL_IMG.get_height()


#Colours
BLUE = "#2596be"
WHITE = "#F5FEFD"

#Fonts
WII_FONT = "Assets/Fonts/AOTFShinGoProMedium.otf"

#Grid
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS 
TILE_TYPES = 21


class GoGolf():
    def __init__(self, username):
        self.__game_running = True
        self.__current_player = Player(username)
        self.__currentlevel = Level(1, 'Level_Editor/Background_Image/bg.png')
        self.__past_camera_theshold = False
        self.__gap = 0
        self.__muitplier = 1.5
        self.__distance_moved = 0
        self.__place_ball = True
        self.__world = World()


    def PlayGame(self):

        #Temp location
        self.LoadWorld()
        self.__world.proccess_data(self.__currentlevel.get_world_data(), self.__currentlevel.get_block_list(), self.__current_player.get_golfball())

        while self.__game_running:
            self.__currentlevel.create_background()
            self.__world.draw(self.__distance_moved)


            if self.__currentlevel.get_control_backgorund():
                self.level_controls()
                if not self.__currentlevel.get_control_backgorund():
                    self.set_camera_pos()

            else:
                self.player_can_shoot()
                if self.__current_player.get_golfball().get_stop():
                    self.__current_player.get_golfball().set_stop(False)
                    self.__currentlevel.set_control_background(True)
                    self.__current_player.get_golfball().set_clicked(False)

            self.__current_player.get_golfball().display_ball()
            self.EventHandler()

        
    def EventHandler(self):
        #Event Handler 
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                LOGGER.info("Quit Application")
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)


    def update_camera_postion(self):

        player_ball = self.__current_player.get_golfball()
        ball_postion = player_ball.get_postion_of_ball()
        speed_movement = player_ball.get_x_velocityofball()//110 #120
        self.__muitplier = 3
        
        if ball_postion[0] > self.__currentlevel.get_threshold_left():
            if ball_postion[0] > self.__currentlevel.get_threshold_right() and self.__gap <= 0:
                self.__gap = self.__currentlevel.get_threshold_right() - self.__currentlevel.get_threshold_left()
                

            #if self.__gap > 0:
            offset_x = self.__muitplier * speed_movement
            self.__currentlevel.update_scroll_right(offset_x)
            player_ball.update_ball_to_right(offset_x)
            self.__distance_moved -= offset_x
            self.__gap = self.__gap - 1



    def set_camera_pos(self):
        golfball = self.__current_player.get_golfball()
        golfball_x_pos = golfball.get_postion_of_ball()[0]

        LOGGER.info(f"golfball x pos before {golfball_x_pos} ")
        LOGGER.info(f"Scroll Before {self.__currentlevel.get_scroll_background()}")
        print(f"distance {self.__distance_moved}")

        # Calculate the offset to center the golf ball on the screen
        # Center the golf ball on the screen
        offset_x = -(golfball.get_postion_of_ball()[0] - SCREEN_WIDTH // 2) + self.__distance_moved 
        offset_y = golfball.get_postion_of_ball()[1]

        LOGGER.info(f"Distance camera from ball x of camera is {self.__distance_moved} ")
        LOGGER.info(f"Offset x of camera is {offset_x} ")

        # Center the golf ball on the screen
        #golfball.set_ball_postion(offset_x, offset_y)

         # Center the golf ball on the screen
        golfball.set_ball_postion(SCREEN_WIDTH//2 , offset_y)
        
        # Update the background scroll to center the camera on the golf ball
        self.__currentlevel.set_scroll_background(offset_x)

    

        self.__distance_moved = (offset_x)
        LOGGER.info(f"golfball x pos after {golfball_x_pos} ")
        LOGGER.info(f"Scroll after {self.__currentlevel.get_scroll_background()}")




    def player_can_shoot(self):
        player_ball = self.__current_player.get_golfball()

        if not self.__currentlevel.get_control_backgorund():

            #Stop the game reseting the shot (if not in places the ball just go in the same angle for ever)
            if not player_ball.get_clicked():
                player_ball.shot()
                print("1")

            if not player_ball.get_stop():
                player_ball.trajecotry(self.__world.get_obstacle_list(), self.__distance_moved)
                if player_ball.get_clicked():
                    self.update_camera_postion()
                print("2")
            # else:
            #     self.__currentlevel.set_control_background(True)
            #     player_ball.set_clicked(False)
            #     print("3")



    def level_controls(self):
        if self.__currentlevel.get_control_backgorund():

            keys = pygame.key.get_pressed()
            spped_muiltplayer = 1

            if keys[pygame.K_LSHIFT]:
                spped_muiltplayer = 5
                
            speed = 5*spped_muiltplayer
            if keys[pygame.K_d] and abs(self.__distance_moved)//TILE_SIZE < 150:
                self.__currentlevel.update_scroll_right(speed)
                self.__current_player.get_golfball().update_ball_to_right(speed)
                self.__distance_moved -= speed

            if keys[pygame.K_a] and self.__distance_moved //TILE_SIZE < 2:
                self.__currentlevel.update_scroll_left(speed)
                self.__current_player.get_golfball().update_ball_to_left(speed)
                self.__distance_moved += speed

            if keys[pygame.K_RETURN]:
                self.__currentlevel.set_control_background(False)


    def LoadWorld(self):
        #Create emptylist 2d array
        world_data = [[-1] * 150 for _ in range(16)]
        #Ground
        world_data[-1] = [2 for i in world_data[-1]]

        LOGGER.info("Save Level")
        pickle_in = open(f'Levels/level{self.__currentlevel.get_level()}_data', 'rb')
        self.__currentlevel.set_scroll_background(0)
        self.__currentlevel.set_World_data(world_data)
        self.__currentlevel.set_World_data(pickle.load(pickle_in))
        LOGGER.info(f"Level {self.__currentlevel.get_level()} has been loaded ")


    def tiles_pixels(self, row):
        return SCREEN_HEIGHT * row 
        
class World():
    def __init__(self):
        self.obstacle_list = []

    def proccess_data(self, world_data, tile_img_list, golfball):
        for y, row in enumerate(world_data):
            for x, block in enumerate(row):
                if block >= 0:
                    img = tile_img_list[block]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if block <= 7 or block >= 12 and block <= 17:
                        tile_data = Tile(img, img_rect, x, y, "obstacle")
                        self.obstacle_list.append(tile_data)
                    elif block >= 8 and block <= 11:
                        tile_data = Water(img, img_rect, x, y, "water")
                        self.obstacle_list.append(tile_data)
                    elif block >= 18 and block <= 19:
                        tile_data = Goal(img, img_rect, x, y, "goal")
                        self.obstacle_list.append(tile_data)
                    elif block == 20:
                        golfball.set_ball_postion(x*TILE_SIZE, y*TILE_SIZE)


    def draw(self, distance_moved):
        for block in self.obstacle_list:
            x = block.get_rect().x // TILE_SIZE  # Calculate the x-coordinate in terms of tiles
            if (x * TILE_SIZE + distance_moved) < SCREEN_WIDTH + 1*TILE_SIZE and (x * TILE_SIZE + distance_moved) > -1 * TILE_SIZE:
                temp = block.get_rect().x
                screen.blit(block.get_img(), (temp + distance_moved, block.get_rect().y))



    def get_obstacle_list(self):
        return self.obstacle_list



                        

class Tile():
    def __init__(self, img, img_rect, x, y, img_type):
        self.__img = img
        self.__rect = img_rect
        self.__rect.midtop = (x + TILE_SIZE //2, y + (TILE_SIZE - self.__img.get_height()))
        self.__rect.x = x * TILE_SIZE
        self.__rect.y = y * TILE_SIZE
        self.__type = img_type

    def get_img(self):
        return self.__img

    def get_rect(self):
        return self.__rect

    def set_rectx(self ,v):
        self.__rect.x = v

    def set_rectu(self, v):
        self.__rect.y = v

    def set_rect(self, distnace):
        self.__rect.x += distnace



class Water(Tile):
    def __init__(self, img, img_rect, x, y, img_type):
        super().__init__(img, img_rect, x, y, img_type)

class Goal(Tile):
    def __init__(self, img, img_rect, x, y, img_type):
        super().__init__(img, img_rect, x, y, img_type)




class Player():
    def __init__(self, username):
        self.__username = username
        self.__totalstrokes = 0
        self.__totalscore = 0
        self.__playergolfball = Golf_Ball()

    def set_currentlevel(self, level):
        self.__currentlevel = level

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def set_totalstrokes(self, strokes):
        self.__totalstrokes = strokes

    def add_to_totalstokes(self, stokes):
        self.__totalstrokes += strokes
    
    def get_total_stokes(self):
        return self.__totalstrokes

    def get_golfball(self):
        return self.__playergolfball




class Level():
    def __init__(self, levelname, background):
        self.__level = levelname
        self.__backgroundscroll = 0
        self.__backgrond_widith = background_1.get_width()
        self.__backgrond_height = background_2.get_height()
        self.__background_threshold_right= 1000
        self.__background_threshold_left = 100
        self.__background_threshold_middle = SCREEN_WIDTH//2
        self.__tiles = math.ceil(SCREEN_WIDTH /  self.__backgrond_widith) + 1 #1 is a buffer
        self.__control_background = True #If the user allowed use scroll
        self.__block_list = self.__CreateBlockList() 
        self.__world_data = []
    

    def __CreateBlockList(self):
        LOGGER.info("Create List Of Image Tiles")
        tile_list = []
        for x in range(TILE_TYPES):
            img = pygame.image.load(f'Assests/tile/{x}.png')
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            tile_list.append(img)
        return tile_list

    def get_block_list(self):
        return self.__block_list

    def get_control_backgorund(self):
        return self.__control_background

    def set_control_background(self, locked):
        self.__control_background = locked

    def update_scroll_right(self, number):
        self.__backgroundscroll -= number

    def update_scroll_left(self, number):
        self.__backgroundscroll += number

    def set_scroll_background(self, number):
        self.__backgroundscroll = number

    def set_World_data(self, value):
        self.__world_data = value

    def get_scroll_background(self):
        return self.__backgroundscroll

    def draw_background(self):
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
        self.draw_background()
        self.update_backgorund()

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





class Golf_Ball():
    def __init__(self):
        self.__GOLFBALL_image = pygame.transform.scale(GOLFBALL_IMG,(int(GOLFBALL_WIDITH*1.5), 
        int(GOLFBALL_HEIGHT*1.5)))
        self.__BallPostion = [0,0] #[x,y]
        self.__GOLFBALL_rect = GOLFBALL_IMG.get_rect()
        self.__GOLFBALL_rect.x = self.__BallPostion[0]
        self.__GOLFBALL_rect.y = self.__BallPostion[1]
        self.__GRAVITY = 10
        self.__BALL_MASS = 0.045
        self.__AirResistance = 0.005
        self.__BallSpeed = 0
        self.__BallAngle = 0
        self.__clicked = False
        self.__stop = False
        self.__display_shot_info = gogolf_lilbray.Text()
        self.__time_to_stop = 0
        self.__direction = 1
        self.__r_colour = 247

    def set_air_resistance(self, Resistance):
        self.__AirResistance = Resistance

    def set_stop(self, value):
        self.__stop = value


    def set_ball_postion(self, x, y):
        self.__BallPostion = [x, y]
        self.__GOLFBALL_rect.x = x
        self.__GOLFBALL_rect.y = y

    def update_ball_to_right(self, number):
        self.__BallPostion[0] -=number

    def update_ball_to_left(self, number):
        self.__BallPostion[0] +=number

    def get_postion_of_ball(self):
        return self.__BallPostion

    def get_ball_speed(self):
        return self.__BallSpeed

    def direction_of_golfball_x(self):
        if self.__VelocityOfBall[0] > 0:
            #Right
            return 1
        else:
            #Left
            return -1
        
    def shot_infomation(self):
        self.__display_shot_info.set_all(f"Ball Speed: {round(self.__BallSpeed)} ", WHITE, WII_FONT, 30, 10, 10)
        self.__display_shot_info.draw_text(screen)
        self.__display_shot_info.set_text(f"Ball Angle: {abs(round(math.degrees(self.__BallAngle))-180)}") 
        self.__display_shot_info.set_y(50)
        self.__display_shot_info.draw_text(screen)

    def power_increaser(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LCTRL]:
            return 4
        return 1

    def aim(self):
        """Use to set the force of ball (ball speed) and the ball angle"""

        mouse_position = pygame.mouse.get_pos()
        self.__r_colour = self.__BallSpeed//4
        pygame.draw.line(screen, (self.__r_colour, 180, 47), (self.__BallPostion[0] + 8, self.__BallPostion[1] + 8), mouse_position, 3)
        right_click = pygame.mouse.get_pressed()
        self.shot_infomation()

        
        
        dx = mouse_position[0] - self.__BallPostion[0]
        dy = mouse_position[1] - self.__BallPostion[1]
        self.__BallSpeed = math.sqrt(dx**2 + dy**2) * 2
        self.__BallAngle = math.atan2(dy, dx)

        self.__BallSpeed = self.power_increaser()*self.__BallSpeed 

        if self.__BallSpeed > 1000:
            self.__BallSpeed = 1000

        if math.degrees(self.__BallAngle) < 90 and math.degrees(self.__BallAngle) > -90:
            self.__direction = -1

        if abs(math.degrees(self.__BallAngle)) > 90 :
            self.__direction = 1   
            
        
        if right_click[2] and self.__clicked == False:
            self.__clicked = True
            LOGGER.info("Player set his aim")
            LOGGER.info(mouse_position)
            LOGGER.info(f"Direction {self.__direction}")
            LOGGER.info(self.__BallPostion)
            LOGGER.info(f"Ball Speed: {self.__BallSpeed} Ball Angle: {math.degrees(self.__BallAngle)}")


    def swing(self):
        #Intial Velocitys 
        XVelocity = -self.__BallSpeed*math.cos(self.__BallAngle)
        YVelocity = -self.__BallSpeed*math.sin(self.__BallAngle)
        self.__VelocityOfBall = [XVelocity, YVelocity]

    def shot(self):
        self.aim()
        self.swing()

    def get_clicked(self):
        return self.__clicked

    def update_flight(self, update_step):
        #Acceleration Calucation
        GravityAcceleration = [0, self.__GRAVITY] #[x,y]
        self.__AirResistanceAcceleration = [-self.__AirResistance * self.__VelocityOfBall[i] for i in range(0, len(self.__VelocityOfBall))]
        Acceleration = [sum(x) for x in zip(GravityAcceleration, self.__AirResistanceAcceleration)]

        self.__VelocityOfBall[0] += Acceleration[0] / self.__BALL_MASS * update_step
        self.__VelocityOfBall[1] += Acceleration[1] / self.__BALL_MASS * update_step
        self.__BallPostion[0] += self.__VelocityOfBall[0] *update_step
        self.__BallPostion[1] += self.__VelocityOfBall[1] *update_step
        self.__GOLFBALL_rect.x = self.__BallPostion[0]
        self.__GOLFBALL_rect.y = self.__BallPostion[1]


    def set_clicked(self, value):
        self.__clicked = value



    def trajecotry(self, obstacles, distance):
        update_step = 0.025

        if self.__clicked:
            self.update_flight(update_step)

            #Check for collioson
            if not self.__stop:
                for tile in obstacles:

                    #CHECK Y
                    if tile.get_rect().colliderect(-distance + self.__GOLFBALL_rect.x , self.__GOLFBALL_rect.y + (self.__VelocityOfBall[1]*update_step), self.__GOLFBALL_image.get_width(), self.__GOLFBALL_image.get_height()):
                        if abs(self.__VelocityOfBall[1]) > 200 :
                            self.__VelocityOfBall[1] = -self.__VelocityOfBall[1]  / 3
                            self.__VelocityOfBall[0] -= self.__VelocityOfBall[0]  / 45
                            print(f"hit y {tile.get_rect().y}")
                        elif abs(self.__VelocityOfBall[0]) > 0.5 :
                            self.__VelocityOfBall[0] -= self.__VelocityOfBall[0]  / 20
                            self.__VelocityOfBall[1] = 15
                            print(f"hit y {tile.get_rect().y}")

                        else:
                            self.__stop = True
                     
                            self.set_ball_postion(self.__BallPostion[0], self.__BallPostion[1] -3.7 )

                    #CHECK X
                    if tile.get_rect().colliderect(-distance + self.__GOLFBALL_rect.x + (self.__VelocityOfBall[0] *update_step), self.__GOLFBALL_rect.y, self.__GOLFBALL_image.get_width(), self.__GOLFBALL_image.get_height()):
                            self.__direction = self.__direction*-1
                            self.__VelocityOfBall[0] = -self.__VelocityOfBall[0]  / 2





    
            # print(f"ball pos: {self.__BallPostion[0]} and rect.x: {self.__GOLFBALL_rect.x}")
            # print(f"ball pos: {self.__BallPostion[1]} and rect.x: {self.__GOLFBALL_rect.y}")
        

    def get_stop(self):
        return self.__stop

    def get_x_velocityofball(self):
        return self.__VelocityOfBall[0]

    def get_y_velocityofball(self):
        return self.__VelocityOfBall[1]

    
    def display_ball(self):
        screen.blit(self.__GOLFBALL_image, (int(self.__BallPostion[0]), int(self.__BallPostion[1])))



        
        

def gameloop():
    game = GoGolf("Erol")
    game.PlayGame()
        

