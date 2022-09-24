import logging
from time import sleep

from utils.application import run


with run('counting_application') as application:
    for i in range(10):
        logging.debug(i)
        sleep(1)
