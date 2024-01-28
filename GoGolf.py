import gogolf_gui
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

def create_register_table(conn):
    c = conn.cursor()
    c.execute("""CREATE TABLE UserRegister (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username VARCHAR(8),
        Password VARCHAR(8)
    )""")
    conn.commit()

    

def create_selection_table(conn):
    c = conn.cursor()
    c.execute("""CREATE TABLE Selection (
        ID AUTO_INCREMENT NOT NULL,
        HOLE3ID VARCHAR(6) NOT NULL,
        HOLE5ID VARCHAR(6) NOT NULL,
        PRIMARY KEY('HOLE3ID','HOLE5ID' ),
        FOREIGN KEY('ID')
        REFERENCES UserRegister(ID)
    )""")
    conn.commit()



def create_holes_table(conn):
    c = conn.cursor()
    for table in ["HOLES3", "HOLES5"]:
        c.execute(f"""CREATE TABLE {table} (
            {table}ID VARCHAR(6) NOT NULL,
            SCORE INT,
            STROKES INT,
            TOTAL_TIME INT,
            FOREIGN KEY({table}ID) REFERENCES Selection({table}ID)
        )
        """)
    conn.commit()


        # LEVEL1 VARCHAR(6) NOT NULL,
        # LEVEL2 VARCHAR(6) NOT NULL,
        # LEVEL3 VARCHAR(6) NOT NULL,
        # LEVEL4 VARCHAR(6) NOT NULL,
        # LEVEL5 VARCHAR(6) NOT NULL,




def create_database():
    LOGGER.info("Creating database")
    conn = sqlite3.connect("database/GoGolfDB.db")
    c = conn.cursor()
    create_register_table(conn )
    create_selection_table(conn)
    create_holes_table(conn)
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





