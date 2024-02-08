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
leaderboard_wall = pygame.image.load('Assests/leaderboard_wall.png')

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
random_button = pygame.image.load('Assests/random.png')
change_user_button =  pygame.image.load('Assests/change_user.png')
skins_button =  pygame.image.load('Assests/skins.png')
buy_skins_button = pygame.image.load('Assests/buy_skins.png')
select_skins_button = pygame.image.load('Assests/select_skin.png')

golf_names = ["white","pink","blue","orange","red","gold","black"]

golf_skins = [pygame.image.load(f'Assests/{skin}.png') for skin  in golf_names]

sign_up_button = pygame.image.load('Assests/sign_up.png')
login_button = pygame.image.load('Assests/login.png')

#Colours
GREY = (245, 244, 243)
BLUE = "#2596be"
WHITE = "#F5FEFD"
ORANGE = "#ff8500"
BLACK = "#000000"
RED = "#D21404"

#Backgorund widiths
bg_w = background_1.get_width()
bg_h = background_1.get_height()

#Fonts
WII_FONT = "Assests/Fonts/AOTFShinGoProMedium.otf"
PIXEL_FONT = "Assests/Fonts/04B_30__.TTF"
P2 = "Assests/Fonts/Retro Gaming.ttf"

#Display Widths and Heights
SCREEN_HEIGHT = 768 
SCREEN_WIDTH = 1366
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))



class Tee_Box():
    """Creates object for the game to start """

    def __init__(self):
        self.__run = True
        self.__BG = Background()
        self.__start_menu = StartScreen(self.__BG)
        self.__account = User(self.__BG)
        self.__menu = MainMenu(self.__BG)

    def Game(self):
        """Main Handler of the the program, where the start menu held
        and main menu"""

        while self.__run:

            #Start Menu
            if not self.__start_menu.get_running():
                self.__start_menu.start_menu()

            #Runs account menu and then the main menu 
            if self.__start_menu.get_running():
                self.__menu.main_menu(self.__start_menu, self.__account.account_menu())
                if not self.__menu.get_in_menu():
                    #Resets all menus
                    self.__start_menu.set_running(False)
                    self.__account.set_in_menu(True)
                    self.__account.set_menu("")
            self.EventHandler()


    def EventHandler(self):
        """Event Handler """

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                LOGGER.info("Quit Application")
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)

                
        
class Background():
    def __init__(self):
        self.__scroll = 0
        self.__tiles = ceil(SCREEN_WIDTH /  bg_w) + 1

    def draw_background(self):
        """Draw menu background """
    
        self.__scroll -= 4
        for i in range(0, self.__tiles):
            screen.blit(background_1, (i * bg_w + self.__scroll, 0))
            screen.blit(background_2, (i * bg_w + self.__scroll, 0))
            screen.blit(background_3, (i * bg_w + self.__scroll, 0))
        
        if abs(self.__scroll) > bg_w:
                self.__scroll = 0

    
    def side_bar(self):
        """Draw the game side bar for menu selection """
        pygame.draw.rect(screen, BLUE, (0, 0, 300, SCREEN_HEIGHT))


