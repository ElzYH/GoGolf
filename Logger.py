import logging
import os
import datetime


def logger_setup(name):
    """Create the Logger for the application"""

    #Create the name of the log
    time = datetime.datetime.now()
    time =f'{name}-' + str(time.strftime("%x")) + " T-"+ str(time.strftime("%X")) + '.log'
    time = str(time).replace("/","-").replace(" ","--").replace(":","-")

    #Creates the file within Logs directory
    logging.basicConfig(filename=f"Logs/{time}",filemode='w',
    format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)
    

def starting_check(name):
    """checks if all that needed on application side to start the application"""

    if not os.path.exists("Logs"): 
        os.mkdir("Logs")
    logger_setup(name)
