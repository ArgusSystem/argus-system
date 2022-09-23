import logging
from time import sleep

from ..src.application import run


with run('endless_application') as application:
    time_alive = 0

    while not application.is_stopped():
        logging.info(f"I've been alive for {time_alive} seconds!")
        sleep(1)
        time_alive += 1

