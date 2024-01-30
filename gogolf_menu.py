import pygame
import logging
from math import ceil, sin
import gogolf_gui
import gogolf_lilbray
import sys
import pygame_textinput
import sqlite3

pygame.init()


LOGGER = logging.getLogger(f"{__name__}")
#FPS
clock = pygame.time.Clock()
FPS = 100

icon = pygame.image.load('Assests/logo1.ico')
pygame.display.set_icon(icon)

#Image Widiths and Heights
background_1 = pygame.image.load('Background_Img/1.png').convert_alpha()
background_2 = pygame.image.load('Background_Img/2.png').convert_alpha()
background_3 = pygame.image.load('Background_Img/4.png').convert_alpha()

logo = pygame.image.load('Assests/logo1.png').convert_alpha()

play_button = pygame.image.load('Assests/play.png')
lb_buttons = pygame.image.load('Assests/leaderboard.png')
quit_buttons = pygame.image.load('Assests/quit.png')
back_buttons = pygame.image.load('Assests/back.png')
three_hole_button = pygame.image.load('Assests/three_hole.png')
five_hole_button = pygame.image.load('Assests/five_hole.png')
score_button = pygame.image.load('Assests/score.png')
time_button = pygame.image.load('Assests/time.png')
strokes_button = pygame.image.load('Assests/strokes.png')

sign_up_button = pygame.image.load('Assests/sign_up.png')
login_button = pygame.image.load('Assests/login.png')

GREY = (245, 244, 243)
BLUE = "#2596be"
WHITE = "#F5FEFD"
ORANGE = "#ff8500"
BLACK = "#000000"
RED = "#D21404"

bg_w = background_1.get_width()
bg_h = background_1.get_height()

WII_FONT = "Assests/Fonts/AOTFShinGoProMedium.otf"
PIXEL_FONT = "Assests/Fonts/04B_30__.TTF"
P2 = "Assests/Fonts/Retro Gaming.ttf"

SCREEN_HEIGHT = 768 
SCREEN_WIDTH = 1366
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

def EventHandler():
    """Event Handler """

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            LOGGER.info("Quit Application")
            sys.exit()

    pygame.display.update()
    clock.tick(FPS)

class Tee_Box():
    def __init__(self):
        self.__run = True
        self.__BG = Background()
        self.__start_menu = StartScreen(self.__BG)
        self.__account = User(self.__BG)
        self.__GameModule = gogolf_gui.GoGolf("Erol")
        self.__menu = MainMenu(self.__BG)

    def Game(self):
        while self.__run:

            if not self.__start_menu.get_running():
                self.__start_menu.start_menu()

            if self.__start_menu.get_running():
                self.__enter = True
                username = self.__account.account_menu()
                self.__menu.main_menu(self.__start_menu, username)

            EventHandler()

                
        
class Background():
    def __init__(self):
        self.__scroll = 0
        self.__tiles = ceil(SCREEN_WIDTH /  bg_w) + 1

    def draw_background(self):
        screen.fill(BLUE)
        self.__scroll -= 4
        for i in range(0, self.__tiles):
            screen.blit(background_1, (i * bg_w + self.__scroll, 0))
            screen.blit(background_2, (i * bg_w + self.__scroll, 0))
            screen.blit(background_3, (i * bg_w + self.__scroll, 0))
        
        if abs(self.__scroll) > bg_w:
                self.__scroll = 0

    
    def side_bar(self):
        pygame.draw.rect(screen, BLUE, (0, 0, 300, SCREEN_HEIGHT))


