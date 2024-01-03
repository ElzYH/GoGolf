import logging
import os
import datetime
import gogolf_gui
import gogolf_body
from pygame.locals import *

def logger_setup():
    """Create the Logger for the application"""

    #Create the name of the log
    time = datetime.datetime.now()
    time ='GoGolf-' + str(time.strftime("%x")) + " T-"+ str(time.strftime("%X")) + '.log'
    time = str(time).replace("/","-").replace(" ","--").replace(":","-")

    #Creates the file within Logs directory
    logging.basicConfig(filename=f"Logs/{time}",filemode='w',
    format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)
    

def starting_check():
    """checks if all that needed on application side to start the application"""

    if not os.path.exists("Logs"): 
        os.mkdir("Logs")
    logger_setup()


#Checks if all that needed on application side to start the application
starting_check()

#Get name of current file being used
LOGGER = logging.getLogger(f"{__name__}")

#Starting log (info can be swaped for different use cases)
LOGGER.info(f'Application started')

if __name__ == "__main__":
    LOGGER.info('Hello')
    gogolf_gui.gameloop()




