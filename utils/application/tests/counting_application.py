import logging
from time import sleep

from ..src.application import run


with run('counting_application') as application:
    for i in range(10):
        logging.info(i)
        sleep(1)