class StartScreen():
    def __init__(self , bg):
        self.__bg = bg
        self.__direction = 1
        self.__y = 1
        self.__text = gogolf_lilbray.Text()
        self.__start_running = False


    def sin_counter(self):
        if abs(self.__y) % 90 == 0:
            self.__direction = -1
        self.__y +=0.05*self.__direction
        
    
    def start_menu(self):
        keys =  pygame.key.get_pressed()
        self.__bg.draw_background()
        self.floatiing_logo(SCREEN_WIDTH//2- 300, (SCREEN_HEIGHT//2 - 280))
        self.__text.set_all("Press Enter To Start", ORANGE, P2, 40, SCREEN_WIDTH//2 - 260, (sin(self.__y)*10) + 450)
        self.__text.draw_text(screen)
        if keys[pygame.K_RETURN]:
            self.__start_running =  True


    def get_running(self):
        return self.__start_running

    def floatiing_logo(self, x, y):
        self.sin_counter()
        pos = (y) + (sin(self.__y)*10)
        screen.blit(logo, (x, pos))
        self.__text.set_all("Press Enter To Start", ORANGE, P2, 40, SCREEN_WIDTH//2 - 260, pos + 400)


class User():
    def __init__(self, bg):
        self.__username = ""
        self.__password = ""
        self.__bg = bg
        self.__InMenu = True
        self.__menu_choice = ""
        self.__login = gogolf_lilbray.Button(SCREEN_HEIGHT//2  , SCREEN_WIDTH//2 - 350, login_button, 0.5)
        self.__sign_up = gogolf_lilbray.Button(SCREEN_HEIGHT//2 + 400, SCREEN_WIDTH//2- 350, sign_up_button, 0.5)
        self.__back = gogolf_lilbray.Button(50, SCREEN_HEIGHT-150, back_buttons, 0.4)
        self.__manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 8)
        self.__username_text = gogolf_lilbray.Enter_Text(SCREEN_WIDTH//2- 45, SCREEN_HEIGHT//2- 45, "cambria", 22, True, self.__manager)
        self.__password_text = gogolf_lilbray.Enter_Text(SCREEN_WIDTH//2- 45, SCREEN_HEIGHT//2, "cambria", 22, True, self.__manager)
        self.__section = "user"
        self.__display_username = gogolf_lilbray.Text()
        self.__error = ""
        self.__display_error = gogolf_lilbray.Text()

    def __buttons(self, events):
        if self.__login.draw(screen):
            self.__username_text.clear_text()
            self.__password_text.clear_text()
            self.__menu_choice = "login"

        if self.__sign_up.draw(screen):
            self.__username_text.clear_text()
            self.__menu_choice = "sign_up"


    def __user_password(self, events):
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2- 50, SCREEN_HEIGHT//2 - 50, 300, 40))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2- 50, SCREEN_HEIGHT//2 - 5, 300, 40))
        if self.__section == "user":
            self.__username_setter(events)

        elif self.__section == "pass":
            self.__password_setter(events)


    def __username_setter(self, events):
        self.__display_username.set_text("")
        self.__username_text.draw(events, screen, SCREEN_WIDTH//2- 50, SCREEN_HEIGHT//2 - 50, 300, 40)

        self.__username_text.enter(events)

        if not self.__username_text.access() == "":
            self.__username = self.__username_text.access().lower()
            self.__section = "pass"
            self.__username_text.clear_text()
            self.__display_username.set_all(self.__username, BLACK, P2 , 22, SCREEN_WIDTH//2- 45, SCREEN_HEIGHT//2- 40)


    def __password_setter(self, events):
        self.__display_username.draw_text(screen)
        self.__password_text.draw(events, screen, SCREEN_WIDTH//2- 50, SCREEN_HEIGHT//2 - 5, 300, 40)
        self.__password_text.enter(events)

        if not self.__password_text.access() == "":
            self.__password = self.__password_text.access()
            self.__username_text.clear_text()
            self.__password_text.clear_text()
            self.__section = "user"
            if self.__menu_choice == "login":
                self.__menu_choice = "game"

            if self.__menu_choice == "sign_up":
                self.__menu_choice = "creation"



    def __login_into_account(self, events):
        self.__go_back()
        self.__user_password(events)

    def __create_account(self, events):
        self.__go_back()
        self.__user_password(events)

        

    def __account_maker(self):
        conn = sqlite3.connect("database/GoGolfDB.db")
        c = conn.cursor()
        self.__username = self.__username .replace(" ", "_")
        for i in range(len(self.__password)):
            if self.__password[i] == " ":
                self.__error = "Password cannot contain spaces"
                self.__menu_choice = ""
                return
        try:
            username_sql = c.execute(f'SELECT Username FROM UserRegister WHERE Username IS "{self.__username}"')
            username_sql = str("".join(c.fetchone()))
        except TypeError: 
            pass #Username not in the database

        if username_sql == self.__username: 
            self.__error = "Username taken"

        elif self.__username == "": 
            self.__error = "Username was blank"

        else:
            c.execute(f"INSERT INTO UserRegister (Username, Password) VALUES ('{self.__username.lower()}', '{self.__password}')")
            c.execute(f"""INSERT INTO HOLE3NUMBER (Username) VALUES ('{self.__username.lower()}')""")
            c.execute(f"""INSERT INTO HOLE5NUMBER (Username) VALUES ('{self.__username.lower()}')""")

        
        self.__clear_info()
        conn.commit()
        conn.close()
        self.__menu_choice = ""



    def __go_back(self):
        if self.__back.draw(screen):
            self.__menu_choice = ""


    def account_menu(self):
        while self.__InMenu:
            self.__bg.draw_background()
            events = pygame.event.get()

            self.__display_error.set_all(self.__error, RED, P2, 30, 30, 30 )
            self.__display_error.draw_text(screen)

            if self.__menu_choice == "":
                self.__buttons(events)

            if self.__menu_choice == "login":
                self.__login_into_account(events)
            
            if self.__menu_choice == "sign_up":
                self.__create_account(events)

            if self.__menu_choice == "creation":
                self.__account_maker()

            if self.__menu_choice == "game":
                if self.__if_account_exist():
                    return self.__username
                else:
                    self.__menu_choice = ""
            self.EventHandler(events)



    def __if_username_exist(self, conn):
        c = conn.cursor()
        username_sql = c.execute(f'SELECT Username FROM UserRegister WHERE Username IS "{self.__username}"')
        
        try:
            username_sql =  str("".join(c.fetchone())).lower()
        except TypeError:
            self.__clear_info()
            self.__error = "username does not exist"
            conn.close()
        return username_sql



    def __if_account_exist(self):
        conn = sqlite3.connect("database/GoGolfDB.db")
        c = conn.cursor()
        username_sql = self.__if_username_exist(conn)

        if username_sql == self.__username:
            password_sql = c.execute(f'SELECT Password FROM UserRegister WHERE Username IS "{self.__username}"')
            try:
                password_sql =  str("".join(c.fetchone())).lower()
            except TypeError:
                pass
            if password_sql == self.__password:
                conn.close()
                return True
            else:
                self.__clear_info()
                conn.close()
        self.__error = "username/password is not correct"
        conn.close()     
        return False

    
    def __clear_info(self):
        self.__username = ""
        self.__password = ""
            

    def EventHandler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                LOGGER.info("Quit Application")
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)




class MainMenu():
    def __init__(self, bg):
        self.__bg = bg
        self.__InMenu = True
        self.__InHoleMenu = False
        self.__play = gogolf_lilbray.Button(50, 50, play_button, 0.5)
        self.__lb = gogolf_lilbray.Button(50, 200, lb_buttons, 0.5)
        self.__quit = gogolf_lilbray.Button(50, 350, quit_buttons, 0.5)
        self.__three_hole = gogolf_lilbray.Button(50, 50, three_hole_button, 0.5)
        self.__five_hole = gogolf_lilbray.Button(50, 200, five_hole_button, 0.5)
        self.__back = gogolf_lilbray.Button(50, SCREEN_HEIGHT-150, back_buttons, 0.5)
        self.__strokes_lb = gogolf_lilbray.Button(50, 50, strokes_button, 0.5)
        self.__score_lb = gogolf_lilbray.Button(50, 200, score_button, 0.5)
        self.__time_lb = gogolf_lilbray.Button(50, 350, time_button, 0.5)
        self.__game = None #temp
        self.__menu_choice = ""
        self.__leaderboard_filter = "score"
        self.__leaderboard_hole = None
        self.__leaderboard_text = gogolf_lilbray.Text()

    
    def __holes(self, username):
        if self.__three_hole.draw(screen):
                self.__game = gogolf_gui.GoGolf(username)
                self.__game.PlayGame(3)
        if self.__five_hole.draw(screen):
                self.__game = gogolf_gui.GoGolf(username)
                self.__game.PlayGame(5)
        if self.__back.draw(screen):
            self.__menu_choice = ""



    def __buttons(self):
        if self.__play.draw(screen):
            self.__menu_choice = "play"

        if self.__lb.draw(screen):
            self.__menu_choice = "leaderboard_hole_select"

        if self.__quit.draw(screen):
            sys.exit()

    def __leaderboard_holes(self):
        if self.__three_hole.draw(screen):
            self.__menu_choice = "leaderboard"
            self.__leaderboard_hole = 3
            

        if self.__five_hole.draw(screen):
            self.__menu_choice = "leaderboard"
            self.__leaderboard_hole = 5

        if self.__back.draw(screen):
            self.__menu_choice = ""

    def __filter_options(self):
        if self.__strokes_lb.draw(screen):
            self.__leaderboard_filter = "STROKES"
        if self.__score_lb.draw(screen):
            self.__leaderboard_filter = "SCORE"
        if self.__time_lb.draw(screen):
            self.__leaderboard_filter = "TOTAL_TIME"
        if self.__back.draw(screen):
            self.__menu_choice = "leaderboard_hole_select"


    def __leaderboard(self, username):
        self.__filter_options()

        conn = sqlite3.connect("database/GoGolfDB.db")  # Fix the path to the database
        c = conn.cursor()
        c.execute(f"""SELECT HOLE{self.__leaderboard_hole}NUMBER.Username, HOLES{self.__leaderboard_hole}.{self.__leaderboard_filter}
        FROM HOLE{self.__leaderboard_hole}NUMBER INNER JOIN HOLES{self.__leaderboard_hole} 
        ON HOLE{self.__leaderboard_hole}NUMBER.HOLE{self.__leaderboard_hole}ID == HOLES{self.__leaderboard_hole}.HOLES{self.__leaderboard_hole}ID
        ORDER BY HOLES{self.__leaderboard_hole}.{self.__leaderboard_filter} DESC
        """)
        player_positions = [i for i in c.fetchall()]
        leader_board = []

        for i in range(0, len(player_positions)):
            if self.__leaderboard_filter == "TOTAL_TIME":
                self.__leaderboard_filter = "TIME"
            pos = f"{str(i+1)}.{"":3}"
            string_pos_name = f"{player_positions[i][0]:6}"
            string_result = f"{self.__leaderboard_filter} : {player_positions[i][1]:6}"
            leader_board.append((pos, string_pos_name, string_result))

        conn.close()

        lb_y_pos = 50
        lb_x_pos = SCREEN_WIDTH // 2

        if self.__leaderboard_filter == "TIME":
                self.__leaderboard_filter = "TOTAL_TIME"

        for i in range(0, len(player_positions)):
            self.__leaderboard_text.set_all(leader_board[i][0], ORANGE, P2, 20, lb_x_pos, lb_y_pos)
            self.__leaderboard_text.draw_text(screen)
            self.__leaderboard_text.set_all(leader_board[i][1], ORANGE, P2, 20, lb_x_pos + 50, lb_y_pos)
            self.__leaderboard_text.draw_text(screen)
            self.__leaderboard_text.set_all(leader_board[i][2], ORANGE, P2, 20, lb_x_pos + 150, lb_y_pos)
            self.__leaderboard_text.draw_text(screen)
            lb_y_pos += 25


            







        #Draw a leaderbaord wtih 10 peoples name for each page (that cand be scroll with a & d)

        #Buttons on the side for score, strokes, time, back


        

            

    def main_menu(self, logo, username):
        while self.__InMenu:
            events = pygame.event.get()

            self.__bg.draw_background()
            self.__bg.side_bar()
            
            if not self.__menu_choice == "leaderboard":
                logo.floatiing_logo(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 200)
            if self.__menu_choice == "":
                self.__buttons()

            if self.__menu_choice == "play":
                self.__holes(username)

            if self.__menu_choice == "leaderboard_hole_select":
                self.__leaderboard_holes()

            if self.__menu_choice == "leaderboard":
                self.__leaderboard(username)
                
            
    
            self.EventHandler(events)
        
    def EventHandler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                LOGGER.info("Quit Application")
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)
            
        


def menu():
    Tee = Tee_Box()
    Tee.Game()