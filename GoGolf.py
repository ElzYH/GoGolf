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
    c.execute("""CREATE TABLE Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        AccountID INTEGER UNIQUE NOT NULL,
        Username VARCHAR(8) NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        Salt TEXT NOT NULL
    )""")
    conn.commit()


def create_holes_table(conn):
    c = conn.cursor()
    for table in ["Holes3", "Holes5"]:
        c.execute(f"""CREATE TABLE {table} (
            UserID INTEGER NOT NULL,
            Score INT,
            Strokes INT,
            Time INT,
            Played DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY(UserID) REFERENCES Users(UserID)
        )""")
    conn.commit()

def create_skins_table(conn):
    c = conn.cursor()

    # Create SKINS table
    c.execute("""CREATE TABLE Skins (
        AccountID INTEGER NOT NULL,
        White BOOL DEFAULT 1,
        Pink BOOL DEFAULT 0,
        Blue BOOL DEFAULT 0,
        Orange BOOL DEFAULT 0,
        Red BOOL DEFAULT 0,
        Gold BOOL DEFAULT 0,
        Black BOOL DEFAULT 0,
        FOREIGN KEY(AccountID) REFERENCES Users(AccountID)
    )""")


    # Create PLAYER_SKINS table
    c.execute("""CREATE TABLE Player_Skins (
        AccountID INTEGER NOT NULL,
        Coins INT DEFAULT 0,
        FOREIGN KEY(AccountID) REFERENCES Users(AccountID)
    )""")
    conn.commit()




def create_database():
    LOGGER.info("Creating database")
    conn = sqlite3.connect("database/GoGolfDB.db")
    c = conn.cursor()
    create_register_table(conn)
    create_holes_table(conn)
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








