import gogolf_menu
from pygame.locals import *
from Logger import *
import os
import sqlite3


#Checks if all that needed on application side to start the application
starting_check("GoGolf")

#Get name of current file being used
LOGGER = logging.getLogger(f"{__name__}")

#Starting log (info can be swaped for different use cases)
LOGGER.info(f'Application started')

LOGGER.info('Application started')

def create_register_table(conn):
    c = conn.cursor()
    c.execute("""CREATE TABLE UserRegister (
        Username VARCHAR(8) PRIMARY KEY,
        Password VARCHAR(8)
    )""")
    conn.commit()

def create_selection_table(conn):
    c = conn.cursor()
    for hole in [3,5]:
        c.execute(f"""CREATE TABLE HOLE{hole}NUMBER (
            Username VARCHAR(8),
            HOLE{hole}ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FOREIGN KEY(Username) REFERENCES UserRegister(Username),
            FOREIGN KEY(HOLE{hole}ID) REFERENCES HOLES{hole}(HOLES{hole}ID)
        )""")
    

    conn.commit()

def create_holes_table(conn):
    c = conn.cursor()
    for table in ["HOLES3", "HOLES5"]:
        c.execute(f"""CREATE TABLE {table} (
            {table}ID INTEGER KEY NOT NULL,
            SCORE INT,
            STROKES INT,
            TOTAL_TIME INT
        )""")
    conn.commit()

def create_skins_table(conn):
    c = conn.cursor()

    # Create SKINS table
    c.execute("""CREATE TABLE SKINS (
        SKINID INTEGER PRIMARY KEY AUTOINCREMENT,
        white BOOL,
        pink BOOL,
        blue BOOL,
        orange BOOL,
        red BOOL,
        gold BOOL,
        black BOOL
    )""")

    # Create WALLET table
    c.execute("""CREATE TABLE WALLET (
        COINID INTEGER PRIMARY KEY AUTOINCREMENT,
        coins INT
    )""")


    # Create PLAYER_SKINS table
    c.execute("""CREATE TABLE PLAYER_SKINS (
        Username VARCHAR(8),
        SKINID INTEGER ,
        COINID INTEGER ,
        FOREIGN KEY(Username) REFERENCES UserRegister(Username),
        FOREIGN KEY(SKINID) REFERENCES SKINS(SKINID),
        FOREIGN KEY(COINID) REFERENCES WALLET(COINID)
    )""")


    conn.commit()



def create_database():
    LOGGER.info("Creating database")
    conn = sqlite3.connect("database/GoGolfDB.db")
    c = conn.cursor()
    create_register_table(conn)
    create_holes_table(conn)
    create_selection_table(conn)
    create_skins_table(conn)
    conn.commit()
    conn.close()

    


def check_database():
    if os.path.exists("database/GoGolfDB.db"):
        LOGGER.info(f"Database is already created")
    else:
        LOGGER.warning("Database does not exist")
        create_database()

if __name__ == "__main__":
    LOGGER.info('Hello')
    check_database()
    gogolf_menu.menu()