class StartScreen():
    def __init__(self , bg):
        self.__bg = bg
        self.__direction = 1
        self.__y = 1
        self.__text = gogolf_lilbray.Text()
        self.__start_running = False


    def sin_counter(self):
        """Changes the y coords by sin"""

        if abs(self.__y) % 90 == 0:
            self.__direction = -1
        self.__y +=0.05*self.__direction

    def floatiing_logo(self, x, y):
        """Draws Game Logo oscillating"""

        self.sin_counter()
        pos = (y) + (sin(self.__y)*10)
        screen.blit(logo, (x, pos))
        self.__text.set_all("Press Enter To Start", ORANGE, P2, 40, SCREEN_WIDTH//2 - 260, pos + 400)
        
    
    def start_menu(self):
        """Game Start screen"""

        keys =  pygame.key.get_pressed()
        self.__bg.draw_background()
        self.floatiing_logo(SCREEN_WIDTH//2- 300, (SCREEN_HEIGHT//2 - 280))
        self.__text.set_all("Press Enter To Start", ORANGE, P2, 40, SCREEN_WIDTH//2 - 260, (sin(self.__y)*10) + 450)
        self.__text.draw_text(screen)

        if keys[pygame.K_RETURN] or pygame.mouse.get_pressed()[0]:
            self.__start_running =  True


    def get_running(self):
        return self.__start_running

    def set_running(self, value):
        self.__start_running = value




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
        self.__item_box_text = gogolf_lilbray.Text()

    def __account_buttons(self, events):
        """Draws the game Login and Sign up buttons and return an input
        to menu choice varibale """

        if self.__login.draw(screen):
            self.__username_text.clear_text()
            self.__password_text.clear_text()
            self.__menu_choice = "login"

        if self.__sign_up.draw(screen):
            self.__username_text.clear_text()
            self.__password_text.clear_text()
            self.__menu_choice = "sign_up"


    def __draw_input_boxes(self):
        """Draws input boxes for user type his username and password"""

        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2- 50, SCREEN_HEIGHT//2 - 50, 300, 40))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2- 50, SCREEN_HEIGHT//2 - 5, 300, 40))
        self.__item_box_text.set_all("Username:", BLACK, P2, 20, SCREEN_WIDTH//2 - 190, SCREEN_HEIGHT//2 - 40)
        self.__item_box_text.draw_text(screen)
        self.__item_box_text.set_all("Password:", BLACK, P2, 20, SCREEN_WIDTH//2- 190, SCREEN_HEIGHT//2 + 5)
        self.__item_box_text.draw_text(screen)



    def __user_password(self, events):
        """Sets username and passwords inputs"""

        self.__draw_input_boxes()
        if self.__section == "user":
            self.__username_setter(events)

        elif self.__section == "pass":
            self.__password_setter(events)

        #Create a Superencipherment cipher (cipher that encrypted twice)
        #Change letters to ASCII to binary, apply xor, convert back to denary, ceaser cipher of one of 
        #5 keys (either 5, 28, 26, 66, 92)


    def __username_setter(self, events):
        """Sets username"""

        self.__display_username.set_text("")
        self.__username_text.draw(events, screen, SCREEN_WIDTH//2- 50, SCREEN_HEIGHT//2 - 50, 300, 40)

        self.__username_text.enter(events)

        if not self.__username_text.access() == "":
            self.__username = self.__username_text.access().lower()
            self.__section = "pass"
            self.__username_text.clear_text()
            self.__display_username.set_all(self.__username, BLACK, P2 , 22, SCREEN_WIDTH//2- 45, SCREEN_HEIGHT//2- 40)


    def __password_setter(self, events):
        """Sets password"""

        self.__display_username.draw_text(screen)
        self.__password_text.draw(events, screen, SCREEN_WIDTH//2- 50, SCREEN_HEIGHT//2 - 5, 300, 40)
        self.__password_text.enter(events)

        if not self.__password_text.access() == "":
            self.__password = self.__password_text.access()
            self.__username_text.clear_text()
            self.__password_text.clear_text()
            self.__section = "user"
            self.__account_menu_options()

    def __account_menu_options(self):
        """Depending on if user attmepting sign up or login it will 
        change the mneu choice after user enter there inputs correctly
        accordingly"""
        
        if self.__menu_choice == "login":
            self.__menu_choice = "game"

        if self.__menu_choice == "sign_up":
            self.__menu_choice = "creation"



    def __login_into_account(self, events):
        """Draws back button and inputs for login in """

        self.__go_back()
        self.__user_password(events)

    def __create_account(self, events):
        """Draws back button and inputs for account creation"""

        self.__go_back()
        self.__user_password(events)

    def __update_user_registery(self, conn):
        """Updates the table with user infomation"""

        c = conn.cursor()
        self.__password = gogolf_lilbray.encrypter(self.__password)
        c.execute(f"INSERT INTO UserRegister (Username, Password) VALUES ('{self.__username.lower()}', '{self.__password}')")
        c.execute(f"""INSERT INTO HOLE3NUMBER (Username) VALUES ('{self.__username.lower()}')""")
        c.execute(f"""INSERT INTO HOLE5NUMBER (Username) VALUES ('{self.__username.lower()}')""")
        
        last_inserted_id = []

        # Insert into SKINS table
        c.execute(f"""INSERT INTO SKINS (white, pink, blue, orange, red, gold, black) 
                    VALUES ('1', '0', '0', '0', '0', '0', '0')""")
        last_inserted_id.append(c.lastrowid)

        # Insert into WALLET table
        c.execute(f"""INSERT INTO WALLET (coins) 
                    VALUES ('0')""")
        last_inserted_id.append(c.lastrowid)

        # Insert into PLAYER_SKINS table
        c.execute(f"""INSERT INTO PLAYER_SKINS (Username, SKINID, COINID) 
                    VALUES ('{self.__username.lower()}', '{last_inserted_id[0]}', '{last_inserted_id[1]}')""")
        

    def __account_maker(self):
        """Checks if user has followed the account creation rules 
        and add there data to user registery """

        conn = sqlite3.connect("database/GoGolfDB.db")
        c = conn.cursor()
        #Removes spaces out of user name and repalces them with underscore
        self.__username = self.__username.replace(" ", "_")

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
            self.__update_user_registery(conn)

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
                self.__account_buttons(events)

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
        """Checks if username exist within the database, if it doesnt
        an error flag will shown on the screen """

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
        """Check if user trying to login infomation is correct. 
        This consit of checking for user username and password"""

        conn = sqlite3.connect("database/GoGolfDB.db")
        c = conn.cursor()
        username_sql = self.__if_username_exist(conn)

        if username_sql == self.__username:
            password_sql = c.execute(f'SELECT Password FROM UserRegister WHERE Username IS "{self.__username}"')
            try:
                password_sql =  str("".join(c.fetchone()))
                self.__password = gogolf_lilbray.encrypter(self.__password)
            except TypeError:
                pass
            print(f"sql: {password_sql} and enter : {self.__password}")
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
        """Sets the username abd password of the object to blank"""

        self.__username = ""
        self.__password = ""
            

    def EventHandler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                LOGGER.info("Quit Application")
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)

    
    def set_in_menu(self, value):
        self.__InMenu = value

    def set_menu(self, value):
        self.__menu_choice = value


class MainMenu():
    def __init__(self, bg):
        self.__bg = bg #Backgorund
        self.__InMenu = True #If in menu
        self.__play = gogolf_lilbray.Button(50, 50, play_button, 0.5)
        self.__lb = gogolf_lilbray.Button(50, 200, lb_buttons, 0.5)
        self.__change_user = gogolf_lilbray.Button(50, 350, change_user_button, 0.5)
        self.__skins = gogolf_lilbray.Button(50, 500, skins_button, 0.5)
        self.__quit = gogolf_lilbray.Button(50, 650, quit_buttons, 0.5)
        self.__three_hole = gogolf_lilbray.Button(50, 50, three_hole_button, 0.5)
        self.__five_hole = gogolf_lilbray.Button(50, 200, five_hole_button, 0.5)
        self.__random_hole = gogolf_lilbray.Button(50, 350, random_button, 0.5)
        self.__back = gogolf_lilbray.Button(50, SCREEN_HEIGHT-150, back_buttons, 0.5)
        self.__strokes_lb = gogolf_lilbray.Button(50, 50, strokes_button, 0.5)
        self.__score_lb = gogolf_lilbray.Button(50, 200, score_button, 0.5)
        self.__time_lb = gogolf_lilbray.Button(50, 350, time_button, 0.5)
        self.__buy_skins = gogolf_lilbray.Button(50, 50, buy_skins_button, 0.5)
        self.__select_skins = gogolf_lilbray.Button(50, 200, select_skins_button, 0.5)
        self.__game = None #GoGolf Object
        self.__menu_choice = "" #Which menu to access
        self.__leaderboard_filter = "SCORE" #Filter for leaderbaord, defaults to SCORE
        self.__leaderboard_hole = None #Which collections of holes results to display
        self.__leaderboard_text = gogolf_lilbray.Text() 
        self.__change_range = 15 #Range of user to display
        self.__skin_buttons = self.__set_skin_buttons()
        self.__GOLFBALL = self.__GOLFBALL_SELECT("white")
        self.__prices_text = gogolf_lilbray.Text()
        self.__wallet_text = gogolf_lilbray.Text()

    def __set_skin_buttons(self):
        """Creates list of golg skins buttons """

        x = 400
        y = 100
        col_count = 0
        temp_skins_buttons = []
        for i in range(len(golf_skins)):
            temp_skins_buttons.append(gogolf_lilbray.Button(x, y, golf_skins[i], 0.5))
            x+=300
            col_count+=1
            if col_count > 2:
                x = 400
                y+= 150
                col_count = 0
        return temp_skins_buttons




    def __GOLFBALL_SELECT(self, value):
        """Selects the correct image of the GOlFBAll image"""

        return pygame.image.load(f'Assests/{value}_ball.png')
    
    def __holes(self, username):
        """Game Select for what type for game the user want to play """

        if self.__three_hole.draw(screen):
                self.__game = gogolf_gui.GoGolf(username, 3, False, self.__GOLFBALL)
                self.__game.PlayGame(3)

        if self.__five_hole.draw(screen):
                self.__game = gogolf_gui.GoGolf(username, 5, False, self.__GOLFBALL)
                self.__game.PlayGame(5)

        if self.__random_hole.draw(screen):
            self.__game = gogolf_gui.GoGolf(username, 1, True, self.__GOLFBALL)
            self.__game.PlayGame(1)
            
        if self.__back.draw(screen):
            self.__menu_choice = ""



    def __main_menu_button(self):
        """Main menu buttons to play the game, access the leaderboard, quit """

        if self.__play.draw(screen):
            self.__menu_choice = "play"

        if self.__lb.draw(screen):
            self.__menu_choice = "leaderboard_hole_select"

        if self.__change_user.draw(screen):
            self.__menu_choice = "back"

        if self.__skins.draw(screen):
            self.__menu_choice = "skins"

        if self.__quit.draw(screen):
            sys.exit()

    def __leaderboard_holes(self):
        """Leaderboard game mode button select """

        if self.__three_hole.draw(screen):
            self.__menu_choice = "leaderboard"
            self.__leaderboard_hole = 3
            

        if self.__five_hole.draw(screen):
            self.__menu_choice = "leaderboard"
            self.__leaderboard_hole = 5

        if self.__back.draw(screen):
            self.__menu_choice = ""

    def __filter_options(self):
        """Filter options buttons for the leaderboard """
        
        if self.__strokes_lb.draw(screen):
            self.__leaderboard_filter = "STROKES"

        if self.__score_lb.draw(screen):
            self.__leaderboard_filter = "SCORE"

        if self.__time_lb.draw(screen):
            self.__leaderboard_filter = "TOTAL_TIME"

        if self.__back.draw(screen):
            self.__menu_choice = "leaderboard_hole_select"


    def __ASC_DSC(self):
        """If data should repsented ascending or descending """

        if self.__leaderboard_filter == "STROKES" or self.__leaderboard_filter == "TOTAL_TIME":
            return "ASC"
        else:
            return "DESC"

    def __leaderboard_range_changer(self):
        """Changes the range of data to be drawn on the screen"""

        keys =  pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.__change_range += 15

        if keys[pygame.K_a] and self.__change_range > 15:
            self.__change_range -= 15


    def __draw_leaderboard(self, player_positions, leader_board, lb_x_pos, lb_y_pos):
        """Display Users leaderboard results onto the GUI """

        for i in range(-15 + self.__change_range, self.__change_range):

            if i < len(player_positions):
                self.__leaderboard_text.set_all(leader_board[i][0], BLACK, P2, 20, lb_x_pos, lb_y_pos)
                self.__leaderboard_text.draw_text(screen)
                self.__leaderboard_text.set_all(leader_board[i][1], BLACK, P2, 20, lb_x_pos + 50, lb_y_pos)
                self.__leaderboard_text.draw_text(screen)
                self.__leaderboard_text.set_all(leader_board[i][2], BLACK, P2, 20, lb_x_pos + 150, lb_y_pos)
                self.__leaderboard_text.draw_text(screen)
                lb_y_pos += 35
            else:
                break


    def __leaderboard(self):
        """Leaderboard menu"""

        self.__filter_options()
        screen.blit(leaderboard_wall, (SCREEN_WIDTH//2 - 50, 75))
        conn = sqlite3.connect("database/GoGolfDB.db")  # Fix the path to the database

        order = self.__ASC_DSC()

        c = conn.cursor()

        #Access the databases to find game stats for all players
        c.execute(f"""SELECT HOLE{self.__leaderboard_hole}NUMBER.Username, HOLES{self.__leaderboard_hole}.{self.__leaderboard_filter}
        FROM HOLE{self.__leaderboard_hole}NUMBER INNER JOIN HOLES{self.__leaderboard_hole} 
        ON HOLE{self.__leaderboard_hole}NUMBER.HOLE{self.__leaderboard_hole}ID == HOLES{self.__leaderboard_hole}.HOLES{self.__leaderboard_hole}ID
        ORDER BY HOLES{self.__leaderboard_hole}.{self.__leaderboard_filter} {order}
        """)

        #Player_postions is where all player stats are saves tempoarily 
        player_positions = [i for i in c.fetchall()]
        leader_board = []
        conn.close()

        self.__leaderboard_range_changer()
        
        #Sets all strings to be drawn for each player
        for i in range(0, len(player_positions)):
            if self.__leaderboard_filter == "TOTAL_TIME":
                self.__leaderboard_filter = "TIME"
            pos = f"{str(i+1)}.{"":3}"
            string_pos_name = f"{player_positions[i][0]:6}"
            string_result = f"{self.__leaderboard_filter} : {player_positions[i][1]:6}"
            leader_board.append((pos, string_pos_name, string_result))

        if self.__leaderboard_filter == "TIME": self.__leaderboard_filter = "TOTAL_TIME"
        self.__draw_leaderboard(player_positions, leader_board, SCREEN_WIDTH // 2, 125)


    def __skins_menu(self):
        """Skins menu"""
        
        if self.__select_skins.draw(screen):
            self.__menu_choice = "select_skins"

        if self.__buy_skins.draw(screen):
            self.__menu_choice = "buy_skins"

        if self.__back.draw(screen):
            self.__menu_choice = ""

    def __user_skin_info(self, conn, username):

        c = conn.cursor()

        c.execute(f"""SELECT WALLET.coins, PLAYER_SKINS.COINID, PLAYER_SKINS.SKINID
                FROM PLAYER_SKINS INNER JOIN WALLET
                ON PLAYER_SKINS.COINID == WALLET.COINID
                WHERE PLAYER_SKINS.Username = '{username}'""")

        return c.fetchone()



    def __buy_menu(self, username):
        """Allows a user to purchase skins with there coins """

        screen.fill(BLUE) #Hides laggyness

        if self.__back.draw(screen):
            self.__menu_choice = "skins"

        conn = sqlite3.connect("database/GoGolfDB.db")
        c = conn.cursor()
        coinid = self.__user_skin_info(conn, username)


        x = 400
        y = 225
        count = 0 #Amount coloums allowed 
        
        #Draws each price of every button and button
        for button_index in range(len(self.__skin_buttons)):
            self.__prices_text.set_all(f"Price: {button_index*82}", BLACK, P2, 14, x, y)
            x+= 300
            count += 1

            #Resets coloums
            if count > 2:
                x = 400
                y+= 150
                count = 0

            self.__prices_text.draw_text(screen)

            if self.__skin_buttons[button_index].draw(screen):
                c.execute(f"""SELECT {golf_names[button_index]}
                FROM SKINS
                WHERE SKINID IS {coinid[2]}""")
                skinid = c.fetchone()
                skinid = skinid[0]

                if (coinid[0] - (button_index*82)) > 0 and skinid == 0:
                    c.execute(f"""UPDATE WALLET
                        SET coins = {coinid[0] - (button_index*82)}
                        WHERE COINID = {coinid[1]}""")
                    conn.commit()

                    c.execute(f"""UPDATE SKINS 
                    SET {golf_names[button_index]} = 1
                    WHERE SKINID = {coinid[2]}""")
                    conn.commit()

            self.__wallet_text.set_all(f"Coins: {coinid[0]:5}", BLACK, P2, 15, SCREEN_WIDTH - 135, 20)
            self.__wallet_text.draw_text(screen)
        conn.close()
 
                    
    


    def __select_menu(self, username):
        """Selects skin that the current player/user owns """

        if self.__back.draw(screen):
            self.__menu_choice = "skins"

        conn = sqlite3.connect("database/GoGolfDB.db")
        c = conn.cursor()

        #Selects all data in SKINS table for that player
        c.execute(f"""SELECT SKINS.*
                FROM PLAYER_SKINS INNER JOIN SKINS
                ON PLAYER_SKINS.SKINID == SKINS.SKINID
                WHERE PLAYER_SKINS.Username = '{username}'
         """)
        skins_owned = c.fetchone()

        #Draws the buttons
        for button_index in range(1, len(self.__skin_buttons) + 1):
            if skins_owned[button_index] == 1:
                if self.__skin_buttons[button_index-1].draw(screen):
                    self.__GOLFBALL = self.__GOLFBALL_SELECT(golf_names[button_index-1])

        conn.commit()
        conn.close()

        
        


        
    def main_menu(self, logo, username):
        """Main Menu"""

        self.__InMenu = True
        self.__menu_choice = ""
        while self.__InMenu:
            events = pygame.event.get()

            self.__bg.draw_background()
            self.__bg.side_bar()
            
            if not self.__menu_choice in ["leaderboard", "buy_skins", "select_skins"]:
                logo.floatiing_logo(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 200)

            if self.__menu_choice == "":
                self.__main_menu_button()

            if self.__menu_choice == "play":
                self.__holes(username)

            if self.__menu_choice == "leaderboard_hole_select":
                self.__leaderboard_holes()

            if self.__menu_choice == "leaderboard":
                self.__leaderboard()

            if self.__menu_choice == "skins":
                self.__skins_menu()

            if self.__menu_choice == "buy_skins":
                self.__buy_menu(username)

            if self.__menu_choice == "select_skins":
                self.__select_menu(username)

            if self.__menu_choice == "back":
                self.__InMenu = False

                
            self.EventHandler(events)


    def get_in_menu(self):
        return self.__InMenu
        
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