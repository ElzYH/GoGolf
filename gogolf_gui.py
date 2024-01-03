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
FPS = 100

pygame.display.set_caption("Go Golf")
#icon = pygame.image.load('Assets/uno_icon.ico')
#pygame.display.set_icon(icon)
pygame.key.set_repeat(0,0)

#Load Images
BACKGROUND1_IMG = pygame.image.load('bg.png').convert_alpha()
GOLFBALL_IMG = pygame.image.load('golfball.png')


#Image Widiths and Heights
BACKGROUND1_WIDITH = BACKGROUND1_IMG.get_width()
GOLFBALL_WIDITH = GOLFBALL_IMG.get_width()
GOLFBALL_HEIGHT = GOLFBALL_IMG.get_height()

class Player():
    def __init__(self, username):
        self.__username = username
        self.__totalstrokes = 0
        self.__totalscore = 0
        self.__currentlevel = None

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

    

    


        


class Golf_Ball():
    def __init__(self):
        self.__GOLFBALL_image = pygame.transform.scale(GOLFBALL_IMG,(int(GOLFBALL_WIDITH*0.05), 
        int(GOLFBALL_HEIGHT*0.05)))
        self.__GOLFBALL_rect = GOLFBALL_IMG.get_rect()
        self.__BallPostion = [298,423] #[x,y]
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

    def aim(self):
        """Use to set the force of ball(ball speed) and the ball angle"""

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
            LOGGER.info(f"Ball Speed: {self.__BallSpeed} Ball Angle: {math.degrees(self.__BallAngle)}")


    def swing(self):
        #Intial Velocitys 
        XVelocity = abs(self.__BallSpeed*math.cos(self.__BallAngle))
        YVelocity = -self.__BallSpeed*math.sin(self.__BallAngle)
        self.__VelocityOfBall = [XVelocity, YVelocity]

    def get_clicked(self):
        return self.__clicked


    def trajecotry(self):
        update_step = 0.01
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

    
    def display_ball(self):
        screen.blit(self.__GOLFBALL_image, (int(self.__BallPostion[0]), int(self.__BallPostion[1])))
        
        

def gameloop():
    #DEF GAME VARIABLES
    tiles = math.ceil(SCREEN_WIDTH / BACKGROUND1_WIDITH) + 1 #1 is a buffer
    UserControlOfScrollLocked = False #If the user allowed use scroll
    scroll = 0 #Intial Scroll Postion
    ball = Golf_Ball()


    while True:
        
        #DRAW BACKGROUND
        for i in range(0, tiles):
            screen.blit(BACKGROUND1_IMG, (i * BACKGROUND1_WIDITH + scroll, 0))
        
        #scroll background


        #Reset Scroll (For going forward)
        if abs(scroll) > BACKGROUND1_WIDITH:
            scroll = 0

        #Reset Scroll (For going backward)
        if abs(scroll) < BACKGROUND1_WIDITH and scroll > 0:
            scroll = scroll - BACKGROUND1_WIDITH


        #Start of game
        if UserControlOfScrollLocked == False:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                scroll -= 5

            if keys[pygame.K_a]:
                scroll += 5

        else:
            ball.display_ball()

            #Stop the game reseting the shot (if not in places the ball just go in the same angle for ever)
            if not ball.get_clicked():
                ball.aim()
                ball.swing()
            ball.trajecotry()

        #Event Handler 
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                LOGGER.info("Quit Application")
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    UserControlOfScrollLocked = True
                    #Return user start of the level


                

        pygame.display.update()
        clock.tick(FPS)
