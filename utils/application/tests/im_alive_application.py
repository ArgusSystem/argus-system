import logging
from time import sleep

from utils.application import run


with run('endless_application') as application:
    time_alive = 0

    while not application.is_stopped():
        logging.debug("I've been alive for %d seconds!", time_alive)
        sleep(1)
        time_alive += 1

