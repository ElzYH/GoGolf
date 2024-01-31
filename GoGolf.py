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
    c.execute("""CREATE TABLE HOLE3NUMBER (
        Username VARCHAR(8),
        HOLE3ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY(Username) REFERENCES UserRegister(Username),
        FOREIGN KEY(HOLE3ID) REFERENCES HOLES3(HOLES3ID)
    )""")
    
    c.execute("""CREATE TABLE HOLE5NUMBER (
        Username VARCHAR(8),
        HOLE5ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY(Username) REFERENCES UserRegister(Username),
        FOREIGN KEY(HOLE5ID) REFERENCES HOLES5(HOLES5ID)
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



def create_database():
    LOGGER.info("Creating database")
    conn = sqlite3.connect("database/GoGolfDB.db")
    c = conn.cursor()
    create_register_table(conn)
    create_holes_table(conn)
    create_selection_table(conn)
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








