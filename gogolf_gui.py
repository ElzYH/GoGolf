import pygame
import logging
import math
import sys

pygame.init()

LOGGER = logging.getLogger(f"{__name__}")

#Create display window
SCREEN_HEIGHT = 768 
SCREEN_WIDTH = 1366
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#FPS
clock = pygame.time.Clock()
FPS = 60

pygame.display.set_caption("Go Golf")
#icon = pygame.image.load('Assets/uno_icon.ico')
#pygame.display.set_icon(icon)
pygame.key.set_repeat(0,0)

#Load Images

GOLFBALL_IMG = pygame.image.load('Assests\golfball.png')


#Image Widiths and Heights

GOLFBALL_WIDITH = GOLFBALL_IMG.get_width()
GOLFBALL_HEIGHT = GOLFBALL_IMG.get_height()


class GoGolf():
    def __init__(self, username):
        self.__game_running = True
        self.__current_player = Player(username)
        self.__currentlevel = Level(1, 'Levels/Level1/bg.png')
        self.__past_camera_theshold = False
        self.__gap = 0
        self.__muitplier = 1.5
        self.__distance_moved = 0


    def PlayGame(self):
        while self.__game_running:
            self.__currentlevel.create_background()
            self.__current_player.get_golfball().display_ball()
            if self.__currentlevel.get_control_backgorund():
                self.level_controls()
                if not self.__currentlevel.get_control_backgorund():
                    self.set_camera_pos()

            else:
                self.player_can_shoot()


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
            self.__gap = self.__gap - 1



    def set_camera_pos(self):
        golfball = self.__current_player.get_golfball()
        golfball_x_pos = golfball.get_postion_of_ball()[0]

        LOGGER.info(f"golfball x pos before {golfball_x_pos} ")
        LOGGER.info(f"Scroll Before {self.__currentlevel.get_scroll_background()}")

        # Calculate the offset to center the golf ball on the screen
        offset_x = self.__distance_moved + (golfball_x_pos - SCREEN_WIDTH // 2)
        offset_y = golfball.get_postion_of_ball()[1]

        LOGGER.info(f"Distance camera from ball x of camera is {self.__distance_moved} ")
        LOGGER.info(f"Offset x of camera is {offset_x} ")

        # Update the background scroll to center the camera on the golf ball
        if not self.__distance_moved == 0:
            self.__currentlevel.set_scroll_background(offset_x)

        # Center the golf ball on the screen
        golfball.set_ball_postion(SCREEN_WIDTH // 2, offset_y)
        LOGGER.info(f"golfball x pos after {golfball_x_pos} ")
        LOGGER.info(f"Scroll after {self.__currentlevel.get_scroll_background()}")




     


    def player_can_shoot(self):
        player_ball = self.__current_player.get_golfball()

        if not self.__currentlevel.get_control_backgorund():

            #Stop the game reseting the shot (if not in places the ball just go in the same angle for ever)
            if not player_ball.get_clicked():
                player_ball.shot()

            player_ball.trajecotry()
            self.update_camera_postion()



    def level_controls(self):
        if self.__currentlevel.get_control_backgorund():

            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                self.__currentlevel.update_scroll_right(5)
                self.__current_player.get_golfball().update_ball_to_right(5)
                self.__distance_moved += 5

            if keys[pygame.K_a]:
                self.__currentlevel.update_scroll_left(5)
                self.__current_player.get_golfball().update_ball_to_left(5)
                self.__distance_moved -= 5

            if keys[pygame.K_RETURN]:
                self.__currentlevel.set_control_background(False)
        
        


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
        self.__name_of_level = levelname
        self.__backgroundscroll = 0
        self.__background_img = pygame.image.load('Levels/Level1/bg.png').convert_alpha()
        self.__backgrond_widith = self.__background_img.get_width()
        self.__backgrond_height = self.__background_img.get_height()
        self.__background_threshold_right= 1000
        self.__background_threshold_left = 100
        self.__background_threshold_middle = SCREEN_WIDTH//2
        self.__tiles = math.ceil(SCREEN_WIDTH /  self.__backgrond_widith) + 1 #1 is a buffer
        self.__control_background = True #If the user allowed use scroll

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

    def get_scroll_background(self):
        return self.__backgroundscroll

    def draw_background(self):
        for i in range(0, self.__tiles):
            screen.blit(self.__background_img, (i * self.__backgrond_widith + self.__backgroundscroll, 0))
        
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





class Golf_Ball():
    def __init__(self):
        self.__GOLFBALL_image = pygame.transform.scale(GOLFBALL_IMG,(int(GOLFBALL_WIDITH*0.05), 
        int(GOLFBALL_HEIGHT*0.05)))
        self.__GOLFBALL_rect = GOLFBALL_IMG.get_rect()
        self.__BallPostion = [SCREEN_WIDTH//2, 530] #[x,y]
        self.__GRAVITY = 10
        self.__BALL_MASS = 0.045
        self.__AirResistance = 0.005
        self.__BallSpeed = 0
        self.__BallAngle = 0
        self.__clicked = False

    def set_air_resistance(self, Resistance):
        self.__AirResistance = Resistance

    def set_ball_postion(self, x, y):
        self.__BallPostion = [x, y]

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
        

    def aim(self):
        """Use to set the force of ball (ball speed) and the ball angle"""

        mouse_position = pygame.mouse.get_pos()
        pygame.draw.line(screen, "#f7a42f", self.__BallPostion, mouse_position)
        right_click = pygame.mouse.get_pressed()

        if right_click[2] and self.__clicked == False:

            pygame.time.wait(10)
            self.__clicked = True
            LOGGER.info("Player set his aim")
            LOGGER.info(mouse_position)
            LOGGER.info(self.__BallPostion)

            dx = mouse_position[0] - self.__BallPostion[0]
            dy = mouse_position[1] - self.__BallPostion[1]

            self.__BallSpeed = math.sqrt(dx**2 + dy**2) * 2
            self.__BallAngle = math.atan2(dy, dx)
            if self.__BallSpeed > 1350:
                self.__BallSpeed = 1350

            LOGGER.info(f"Ball Speed: {self.__BallSpeed} Ball Angle: {math.degrees(self.__BallAngle)}")


    def swing(self):
        #Intial Velocitys 
        XVelocity = abs(self.__BallSpeed*math.cos(self.__BallAngle))
        YVelocity = -self.__BallSpeed*math.sin(self.__BallAngle)
        self.__VelocityOfBall = [XVelocity, YVelocity]

    def shot(self):
        self.aim()
        self.swing()

    def get_clicked(self):
        return self.__clicked

    def trajecotry(self):
        update_step = 0.025
        print(self.__BallPostion)

        if self.__clicked == 1:
            #Acceleration Calucation
            GravityAcceleration = [0, self.__GRAVITY] #[x,y]

            self.__AirResistanceAcceleration = [-self.__AirResistance * self.__VelocityOfBall[i] for i in range(0, len(self.__VelocityOfBall))]
            
            #LOGGER.info(f"Check how zip works {zip(GravityAcceleration, AirResistanceAcceleration)}")

            Acceleration = [sum(x) for x in zip(GravityAcceleration, self.__AirResistanceAcceleration)]

            #LOGGER.info(f"Accleration result {Acceleration}")

            self.__VelocityOfBall[0] += Acceleration[0] / self.__BALL_MASS * update_step
            self.__VelocityOfBall[1] += Acceleration[1] / self.__BALL_MASS * update_step
            self.__BallPostion[0] += self.__VelocityOfBall[0] *update_step
            self.__BallPostion[1] += self.__VelocityOfBall[1] *update_step


    def get_x_velocityofball(self):
        return self.__VelocityOfBall[0]

    def get_y_velocityofball(self):
        return self.__VelocityOfBall[1]


    
    def display_ball(self):
        screen.blit(self.__GOLFBALL_image, (int(self.__BallPostion[0]), int(self.__BallPostion[1])))



        
        

def gameloop():
    game = GoGolf("Erol")
    game.PlayGame()
        

