import gogolf_gui
from pygame.locals import *
from Logger import *


#Checks if all that needed on application side to start the application
starting_check("GoGolf")

#Get name of current file being used
LOGGER = logging.getLogger(f"{__name__}")

#Starting log (info can be swaped for different use cases)
LOGGER.info(f'Application started')

if __name__ == "__main__":
    LOGGER.info('Hello')
    gogolf_gui.gameloop()




